"""Tests for pipeline.workflow.prompt_gen — past-prompt scanning, prompt saving."""

import pytest
from pathlib import Path
from pipeline.workflow.prompt_gen import load_past_prompts, create_prompts, save_prompts


def test_load_past_prompts_empty_dir(tmp_project):
    """Should return empty list when no prompt files exist."""
    result = load_past_prompts(tmp_project / "content" / "images")
    pytest.skip("Stub — implementation pending")


def test_load_past_prompts_finds_txt_files(tmp_project):
    """Should find and read all *-prompt.txt files across week directories."""
    pytest.skip("Stub — implementation pending")


def test_create_prompts_dry_run():
    """Dry-run should return placeholder prompts dict with 'base' and variation keys."""
    pytest.skip("Stub — implementation pending")


def test_save_prompts_creates_files(tmp_path):
    """Should write .txt files to base/ and variations/ directories."""
    pytest.skip("Stub — implementation pending")
