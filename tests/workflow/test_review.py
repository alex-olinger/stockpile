"""Tests for pipeline.workflow.review — approve/reject flow with mocked input()."""

import pytest
from pipeline.workflow.review import review_assets, review_metadata, ask_regenerate


def test_review_assets_all_approved(tmp_path, monkeypatch):
    """When user approves all, should return all paths in approved list."""
    pytest.skip("Stub — implementation pending")


def test_review_assets_some_rejected(tmp_path, monkeypatch):
    """Should correctly split files into approved and rejected lists."""
    pytest.skip("Stub — implementation pending")


def test_review_metadata_approved(tmp_path, monkeypatch):
    """Should return True when user approves metadata."""
    pytest.skip("Stub — implementation pending")


def test_ask_regenerate_specific(monkeypatch):
    """Should return 'specific' when user chooses S."""
    pytest.skip("Stub — implementation pending")


def test_ask_regenerate_batch(monkeypatch):
    """Should return 'batch' when user chooses B."""
    pytest.skip("Stub — implementation pending")
