# Music Analysis Tool

A Python audio-analysis tool that extracts useful musical and mixing information from a track without modifying the audio.

## Features

- **Tempo detection** with half/double-time ambiguity handling
- **Key detection** using CQT chroma features and major/minor key profiles
- **Dynamics analysis** including RMS loudness, peak level, crest factor, and section-to-section dynamic range
- **Interpretation layer** that turns measurements into practical observations
- **Command-line interface** for analyzing WAV, MP3, FLAC, OGG, M4A, and AIFF files
- **Text report export** for saving analysis results

## Setup

Use Python 3.10+.

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Analyze a track:

```bash
python main.py "path/to/song.wav"
```

Save the report:

```bash
python main.py "path/to/song.wav" -o report.txt
```

## Example output

```text
=== TEMPO ===
Detected tempo: 124.0 BPM
Detected tempo appears internally plausible.

=== KEY ===
Estimated key: C major
Confidence: 0.812 (high) — likely reliable.

=== DYNAMICS ===
Average loudness: -12.4 dBFS
Peak level: -1.2 dBFS — reasonable headroom.
Crest factor: 8.3 dB — moderate dynamic behavior.
Dynamic range: 7.9 dB — difference between relatively loud and quiet sections.
```

## Limitations

The analysis is intentionally advisory rather than authoritative. Tempo detection can confuse half-time and double-time interpretations, and key detection can be less reliable on tracks with modulation, ambiguous harmony, or substantial non-tonal content. Dynamic measurements also depend on the mastering and genre of the source track.

## Project structure

```text
music-analysis/
├── main.py
├── report.py
├── tempo.py
├── key.py
├── dynamics.py
├── requirements.txt
├── README.md
└── .gitignore
```
