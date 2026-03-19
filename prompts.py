"""Prompt templates for the error analysis workflow."""

from __future__ import annotations


SYSTEM_INSTRUCTIONS = """
You are an expert Python debugging assistant.
Your job is to explain coding errors in simple language and provide practical fixes.

Return only valid JSON with exactly these keys:
- explanation
- root_cause
- fix
- improved_code

Rules:
- Keep the explanation beginner-friendly.
- Be specific about what likely caused the error.
- Suggest an actionable fix.
- Return improved_code as a complete corrected snippet when possible.
- If the code snippet is incomplete, still provide the best possible corrected version.
- Do not include markdown fences.
""".strip()


def build_analysis_prompt(error_text: str, code_text: str) -> str:
    """Build the prompt sent to the Gemini model."""
    return f"""
{SYSTEM_INSTRUCTIONS}

Analyze the following Python error and code snippet.

Error Message:
{error_text}

Code Snippet:
{code_text}
""".strip()
