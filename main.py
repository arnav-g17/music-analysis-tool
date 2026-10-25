import argparse
from pathlib import Path

import librosa

from report import generate_report


SUPPORTED_EXTENSIONS = {".wav", ".mp3", ".flac", ".ogg", ".m4a", ".aiff", ".aif"}


def main():
    parser = argparse.ArgumentParser(
        description="Analyze a music file for tempo, key, and dynamics."
    )
    parser.add_argument("audio", help="Path to an audio file")
    parser.add_argument(
        "-o", "--output",
        help="Optional path for a text report, e.g. report.txt"
    )
    args = parser.parse_args()

    path = Path(args.audio)

    if not path.exists():
        parser.error(f"File not found: {path}")

    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        parser.error(
            f"Unsupported file type: {path.suffix}. "
            f"Use one of: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )

    print(f"Analyzing {path.name}...")

    try:
        y, sr = librosa.load(path, sr=None, mono=True)
        report, _ = generate_report(y, sr, filename=path.name)
    except Exception as exc:
        parser.error(f"Could not analyze audio: {exc}")

    print("\n" + report)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(report + "\n", encoding="utf-8")
        print(f"\nSaved report to {output_path}")


if __name__ == "__main__":
    main()
