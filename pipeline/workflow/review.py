"""User review flow — approve/reject assets, handle regeneration decisions."""

import json
import subprocess
import sys
from pathlib import Path


def review_assets(asset_dir: Path, asset_type: str = "image") -> tuple[list[Path], list[Path]]:
    """Open file explorer and prompt the user to approve/reject each asset.

    Args:
        asset_dir: Directory containing the assets to review.
        asset_type: 'image' or 'video' — affects display messaging.

    Returns:
        Tuple of (approved_paths, rejected_paths).
    """
    # Open file explorer on Windows
    if sys.platform == "win32":
        subprocess.Popen(["explorer", str(asset_dir)])

    approved = []
    rejected = []

    extensions = {".png", ".jpg", ".jpeg"} if asset_type == "image" else {".mp4", ".mov"}
    files = sorted(f for f in asset_dir.iterdir() if f.suffix.lower() in extensions)

    if not files:
        print(f"No {asset_type} files found in {asset_dir}")
        return approved, rejected

    print(f"\nReviewing {len(files)} {asset_type}(s):")
    for file_path in files:
        while True:
            choice = input(f"  {file_path.name} — [A]pprove / [R]eject: ").strip().lower()
            if choice in ("a", "approve"):
                approved.append(file_path)
                break
            elif choice in ("r", "reject"):
                rejected.append(file_path)
                break
            print("    Please enter 'A' or 'R'.")

    print(f"\n  Approved: {len(approved)}, Rejected: {len(rejected)}")
    return approved, rejected


def review_metadata(metadata_path: Path) -> bool:
    """Display metadata JSON in terminal and allow inline edits.

    Args:
        metadata_path: Path to the metadata JSON file.

    Returns:
        True if approved, False if rejected.
    """
    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    print(f"\n=== Metadata: {metadata_path.name} ===")
    print(json.dumps(metadata, indent=2))

    while True:
        choice = input("\n[A]pprove / [E]dit / [R]eject: ").strip().lower()
        if choice in ("a", "approve"):
            return True
        elif choice in ("r", "reject"):
            return False
        elif choice in ("e", "edit"):
            field = input("  Field to edit (title/description/keywords): ").strip().lower()
            if field in metadata:
                new_val = input(f"  New {field}: ").strip()
                if field == "keywords":
                    metadata[field] = [k.strip() for k in new_val.split(",")]
                else:
                    metadata[field] = new_val
                with open(metadata_path, "w", encoding="utf-8") as f:
                    json.dump(metadata, f, indent=2)
                print(f"  Updated {field}.")
            else:
                print(f"  Unknown field: {field}")
        else:
            print("  Please enter 'A', 'E', or 'R'.")


def ask_regenerate() -> str:
    """Prompt user whether to regenerate specific images or the entire batch.

    Returns:
        'specific' or 'batch'.
    """
    while True:
        choice = input("Regenerate [S]pecific images or entire [B]atch? ").strip().lower()
        if choice in ("s", "specific"):
            return "specific"
        elif choice in ("b", "batch"):
            return "batch"
        print("  Please enter 'S' or 'B'.")
