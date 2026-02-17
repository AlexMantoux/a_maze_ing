"""Shared typing helpers for configuration values."""

from __future__ import annotations

from collections.abc import Mapping

MazeConfig = Mapping[str, int | tuple[int, int] | str | bool]
