"""Tests for pipeline.workflow.prompt_gen — past-prompt scanning, prompt saving."""

import pytest
from pathlib import Path
from pipeline.workflow.prompt_gen import load_past_prompts, create_prompts, save_prompts


def test_load_past_prompts_empty_dir(tmp_project):
    """Should return empty list when no prompt files exist."""
    result = load_past_prompts(tmp_project / "content" / "images")
    assert result == []


def test_load_past_prompts_finds_txt_files(tmp_project):
    """Should find and read all *-prompt.txt files across week directories."""
    images_dir = tmp_project / "content" / "images"
    week_dir = images_dir / "week01_20260105" / "test-scene" / "base"
    week_dir.mkdir(parents=True)
    (week_dir / "test-scene-base-prompt.txt").write_text("A test prompt")
    (week_dir / "test-scene-var1-prompt.txt").write_text("A variation prompt")

    result = load_past_prompts(images_dir)
    assert len(result) == 2
    assert "A test prompt" in result


def test_create_prompts_dry_run():
    """Dry-run should return placeholder prompts dict with 'base' and variation keys."""
    result = create_prompts("wellness", "studio", 2, [], dry_run=True)
    assert "base" in result
    assert isinstance(result["base"], str)
    assert len(result) >= 2


def test_save_prompts_creates_files(tmp_path):
    """Should write .txt files to base/ and variations/ directories."""
    scene_dir = tmp_path / "test-scene"
    (scene_dir / "base").mkdir(parents=True)
    (scene_dir / "variations").mkdir(parents=True)

    prompts = {"base": "A base prompt", "var1": "A variation prompt"}
    paths = save_prompts(prompts, scene_dir, "test-scene")

    assert paths["base"].exists()
    assert paths["var1"].exists()
    assert paths["base"].read_text() == "A base prompt"
    assert "base" in str(paths["base"])
    assert "variations" in str(paths["var1"])
