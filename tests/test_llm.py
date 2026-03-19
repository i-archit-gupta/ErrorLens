"""Tests for Gemini integration helpers."""

from __future__ import annotations

import importlib
import sys
import types
import unittest
from unittest.mock import patch


def _load_llm_module():
    """Import llm with lightweight dependency stubs for isolated tests."""
    dotenv_module = types.ModuleType("dotenv")
    dotenv_module.load_dotenv = lambda: None

    google_module = types.ModuleType("google")
    generativeai_module = types.ModuleType("google.generativeai")
    generativeai_module.configure = lambda **_: None
    generativeai_module.GenerativeModel = object
    google_module.generativeai = generativeai_module

    with patch.dict(
        sys.modules,
        {
            "dotenv": dotenv_module,
            "google": google_module,
            "google.generativeai": generativeai_module,
        },
    ):
        sys.modules.pop("llm", None)
        return importlib.import_module("llm")


llm = _load_llm_module()


class ParseJsonResponseTests(unittest.TestCase):
    """Test JSON parsing helpers."""

    def test_parse_json_response_accepts_plain_json(self) -> None:
        result = llm._parse_json_response(
            '{"explanation":"test","root_cause":"cause","fix":"fix","improved_code":"x=1"}'
        )
        self.assertEqual(result["fix"], "fix")

    def test_parse_json_response_accepts_fenced_json(self) -> None:
        result = llm._parse_json_response(
            """```json
{"explanation":"test","root_cause":"cause","fix":"fix","improved_code":"x=1"}
```"""
        )
        self.assertEqual(result["root_cause"], "cause")

    def test_parse_json_response_rejects_invalid_json(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "invalid JSON"):
            llm._parse_json_response("not valid json")

    def test_parse_json_response_rejects_non_object_json(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "not a JSON object"):
            llm._parse_json_response('["not", "an", "object"]')


class AnalyzeErrorTests(unittest.TestCase):
    """Test the main analysis flow with mocks."""

    def test_analyze_error_requires_api_key(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaisesRegex(ValueError, "Missing GEMINI_API_KEY"):
                llm.analyze_error("TypeError", "print('hi')")

    def test_analyze_error_returns_formatted_response(self) -> None:
        fake_response = types.SimpleNamespace(
            text=(
                '{"explanation":"  It failed. ","root_cause":" bad type ",'
                '"fix":" convert it ","improved_code":" print(str(age)) "}'
            )
        )
        fake_model = types.SimpleNamespace(generate_content=lambda prompt: fake_response)

        with patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"}, clear=True):
            with patch.object(llm.genai, "configure") as mock_configure:
                with patch.object(llm.genai, "GenerativeModel", return_value=fake_model):
                    result = llm.analyze_error(
                        "TypeError: unsupported operand type(s)",
                        'message = "Age: " + age',
                    )

        mock_configure.assert_called_once_with(api_key="test-key")
        self.assertEqual(result["explanation"], "It failed.")
        self.assertEqual(result["root_cause"], "bad type")
        self.assertEqual(result["fix"], "convert it")
        self.assertEqual(result["improved_code"], "print(str(age))")

    def test_analyze_error_raises_when_model_returns_empty_text(self) -> None:
        fake_response = types.SimpleNamespace(text="   ")
        fake_model = types.SimpleNamespace(generate_content=lambda prompt: fake_response)

        with patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"}, clear=True):
            with patch.object(llm.genai, "configure"):
                with patch.object(llm.genai, "GenerativeModel", return_value=fake_model):
                    with self.assertRaisesRegex(RuntimeError, "empty response"):
                        llm.analyze_error("ValueError", "raise ValueError")


if __name__ == "__main__":
    unittest.main()
