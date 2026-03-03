"""Prompt generation — load past prompts, generate new prompts via Claude, save to files."""

from pathlib import Path


def load_past_prompts(images_base_dir: Path) -> list[str]:
    """Scan all *-prompt.txt files from all week directories to collect past prompts.

    Args:
        images_base_dir: The content/images/ directory to scan recursively.

    Returns:
        List of prompt strings from all previous weeks.
    """
    pass


def create_prompts(
    theme: str,
    location: str,
    num_variations: int,
    past_prompts: list[str],
    dry_run: bool = False,
) -> dict[str, str]:
    """Generate base + variation prompts via Claude API.

    Calls api/claude_api.generate_prompts with theme, location, stock
    photography best practices, and past prompts as "avoid these".

    Args:
        theme: Content theme (e.g. 'wellness').
        location: Scene location (e.g. 'indoor').
        num_variations: Number of variation prompts to generate.
        past_prompts: Previously used prompts to avoid similarity.
        dry_run: If True, returns hardcoded placeholder prompts.

    Returns:
        Dict with 'base' key and 'var1', 'var2', ... keys mapping to prompt strings.
    """
    pass


def save_prompts(prompts: dict[str, str], scene_dir: Path, scene_slug: str) -> dict[str, Path]:
    """Write prompt strings to .txt files in the correct directories.

    Base prompt → scene_dir/base/{slug}-base-prompt.txt
    Variation prompts → scene_dir/variations/{slug}-var{N}-prompt.txt

    Args:
        prompts: Dict from create_prompts ('base', 'var1', ...).
        scene_dir: Path to the scene directory under the week folder.
        scene_slug: Scene slug for file naming.

    Returns:
        Dict mapping prompt keys to their saved file paths.
    """
    pass
