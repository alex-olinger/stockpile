"""Prompt generation — load past prompts, generate new prompts via Claude, save to files."""

from pathlib import Path

from pipeline.api.claude_api import generate_prompts


def load_past_prompts(images_base_dir: Path) -> list[str]:
    """Scan all *-prompt.txt files from all week directories to collect past prompts.

    Args:
        images_base_dir: The content/images/ directory to scan recursively.

    Returns:
        List of prompt strings from all previous weeks.
    """
    prompts = []
    for prompt_file in sorted(images_base_dir.rglob("*-prompt.txt")):
        prompts.append(prompt_file.read_text(encoding="utf-8").strip())
    return prompts


def create_prompts(
    theme: str,
    location: str,
    num_variations: int,
    past_prompts: list[str],
    dry_run: bool = False,
) -> dict[str, str]:
    """Generate base + variation prompts via Claude API.

    Args:
        theme: Content theme (e.g. 'wellness').
        location: Scene location (e.g. 'indoor').
        num_variations: Number of variation prompts to generate.
        past_prompts: Previously used prompts to avoid similarity.
        dry_run: If True, returns hardcoded placeholder prompts.

    Returns:
        Dict with 'base' key and 'var1', 'var2', ... keys mapping to prompt strings.
    """
    past_context = ""
    if past_prompts:
        past_context = "\n\nAvoid similarity to these past prompts:\n" + "\n".join(
            f"- {p}" for p in past_prompts
        )

    system_prompt = (
        "You are a stock photography prompt generator. Generate photorealistic, "
        "clean composition, soft natural lighting, stock-friendly image prompts at 1920x1080. "
        "Output format: BASE: <prompt>\\nVAR1: <prompt>\\nVAR2: <prompt> etc."
        f"{past_context}"
    )
    user_prompt = (
        f"Theme: {theme}\nLocation: {location}\n"
        f"Generate 1 base prompt and {num_variations} variation prompts."
    )

    raw = generate_prompts(system_prompt, user_prompt, dry_run=dry_run)

    result = {}
    for line in raw.strip().splitlines():
        line = line.strip()
        if line.startswith("BASE:"):
            result["base"] = line[len("BASE:"):].strip()
        elif line.startswith("VAR"):
            # Extract key like "var1" from "VAR1:"
            colon_idx = line.index(":")
            key = line[:colon_idx].strip().lower()
            result[key] = line[colon_idx + 1:].strip()
    return result


def save_prompts(prompts: dict[str, str], scene_dir: Path, scene_slug: str) -> dict[str, Path]:
    """Write prompt strings to .txt files in the correct directories.

    Base prompt -> scene_dir/base/{slug}-base-prompt.txt
    Variation prompts -> scene_dir/variations/{slug}-var{N}-prompt.txt

    Args:
        prompts: Dict from create_prompts ('base', 'var1', ...).
        scene_dir: Path to the scene directory under the week folder.
        scene_slug: Scene slug for file naming.

    Returns:
        Dict mapping prompt keys to their saved file paths.
    """
    paths = {}
    for key, text in prompts.items():
        if key == "base":
            path = scene_dir / "base" / f"{scene_slug}-base-prompt.txt"
        else:
            path = scene_dir / "variations" / f"{scene_slug}-{key}-prompt.txt"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        paths[key] = path
    return paths
