# Stockpile

Automated CLI pipeline for generating, reviewing, and packaging AI-generated stock images and videos. Orchestrates multiple AI providers — Claude for creative direction and metadata, Google Gemini for image generation, and Kling (via fal.ai) for video — into a repeatable weekly production workflow.

## Why This Exists

Stock content creation involves repetitive steps: writing prompts, generating images, reviewing quality, tagging metadata, creating video variants, and organizing exports. Stockpile turns that into a guided CLI workflow where AI handles the creative heavy lifting and the human stays in the loop for quality control.

## Key Features

- **Multi-provider orchestration** — coordinates Claude, Gemini, and Kling APIs through a single CLI session
- **Two-mode workflow** — Image mode (prompt → generate → review → metadata → package) and Video mode (select scene → video prompts → generate → review → package)
- **Human-in-the-loop review** — opens File Explorer for visual inspection; approve/reject per asset with regeneration options
- **Intelligent prompt generation** — loads all past prompts as context so Claude avoids repetition across sessions
- **Vision-powered metadata** — Claude analyzes generated images to produce stock-ready titles, descriptions, and keyword tags
- **Dry-run mode** — full pipeline execution with placeholder content and no API calls, useful for development and testing
- **Provider abstraction** — image and video generation use ABC base classes, making it straightforward to swap in new providers

## Architecture

```
pipeline/
├── __main__.py              # Entry point
├── main.py                  # Main menu + mode orchestration
├── config.py                # Environment, API keys, pricing, paths
├── api/
│   ├── claude_api.py        # Prompt generation, metadata, video prompts, slugs
│   ├── image_api.py         # ImageProvider ABC → Gemini, Placeholder
│   └── video_api.py         # VideoProvider ABC → Kling, Placeholder
├── workflow/
│   ├── prompt_gen.py        # Past prompt loading, Claude prompt creation
│   ├── image_gen.py         # Image generation orchestration
│   ├── video_gen.py         # Video generation orchestration
│   ├── metadata_gen.py      # Vision-based metadata + video prompt generation
│   ├── review.py            # Interactive approve/reject flow
│   └── packaging.py         # Export packaging for upload
└── utils/
    ├── file_manager.py      # Directory creation, naming conventions
    └── pricing.py           # Provider cost comparison display
```

## Getting Started

### Prerequisites

- Python 3.11+
- API keys for [Anthropic](https://console.anthropic.com/), [Google AI Studio](https://aistudio.google.com/), and [fal.ai](https://fal.ai/) (optional — dry-run works without them)

### Installation

```bash
git clone https://github.com/alex-olinger/stockpile.git
cd stockpile
pip install -r requirements.txt
```

### Configuration

```bash
cp .env.example .env
# Add your API keys to .env:
#   ANTHROPIC_API_KEY=sk-ant-...
#   GOOGLE_API_KEY=...
#   FAL_KEY=...
```

### Usage

```bash
# Run the full pipeline
python -m pipeline

# Dry-run mode (no API keys needed, placeholder content)
python -m pipeline --dry-run
```

The CLI presents a main menu:

```
=== Stockpile Main Menu ===
  [W] Select/change week
  [I] Image generation mode
  [V] Video generation mode
  [Q] Quit
```

**Image mode** walks through scene setup, prompt generation, image generation, review, metadata creation, and packaging. **Video mode** picks up from existing approved images to generate video variants.

## Content Organization

```
content/
  images/week10_20260302/golden-hour-portrait/
    base/           # Base images + prompts
    variations/     # Variation images + prompts
    exports/        # Approved assets + metadata
  videos/week10_20260302/golden-hour-portrait/
    base/           # Base videos + video prompts
    variations/     # Variation videos
    exports/        # Approved videos

outputs/week10_20260302/golden-hour-portrait/   # Flat export for upload
rejected/week10_20260302/golden-hour-portrait/  # Rejected assets
```

Week folders use ISO week numbering (`weekNN_YYYYMMDD` where the date is the Monday of that week).

## Testing

```bash
pytest
pytest tests/ -v
```

Tests mirror the pipeline structure and cover each module independently. Dry-run paths are tested without requiring API keys; real API calls are tested with mocked clients.

## Tech Stack

| Component | Technology | Role |
|-----------|-----------|------|
| Orchestration | Python CLI | Main menu, workflow sequencing |
| Creative Direction | Claude (Anthropic) | Prompts, metadata, video prompts, scene slugs |
| Image Generation | Google Gemini | 1920x1080 stock images |
| Video Generation | Kling (fal.ai) | 10s image-to-video clips |
| Testing | pytest | Unit tests with mocked providers |

## License

This project is not currently licensed for redistribution.
