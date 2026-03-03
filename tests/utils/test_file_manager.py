"""Tests for pipeline.utils.file_manager — directory creation, uniqueness, structure."""

import pytest
from pipeline.utils.file_manager import create_week_dirs, create_scene_dirs, move_to_rejected


def test_create_week_dirs_creates_both(tmp_project, monkeypatch):
    """Should create matching week dirs under both images/ and videos/."""
    pytest.skip("Stub — implementation pending")


def test_create_week_dirs_errors_if_exists(tmp_project, monkeypatch):
    """Should raise FileExistsError if week directory already exists."""
    pytest.skip("Stub — implementation pending")


def test_create_scene_dirs_creates_subdirs(tmp_path):
    """Should create base/, variations/, exports/ under the scene directory."""
    pytest.skip("Stub — implementation pending")


def test_move_to_rejected(tmp_project):
    """Should move file to rejected/weekNN/scene-slug/ directory."""
    pytest.skip("Stub — implementation pending")
