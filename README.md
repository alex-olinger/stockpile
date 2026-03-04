# Stockpile

Automated CLI pipeline for generating, reviewing, and packaging AI-generated stock images and videos. Orchestrates multiple AI services — Claude for creative direction and metadata, Google Gemini for image generation, and Kling for video — into a single repeatable workflow.

## Why This Exists

Stock content creation involves a lot of repetitive steps: writing prompts, generating images, creating variations, tagging metadata, producing video versions, and organizing everything for upload. Stockpile automates the entire pipeline while keeping a human in the loop for quality control.

## How It Works

```
Prompt Generation ──► Image Generation ──► Review ──► Metadata ──► Video ──► Package
     (Claude)            (Gemini)         (Human)    (Claude)     (Kling)    (Upload-ready)
```

**Image mode** walks through scene setup, prompt generation, image creation, human review, and metadata tagging. **Video mode** takes approved images and generates motion video from them. Both modes output upload-ready asset bundles.

## Architecture

```
pipeline/
├── api/                   # Provider abstraction layer
│   ├── claude_api.py      # Prompt generation, metadata, video prompts (Anthropic SDK)
│   ├── image_api.py       # ImageProvider ABC → GeminiProvider, PlaceholderProvider
│   └── video_api.py       # VideoProvider ABC → KlingProvider, PlaceholderVideoProvider
├── workflow/              # Pipeline step orchestration
│   ├── prompt_gen.py      # Past-prompt-aware generation to avoid repetition
│   ├── image_gen.py       # Batch image generation with cost tracking
│   ├── video_gen.py       # Image-to-video generation via fal.ai
│   ├── metadata_gen.py    # Claude vision → structured metadata JSON
│   ├── review.py          # Terminal-based approve/reject with File Explorer
│   └── packaging.py       # Flat output directory for stock site upload
├── utils/
│   ├── file_manager.py    # ISO week directories, naming conventions, file ops
│   └── pricing.py         # Provider cost comparison display
├── config.py              # Environment, API keys, pricing data, paths
└── main.py                # Menu-driven CLI orchestration
```

### Key Design Decisions

- **Provider pattern** — Image and video APIs use abstract base classes, making it straightforward to swap Gemini for DALL-E or Kling for Runway without touching workflow code
- **Context-aware prompts** — All previous prompts are loaded and sent to Claude on each generation call, preventing duplicate scenes across sessions
- **Dry-run mode** — Full pipeline execution with placeholder content (Pillow-generated PNGs, dummy metadata) — no API keys required for development or testing
- **Human-in-the-loop** — Every generated asset goes through manual review before packaging; rejected assets are archived separately

## Quick Start

```bash
pip install -r requirements.txt
cp .env.example .env   # Add your API keys
python -m pipeline
```

```bash
# Development — no API keys needed
python -m pipeline --dry-run
```

## Tech Stack

| Component | Technology | Role |
|-----------|-----------|------|
| Orchestration | Python | CLI pipeline with menu-driven modes |
| Creative direction | Claude (Anthropic API) | Prompt generation, metadata, video prompts |
| Image generation | Google Gemini | 1920x1080 photorealistic images |
| Video generation | Kling (fal.ai) | 10s image-to-video, 1920x1080 |
| Vision analysis | Claude Vision | Image → metadata JSON, image → video prompt |
| Testing | pytest | 46 tests across 17 test files |

## Testing

```bash
python -m pytest
python -m pytest tests/ -v
```

The test suite mirrors the `pipeline/` package structure. Dry-run paths are tested without API mocking; real API paths use monkeypatched clients.

## Project Structure

```
content/
  images/weekNN_YYYYMMDD/scene-slug/{base,variations,exports}/
  videos/weekNN_YYYYMMDD/scene-slug/{base,variations,exports}/
outputs/weekNN_YYYYMMDD/scene-slug/   # Upload-ready bundles
rejected/weekNN_YYYYMMDD/scene-slug/  # Archived rejected assets
```

Assets follow a consistent naming convention (`{slug}-base.png`, `{slug}-var1.png`, `{slug}-metadata.json`) and are organized by ISO week for batch production tracking.
