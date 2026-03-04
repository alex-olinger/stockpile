"""Tests for pipeline.workflow.review — approve/reject flow with mocked input()."""

import json
import pytest
from pipeline.workflow.review import review_assets, review_metadata, ask_regenerate


def test_review_assets_all_approved(tmp_path, monkeypatch):
    """When user approves all, should return all paths in approved list."""
    (tmp_path / "test-base.png").write_bytes(b"fake")
    (tmp_path / "test-var1.png").write_bytes(b"fake")

    inputs = iter(["a", "a"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr("subprocess.Popen", lambda *a, **kw: None)

    approved, rejected = review_assets(tmp_path, "image")
    assert len(approved) == 2
    assert len(rejected) == 0


def test_review_assets_some_rejected(tmp_path, monkeypatch):
    """Should correctly split files into approved and rejected lists."""
    (tmp_path / "test-base.png").write_bytes(b"fake")
    (tmp_path / "test-var1.png").write_bytes(b"fake")

    inputs = iter(["a", "r"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr("subprocess.Popen", lambda *a, **kw: None)

    approved, rejected = review_assets(tmp_path, "image")
    assert len(approved) == 1
    assert len(rejected) == 1


def test_review_metadata_approved(tmp_path, monkeypatch):
    """Should return True when user approves metadata."""
    meta_path = tmp_path / "test-metadata.json"
    meta_path.write_text(json.dumps({"title": "Test", "keywords": ["a"]}))

    monkeypatch.setattr("builtins.input", lambda _: "a")

    result = review_metadata(meta_path)
    assert result is True


def test_ask_regenerate_specific(monkeypatch):
    """Should return 'specific' when user chooses S."""
    monkeypatch.setattr("builtins.input", lambda _: "s")
    assert ask_regenerate() == "specific"


def test_ask_regenerate_batch(monkeypatch):
    """Should return 'batch' when user chooses B."""
    monkeypatch.setattr("builtins.input", lambda _: "b")
    assert ask_regenerate() == "batch"
