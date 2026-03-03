"""User review flow — approve/reject assets, handle regeneration decisions."""

from pathlib import Path


def review_assets(asset_dir: Path, asset_type: str = "image") -> tuple[list[Path], list[Path]]:
    """Open file explorer and prompt the user to approve/reject each asset.

    Opens the asset directory in Windows File Explorer, then iterates
    through each file prompting [A]pprove / [R]eject.

    Args:
        asset_dir: Directory containing the assets to review.
        asset_type: 'image' or 'video' — affects display messaging.

    Returns:
        Tuple of (approved_paths, rejected_paths).
    """
    pass


def review_metadata(metadata_path: Path) -> bool:
    """Display metadata JSON in terminal and allow inline edits.

    Shows the metadata content, lets the user edit title, description,
    or keywords, then approve or reject.

    Args:
        metadata_path: Path to the metadata JSON file.

    Returns:
        True if approved, False if rejected.
    """
    pass


def ask_regenerate() -> str:
    """Prompt user whether to regenerate specific images or the entire batch.

    Returns:
        'specific' or 'batch'.
    """
    pass
