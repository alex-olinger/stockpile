"""Main menu + Image/Video mode orchestration.

Two separate modes selectable from a main menu:
- Image Mode (I1-I6): scene setup through image packaging
- Video Mode (V1-V5): scene selection through video packaging

Uses input() for all user prompts. Handles KeyboardInterrupt:
- During a mode → return to main menu
- At main menu → exit program
Passes dry_run boolean to all module functions that make API calls.
"""

import argparse
import datetime
import shutil
from pathlib import Path

from pipeline.config import (
    BASE_DIR, IMAGE_DIR, VIDEO_DIR, OUTPUT_DIR, REJECTED_DIR, load_env,
)
from pipeline.utils.pricing import display_pricing
from pipeline.utils.file_manager import create_week_dirs, create_scene_dirs, move_to_rejected
from pipeline.workflow.prompt_gen import load_past_prompts, create_prompts, save_prompts
from pipeline.workflow.image_gen import generate_scene_images
from pipeline.workflow.video_gen import generate_scene_videos
from pipeline.workflow.metadata_gen import (
    create_metadata,
    create_video_prompts,
    save_metadata,
    copy_metadata_to_video,
)
from pipeline.workflow.review import review_assets, review_metadata, ask_regenerate
from pipeline.workflow.packaging import package_approved
from pipeline.api.claude_api import generate_scene_slug


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments. Returns namespace with dry_run bool."""
    parser = argparse.ArgumentParser(description="Stockpile — AI stock content pipeline")
    parser.add_argument("--dry-run", action="store_true", help="Run without API calls")
    return parser.parse_args()


def select_week() -> tuple[Path, Path, str]:
    """Prompt for week number, create/verify week dirs, return week paths.

    Returns:
        Tuple of (image_week_path, video_week_path, week_folder_name).
    """
    year = datetime.date.today().year
    week_num = int(input(f"Which week number is this content for? (1-53, year {year}): "))
    image_week, video_week = create_week_dirs(week_num, year)
    print(f"Created week directories: {image_week.name}")
    return image_week, video_week, image_week.name


def run_image_mode(week_path: Path, dry_run: bool) -> None:
    """Image generation pipeline (Steps I1-I6).

    I1: Scene setup (theme, location, counts, slug, dirs)
    I2: Prompt generation
    I3: Image generation
    I4: Image review
    I5: Metadata generation
    I6: Metadata review + packaging
    """
    week_image_dir = IMAGE_DIR / week_path
    week_video_dir = VIDEO_DIR / week_path

    # I1: Scene setup
    print("\n=== I1: Scene Setup ===")
    theme = input("Theme (business/wellness/beauty/food/technology/nature/lifestyle): ").strip()
    location = input("Location (indoor/outdoor/studio/office/gym/kitchen): ").strip()
    num_base = int(input("How many base images? [1]: ").strip() or "1")
    num_variations = int(input("How many variations per base? [2]: ").strip() or "2")

    slug = generate_scene_slug(theme, location, dry_run=dry_run)
    print(f"Scene slug: {slug}")

    scene_image_dir = create_scene_dirs(week_image_dir, slug)
    create_scene_dirs(week_video_dir, slug)

    # I2: Prompt generation
    print("\n=== I2: Prompt Generation ===")
    past_prompts = load_past_prompts(IMAGE_DIR)
    prompts = create_prompts(theme, location, num_variations, past_prompts, dry_run=dry_run)
    prompt_paths = save_prompts(prompts, scene_image_dir, slug)
    print(f"Saved {len(prompt_paths)} prompt files")

    # I3: Image generation
    print("\n=== I3: Image Generation ===")
    image_paths = generate_scene_images(prompts, scene_image_dir, slug, dry_run=dry_run)

    # I4: Image review
    print("\n=== I4: Image Review ===")
    approved_images, rejected_images = review_assets(scene_image_dir / "base", "image")
    approved_vars, rejected_vars = review_assets(scene_image_dir / "variations", "image")

    approved_all = approved_images + approved_vars
    rejected_all = rejected_images + rejected_vars

    for rej in rejected_all:
        move_to_rejected(rej, REJECTED_DIR, week_path, slug)

    if rejected_all:
        choice = ask_regenerate()
        if choice == "batch":
            print("Batch regeneration not yet implemented — continuing with approved images.")

    # Copy approved images to exports
    for img in approved_all:
        dest = scene_image_dir / "exports" / img.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(img), str(dest))

    # Build approved image_paths dict for metadata
    approved_image_paths = {}
    for key, path in image_paths.items():
        if path in approved_all:
            approved_image_paths[key] = path

    if not approved_image_paths:
        print("No approved images. Returning to menu.")
        return

    # I5: Metadata generation
    print("\n=== I5: Metadata Generation ===")
    # Generate metadata for the first approved image (representative)
    first_key = next(iter(approved_image_paths))
    first_path = approved_image_paths[first_key]
    first_prompt = prompts.get(first_key, "")
    metadata = create_metadata(first_path, first_prompt, theme, dry_run=dry_run)
    metadata_path = scene_image_dir / "exports" / f"{slug}-metadata.json"
    save_metadata(metadata, metadata_path)
    print(f"Saved metadata: {metadata_path.name}")

    # I6: Metadata review + packaging
    print("\n=== I6: Metadata Review + Packaging ===")
    if review_metadata(metadata_path):
        output_dir = package_approved(week_image_dir, week_video_dir, slug, OUTPUT_DIR)
        print(f"Packaged to: {output_dir}")
    else:
        print("Metadata rejected. Returning to menu.")


def run_video_mode(week_path: Path, dry_run: bool) -> None:
    """Video generation pipeline (Steps V1-V5).

    V1: Scene selection (list existing image scenes)
    V2: Video prompt generation
    V3: Video generation
    V4: Video review
    V5: Packaging
    """
    week_image_dir = IMAGE_DIR / week_path
    week_video_dir = VIDEO_DIR / week_path

    # V1: Scene selection
    print("\n=== V1: Scene Selection ===")
    scenes = []
    if week_image_dir.exists():
        for d in sorted(week_image_dir.iterdir()):
            if d.is_dir():
                # Check for approved images (exports dir with files)
                exports = d / "exports"
                if exports.exists() and any(exports.iterdir()):
                    scenes.append(d.name)

    if not scenes:
        print("No scenes with approved images found for this week.")
        return

    print("Available scenes:")
    for i, scene in enumerate(scenes, 1):
        print(f"  {i}. {scene}")
    print(f"  0. Cancel")

    choice = int(input("Select scene number: ").strip())
    if choice == 0:
        return
    slug = scenes[choice - 1]

    scene_image_dir = week_image_dir / slug
    scene_video_dir = week_video_dir / slug
    create_scene_dirs(week_video_dir, slug)

    # Gather approved images from exports
    image_exports = scene_image_dir / "exports"
    approved_image_paths = {}
    for f in sorted(image_exports.iterdir()):
        if f.suffix.lower() in (".png", ".jpg", ".jpeg"):
            if "-base" in f.stem:
                approved_image_paths["base"] = f
            elif "-var" in f.stem:
                # Extract var key from filename like "slug-var1.png"
                parts = f.stem.split("-")
                for p in parts:
                    if p.startswith("var"):
                        approved_image_paths[p] = f
                        break

    if not approved_image_paths:
        print("No approved images found in exports.")
        return

    # V2: Video prompt generation
    print("\n=== V2: Video Prompt Generation ===")
    video_prompts = create_video_prompts(approved_image_paths, dry_run=dry_run)
    for key, prompt in video_prompts.items():
        prompt_path = scene_video_dir / "base" / f"{slug}-{key}-video-prompt.txt"
        if key != "base":
            prompt_path = scene_video_dir / "variations" / f"{slug}-{key}-video-prompt.txt"
        prompt_path.parent.mkdir(parents=True, exist_ok=True)
        prompt_path.write_text(prompt, encoding="utf-8")
    print(f"Generated {len(video_prompts)} video prompts")

    # V3: Video generation
    print("\n=== V3: Video Generation ===")
    video_paths = generate_scene_videos(
        approved_image_paths, video_prompts, scene_video_dir, slug, dry_run=dry_run
    )

    if dry_run:
        print("[DRY-RUN] Skipping video review and packaging.")
        return

    # V4: Video review
    print("\n=== V4: Video Review ===")
    approved_vids, rejected_vids = review_assets(scene_video_dir / "base", "video")
    approved_var_vids, rejected_var_vids = review_assets(scene_video_dir / "variations", "video")

    all_approved = approved_vids + approved_var_vids
    all_rejected = rejected_vids + rejected_var_vids

    for rej in all_rejected:
        move_to_rejected(rej, REJECTED_DIR, week_path, slug)

    # Copy approved videos to exports
    for vid in all_approved:
        dest = scene_video_dir / "exports" / vid.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(vid), str(dest))

    # Copy metadata to video exports if it exists
    img_metadata = scene_image_dir / "exports" / f"{slug}-metadata.json"
    if img_metadata.exists():
        copy_metadata_to_video(img_metadata, scene_video_dir / "exports")

    # V5: Packaging
    print("\n=== V5: Packaging ===")
    output_dir = package_approved(week_image_dir, week_video_dir, slug, OUTPUT_DIR)
    print(f"Packaged to: {output_dir}")


def main() -> None:
    """Main menu loop.

    Startup: parse args, load env, display pricing.
    Menu: [W]eek select, [I]mage mode, [V]ideo mode, [Q]uit.
    KeyboardInterrupt during mode → return to menu.
    KeyboardInterrupt at menu → exit.
    """
    args = parse_args()
    load_env()
    display_pricing()

    week_path = None  # Will be set by select_week

    try:
        while True:
            print("\n=== Stockpile Main Menu ===")
            if week_path:
                print(f"  Active week: {week_path}")
            else:
                print("  No week selected")
            print("  [W] Select/change week")
            print("  [I] Image generation mode")
            print("  [V] Video generation mode")
            print("  [Q] Quit")

            choice = input("\nChoice: ").strip().lower()

            if choice in ("q", "quit"):
                print("Goodbye!")
                break
            elif choice in ("w", "week"):
                try:
                    _, _, week_path = select_week()
                except FileExistsError as e:
                    print(f"Error: {e}")
                except ValueError as e:
                    print(f"Invalid input: {e}")
            elif choice in ("i", "image"):
                if not week_path:
                    print("Please select a week first ([W]).")
                    continue
                try:
                    run_image_mode(week_path, args.dry_run)
                except KeyboardInterrupt:
                    print("\n\nReturning to main menu...")
            elif choice in ("v", "video"):
                if not week_path:
                    print("Please select a week first ([W]).")
                    continue
                try:
                    run_video_mode(week_path, args.dry_run)
                except KeyboardInterrupt:
                    print("\n\nReturning to main menu...")
            else:
                print("Invalid choice. Please enter W, I, V, or Q.")
    except KeyboardInterrupt:
        print("\n\nExiting Stockpile.")
