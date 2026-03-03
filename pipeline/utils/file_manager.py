"""File management — directory creation, naming conventions, file operations."""

from pathlib import Path


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
    pass


def create_scene_dirs(week_path: Path, scene_slug: str) -> Path:
    """Create scene subdirectories (base/, variations/, exports/) under a week folder.

    Args:
        week_path: Path to the week directory (e.g. content/images/week01_20260303/).
        scene_slug: Scene slug for the subdirectory name.

    Returns:
        Path to the created scene directory.
    """
    pass


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
    pass
