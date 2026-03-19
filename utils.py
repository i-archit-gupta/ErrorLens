"""Utility helpers for the app."""

from __future__ import annotations

from typing import Any, Dict


def clean_user_input(text: str) -> str:
    """Trim whitespace and normalize empty values."""
    return text.strip()


def validate_inputs(error_text: str, code_text: str) -> str | None:
    """Validate required user inputs."""
    if not error_text and not code_text:
        return "Please provide both an error message and a code snippet."
    if not error_text:
        return "Please provide an error message."
    if not code_text:
        return "Please provide a code snippet."
    return None


def format_llm_response(data: Dict[str, Any]) -> Dict[str, str]:
    """Normalize the model response into the required sections."""
    return {
        "explanation": _string_value(
            data.get("explanation"),
            default="No explanation was returned.",
        ),
        "root_cause": _string_value(
            data.get("root_cause"),
            default="No root cause was returned.",
        ),
        "fix": _string_value(
            data.get("fix"),
            default="No fix was returned.",
        ),
        "improved_code": _string_value(
            data.get("improved_code"),
            default="# No improved code was returned.",
        ),
    }


def _string_value(value: Any, default: str) -> str:
    """Convert a value to a clean display string."""
    if value is None:
        return default
    text = str(value).strip()
    return text or default
