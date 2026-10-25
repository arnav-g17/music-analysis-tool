import librosa
import numpy as np

MAJOR_PROFILE = np.array([
    6.35, 2.23, 3.48, 2.33, 4.38, 4.09,
    2.52, 5.19, 2.39, 3.66, 2.29, 2.88
])

MINOR_PROFILE = np.array([
    6.33, 2.68, 3.52, 5.38, 2.60, 3.53,
    2.54, 4.75, 3.98, 2.69, 3.34, 3.17
])

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def get_key(y, sr):
    """Estimate the most likely musical key using CQT chroma and key profiles."""
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    chroma_avg = np.mean(chroma, axis=1)

    best_score = -np.inf
    best_key = None

    for mode_name, profile in [("major", MAJOR_PROFILE), ("minor", MINOR_PROFILE)]:
        for tonic in range(12):
            rotated_profile = np.roll(profile, tonic)
            score = np.corrcoef(chroma_avg, rotated_profile)[0, 1]

            if np.isnan(score):
                continue

            if score > best_score:
                best_score = score
                best_key = f"{NOTE_NAMES[tonic]} {mode_name}"

    return best_key, float(best_score)
