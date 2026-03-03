"""Claude API integrations — prompts, metadata, video prompts, slug generation.

All functions that call the Anthropic Claude API live here.
Uses the anthropic SDK. Model is configurable via config.CLAUDE_MODEL.
"""

from pathlib import Path


def generate_prompts(system_prompt: str, user_prompt: str, dry_run: bool = False) -> str:
    """Call Claude to generate image prompts.

    Args:
        system_prompt: System instructions including style guidance and past prompts.
        user_prompt: User message with theme, location, and variation count.
        dry_run: If True, return hardcoded placeholder prompts.

    Returns:
        Raw text response containing base prompt and variation prompts.
    """
    pass


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
    pass


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
    pass


def generate_scene_slug(theme: str, location: str, dry_run: bool = False) -> str:
    """Call Claude to generate a descriptive scene slug from theme and location.

    Args:
        theme: Content theme (e.g. 'wellness', 'food').
        location: Scene location (e.g. 'indoor', 'outdoor', 'studio').
        dry_run: If True, return a placeholder slug.

    Returns:
        Kebab-case slug string (e.g. 'morning-yoga-routine-indoor').
    """
    pass
