import numpy as np


def get_dynamics(y, sr, frame_length=2048, hop_length=512):
    """Measure loudness, peak level, crest factor, and section-to-section dynamics."""
    y = np.asarray(y, dtype=float)

    if len(y) == 0:
        raise ValueError("Audio file contains no samples.")

    rms = float(np.sqrt(np.mean(y ** 2)))
    peak = float(np.max(np.abs(y)))

    rms_db = 20 * np.log10(rms + 1e-12)
    peak_db = 20 * np.log10(peak + 1e-12)
    crest_factor_db = peak_db - rms_db

    frame_rms = []
    for start in range(0, len(y), hop_length):
        frame = y[start:start + frame_length]
        if len(frame) == 0:
            continue
        frame_rms.append(np.sqrt(np.mean(frame ** 2) + 1e-12))

    frame_rms_db = 20 * np.log10(np.asarray(frame_rms) + 1e-12)
    dynamic_range_db = np.percentile(frame_rms_db, 95) - np.percentile(frame_rms_db, 10)

    return {
        "rms_db": round(float(rms_db), 1),
        "peak_db": round(float(peak_db), 1),
        "crest_factor_db": round(float(crest_factor_db), 1),
        "dynamic_range_db": round(float(dynamic_range_db), 1),
    }
