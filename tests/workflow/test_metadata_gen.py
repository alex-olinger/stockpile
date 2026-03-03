"""Tests for pipeline.workflow.metadata_gen — metadata dict structure, JSON save/copy."""

import pytest
import json
from pathlib import Path
from pipeline.workflow.metadata_gen import create_metadata, save_metadata, copy_metadata_to_video


def test_create_metadata_dry_run(tmp_path):
    """Dry-run should return placeholder metadata with required keys."""
    pytest.skip("Stub — implementation pending")


def test_save_metadata_writes_json(tmp_path):
    """Should write a valid JSON file at the given path."""
    pytest.skip("Stub — implementation pending")


def test_copy_metadata_to_video(tmp_path):
    """Should copy metadata JSON from image dir to video dir."""
    pytest.skip("Stub — implementation pending")


def test_metadata_has_required_keys():
    """Metadata dict should contain title, description, keywords, category, editorial, ai_generated."""
    pytest.skip("Stub — implementation pending")
