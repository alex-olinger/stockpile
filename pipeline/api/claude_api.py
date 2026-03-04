"""Claude API integrations — prompts, metadata, video prompts, slug generation.

All functions that call the Anthropic Claude API live here.
Uses the anthropic SDK. Model is configurable via config.CLAUDE_MODEL.
"""

import base64
import json
from pathlib import Path

import anthropic

from pipeline.config import ANTHROPIC_API_KEY, CLAUDE_MODEL


def generate_prompts(system_prompt: str, user_prompt: str, dry_run: bool = False) -> str:
    """Call Claude to generate image prompts.

    Args:
        system_prompt: System instructions including style guidance and past prompts.
        user_prompt: User message with theme, location, and variation count.
        dry_run: If True, return hardcoded placeholder prompts.

    Returns:
        Raw text response containing base prompt and variation prompts.
    """
    if dry_run:
        return (
            "BASE: A serene wellness studio with soft natural lighting, "
            "clean minimalist interior, warm earth tones, photorealistic 1920x1080\n"
            "VAR1: Same scene with morning golden hour light streaming through windows\n"
            "VAR2: Same scene from a wider angle showing the full room layout"
        )

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=2048,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return message.content[0].text


def generate_metadata_from_image(
    image_path: Path, prompt: str, theme: str, dry_run: bool = False
) -> dict:
    """Call Claude with vision to generate metadata for an image.

    Args:
        image_path: Path to the image file.
        prompt: The prompt used to generate the image.
        theme: Content category (e.g. 'wellness', 'business').
        dry_run: If True, return placeholder metadata dict.

    Returns:
        Metadata dict with keys: title, description, keywords, category,
        editorial, ai_generated.
    """
    if dry_run:
        return {
            "title": f"Stock {theme.title()} Image",
            "description": f"A professional {theme} scene for stock photography.",
            "keywords": [theme, "stock", "professional", "high-quality", "commercial"],
            "category": theme,
            "editorial": False,
            "ai_generated": True,
        }

    image_data = base64.b64encode(image_path.read_bytes()).decode()
    media_type = "image/png"

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {"type": "base64", "media_type": media_type, "data": image_data},
                },
                {
                    "type": "text",
                    "text": (
                        f"Generate stock photo metadata for this image.\n"
                        f"Original prompt: {prompt}\nTheme: {theme}\n\n"
                        f"Return a JSON object with these exact keys:\n"
                        f"- title: descriptive title\n"
                        f"- description: 1-2 sentence description\n"
                        f"- keywords: array of 25-50 relevant keywords\n"
                        f"- category: content category\n"
                        f"- editorial: boolean (false for stock)\n"
                        f"- ai_generated: true\n\n"
                        f"Return ONLY the JSON, no markdown fences."
                    ),
                },
            ],
        }],
    )
    return json.loads(message.content[0].text)


def generate_video_prompt_from_image(
    image_path: Path, dry_run: bool = False
) -> str:
    """Call Claude with vision to generate an image-to-video prompt.

    Args:
        image_path: Path to the approved image.
        dry_run: If True, return placeholder video prompt string.

    Returns:
        Video prompt string describing subtle loopable motion, 10s duration.
    """
    if dry_run:
        return "Slow gentle camera drift across the scene."

    image_data = base64.b64encode(image_path.read_bytes()).decode()
    media_type = "image/png"

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=512,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {"type": "base64", "media_type": media_type, "data": image_data},
                },
                {
                    "type": "text",
                    "text": (
                        "Generate a video motion prompt for this image. "
                        "The video should be 10 seconds, with subtle loopable motion. "
                        "Keep the same camera angle. Describe gentle, natural movement "
                        "suitable for stock video. Return ONLY the prompt text."
                    ),
                },
            ],
        }],
    )
    return message.content[0].text


def generate_scene_slug(theme: str, location: str, dry_run: bool = False) -> str:
    """Call Claude to generate a descriptive scene slug from theme and location.

    Args:
        theme: Content theme (e.g. 'wellness', 'food').
        location: Scene location (e.g. 'indoor', 'outdoor', 'studio').
        dry_run: If True, return a placeholder slug.

    Returns:
        Kebab-case slug string (e.g. 'morning-yoga-routine-indoor').
    """
    if dry_run:
        return f"{theme}-{location}"

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=64,
        messages=[{
            "role": "user",
            "content": (
                f"Generate a descriptive 4-6 word kebab-case slug for a stock photo scene.\n"
                f"Theme: {theme}\nLocation: {location}\n\n"
                f"Return ONLY the slug, nothing else. Example: morning-yoga-routine-studio"
            ),
        }],
    )
    return message.content[0].text.strip()
