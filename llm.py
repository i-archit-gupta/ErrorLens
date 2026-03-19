"""LLM integration for Gemini-based error analysis."""

from __future__ import annotations

import json
import os
from typing import Any, Dict

from dotenv import load_dotenv
import google.generativeai as genai

from prompts import build_analysis_prompt
from utils import format_llm_response


load_dotenv()


def analyze_error(error_text: str, code_text: str) -> Dict[str, str]:
    """Analyze an error and return structured guidance."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "Missing GEMINI_API_KEY. Add it to your environment or .env file."
        )

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-flash-lite-latest")
    prompt = build_analysis_prompt(error_text=error_text, code_text=code_text)

    try:
        response = model.generate_content(prompt)
        raw_text = getattr(response, "text", "").strip()
        if not raw_text:
            raise RuntimeError("The model returned an empty response.")

        parsed_response = _parse_json_response(raw_text)
        return format_llm_response(parsed_response)
    except Exception as exc:
        raise RuntimeError(str(exc)) from exc


def _parse_json_response(raw_text: str) -> Dict[str, Any]:
    """Parse JSON from the model response, including fenced JSON blocks."""
    cleaned_text = raw_text.strip()

    if cleaned_text.startswith("```"):
        cleaned_text = cleaned_text.removeprefix("```json").removeprefix("```")
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3]
        cleaned_text = cleaned_text.strip()

    try:
        data = json.loads(cleaned_text)
    except json.JSONDecodeError as exc:
        raise RuntimeError("The model returned invalid JSON.") from exc

    if not isinstance(data, dict):
        raise RuntimeError("The model response format was not a JSON object.")

    return data
