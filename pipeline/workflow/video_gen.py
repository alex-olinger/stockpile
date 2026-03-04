"""Video generation orchestration — generates videos from approved images + prompts."""

from pathlib import Path

from pipeline.api.video_api import get_video_provider
from pipeline.config import PRICING


def generate_scene_videos(
    image_paths: dict[str, Path],
    video_prompts: dict[str, str],
    scene_video_dir: Path,
    scene_slug: str,
    dry_run: bool = False,
) -> dict[str, Path]:
    """Orchestrate video generation for a complete scene.

    Args:
        image_paths: Dict mapping keys ('base', 'var1', ...) to image file paths.
        video_prompts: Dict mapping the same keys to video motion prompts.
        scene_video_dir: Path to the scene's video directory.
        scene_slug: Scene slug for file naming.
        dry_run: If True, uses PlaceholderVideoProvider.

    Returns:
        Dict mapping keys to saved video file paths.
    """
    provider = get_video_provider(dry_run=dry_run)
    video_paths = {}

    for key in image_paths:
        if key not in video_prompts:
            continue

        if key == "base":
            output_path = scene_video_dir / "base" / f"{scene_slug}-base.mp4"
        else:
            output_path = scene_video_dir / "variations" / f"{scene_slug}-{key}.mp4"

        output_path.parent.mkdir(parents=True, exist_ok=True)
        provider.generate(image_paths[key], video_prompts[key], output_path)
        video_paths[key] = output_path
        print(f"  Generated {key}: {output_path.name}")

    cost = PRICING["video"]["kling"]["cost_per_video"] * len(video_paths)
    print(f"\nVideo cost: ${cost:.2f} ({len(video_paths)} videos x ${PRICING['video']['kling']['cost_per_video']:.2f})")

    return video_paths
