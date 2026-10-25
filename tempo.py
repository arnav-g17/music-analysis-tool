import librosa
import numpy as np


def resolve_octave_ambiguity(detected_bpm, typical_range=(70, 180)):
    """Return half/double-time candidates and the candidates in a typical range."""
    candidates = [detected_bpm, detected_bpm * 2, detected_bpm / 2]
    plausible = [
        c for c in candidates
        if typical_range[0] <= c <= typical_range[1]
    ]
    return candidates, plausible


def get_tempo(y, sr, hop_length=512):
    """Estimate tempo and flag likely half/double-time ambiguity."""
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr, hop_length=hop_length)
    tempo = float(np.asarray(tempo).reshape(-1)[0])

    onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop_length)
    tempogram = librosa.feature.tempogram(
        onset_envelope=onset_env, sr=sr, hop_length=hop_length
    )
    tempo_bins = librosa.tempo_frequencies(
        tempogram.shape[0], hop_length=hop_length, sr=sr
    )
    tempo_strength = np.mean(tempogram, axis=1)

    def score_at_bpm(target_bpm):
        idx = int(np.argmin(np.abs(tempo_bins - target_bpm)))
        return float(tempo_strength[idx])

    candidates, plausible = resolve_octave_ambiguity(tempo)

    # Prefer the plausible candidate with the strongest tempogram evidence.
    if plausible:
        likely_bpm = max(plausible, key=score_at_bpm)
    else:
        likely_bpm = tempo

    possible_octave_error = abs(likely_bpm - tempo) > 1

    return {
        "detected_bpm": tempo,
        "likely_bpm": float(likely_bpm),
        "possible_octave_error": possible_octave_error,
        "candidates": [float(c) for c in candidates],
    }
