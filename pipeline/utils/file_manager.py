"""File management — directory creation, naming conventions, file operations."""

import datetime
import shutil
from pathlib import Path

from pipeline.config import IMAGE_DIR, VIDEO_DIR


def create_week_dirs(week_num: int, year: int) -> tuple[Path, Path]:
    """Create weekNN_YYYYMMDD directories under both images/ and videos/.

    Calculates the Monday date for the given ISO week number in the given year.
    Errors if the week directory already exists.

    Args:
        week_num: ISO week number (1-53).
        year: Four-digit year.

    Returns:
        Tuple of (image_week_path, video_week_path).

    Raises:
        FileExistsError: If the week directory already exists.
    """
    monday = datetime.date.fromisocalendar(year, week_num, 1)
    folder_name = f"week{week_num:02d}_{monday.strftime('%Y%m%d')}"

    image_week = IMAGE_DIR / folder_name
    video_week = VIDEO_DIR / folder_name

    if image_week.exists() or video_week.exists():
        raise FileExistsError(f"Week directory already exists: {folder_name}")

    image_week.mkdir(parents=True, exist_ok=True)
    video_week.mkdir(parents=True, exist_ok=True)

    return image_week, video_week


def create_scene_dirs(week_path: Path, scene_slug: str) -> Path:
    """Create scene subdirectories (base/, variations/, exports/) under a week folder.

    Args:
        week_path: Path to the week directory (e.g. content/images/week01_20260303/).
        scene_slug: Scene slug for the subdirectory name.

    Returns:
        Path to the created scene directory.
    """
    scene_dir = week_path / scene_slug
    for subdir in ["base", "variations", "exports"]:
        (scene_dir / subdir).mkdir(parents=True, exist_ok=True)
    return scene_dir


def move_to_rejected(
    file_path: Path, rejected_base: Path, week_folder: str, scene_slug: str
) -> Path:
    """Move a rejected file to the rejected/ directory structure.

    Args:
        file_path: Path to the file being rejected.
        rejected_base: Base rejected/ directory path.
        week_folder: Week folder name (e.g. 'week01_20260303').
        scene_slug: Scene slug for organizing rejected files.

    Returns:
        Path to the file in its new rejected location.
    """
    target_dir = rejected_base / week_folder / scene_slug
    target_dir.mkdir(parents=True, exist_ok=True)
    dest = target_dir / file_path.name
    shutil.move(str(file_path), str(dest))
    return dest
