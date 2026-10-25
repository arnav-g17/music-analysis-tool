from tempo import get_tempo
from key import get_key
from dynamics import get_dynamics


def interpret_dynamics(dynamics):
    lines = [f"Average loudness: {dynamics['rms_db']} dBFS"]

    if dynamics["peak_db"] > -1:
        lines.append(
            f"Peak level: {dynamics['peak_db']} dBFS — close to clipping; consider more headroom."
        )
    elif dynamics["peak_db"] > -3:
        lines.append(
            f"Peak level: {dynamics['peak_db']} dBFS — limited headroom; check loud sections carefully."
        )
    else:
        lines.append(f"Peak level: {dynamics['peak_db']} dBFS — reasonable headroom.")

    if dynamics["crest_factor_db"] < 6:
        lines.append(
            f"Crest factor: {dynamics['crest_factor_db']} dB — strong compression/limiting may be present."
        )
    elif dynamics["crest_factor_db"] > 15:
        lines.append(
            f"Crest factor: {dynamics['crest_factor_db']} dB — very dynamic; compare against an appropriate reference."
        )
    else:
        lines.append(
            f"Crest factor: {dynamics['crest_factor_db']} dB — moderate dynamic behavior."
        )

    lines.append(
        f"Dynamic range: {dynamics['dynamic_range_db']} dB — difference between relatively loud and quiet sections."
    )
    return lines


def interpret_key(key, confidence):
    lines = [f"Estimated key: {key}"]

    if confidence > 0.7:
        level = "high"
        advice = "likely reliable"
    elif confidence > 0.5:
        level = "moderate"
        advice = "worth double-checking by ear"
    else:
        level = "low"
        advice = "the track may be harmonically ambiguous or contain significant non-tonal content"

    lines.append(f"Confidence: {confidence:.3f} ({level}) — {advice}.")
    return lines


def interpret_tempo(tempo_result):
    detected = tempo_result["detected_bpm"]
    likely = tempo_result["likely_bpm"]

    lines = [f"Detected tempo: {detected:.1f} BPM"]

    if tempo_result["possible_octave_error"]:
        lines.append(
            f"Possible half/double-time ambiguity: {likely:.1f} BPM is the stronger plausible candidate."
        )
        lines.append(
            "Tempo detection can confuse a beat with its half or double; verify the pulse by ear."
        )
    else:
        lines.append("Detected tempo appears internally plausible.")

    return lines


def analyze_audio(y, sr):
    tempo_result = get_tempo(y, sr)
    key, confidence = get_key(y, sr)
    dynamics = get_dynamics(y, sr)

    return {
        "tempo": tempo_result,
        "key": {"key": key, "confidence": confidence},
        "dynamics": dynamics,
    }


def generate_report(y, sr, filename=None):
    results = analyze_audio(y, sr)
    tempo_result = results["tempo"]
    key_result = results["key"]
    dynamics = results["dynamics"]

    lines = []
    if filename:
        lines.append(f"MUSIC ANALYSIS REPORT — {filename}")
        lines.append("=" * 50)

    lines.append("=== TEMPO ===")
    lines.extend(interpret_tempo(tempo_result))

    lines.append("\n=== KEY ===")
    lines.extend(interpret_key(key_result["key"], key_result["confidence"]))

    lines.append("\n=== DYNAMICS ===")
    lines.extend(interpret_dynamics(dynamics))

    return "\n".join(lines), results
