"""Tests for utility helpers."""

from __future__ import annotations

import unittest

from utils import clean_user_input, format_llm_response, validate_inputs


class CleanUserInputTests(unittest.TestCase):
    """Test input cleanup behavior."""

    def test_clean_user_input_strips_surrounding_whitespace(self) -> None:
        self.assertEqual(clean_user_input("  hello world  \n"), "hello world")


class ValidateInputsTests(unittest.TestCase):
    """Test form validation rules."""

    def test_validate_inputs_requires_both_fields(self) -> None:
        self.assertEqual(
            validate_inputs("", ""),
            "Please provide both an error message and a code snippet.",
        )

    def test_validate_inputs_requires_error_message(self) -> None:
        self.assertEqual(
            validate_inputs("", "print('hi')"),
            "Please provide an error message.",
        )

    def test_validate_inputs_requires_code_snippet(self) -> None:
        self.assertEqual(
            validate_inputs("TypeError", ""),
            "Please provide a code snippet.",
        )

    def test_validate_inputs_accepts_valid_values(self) -> None:
        self.assertIsNone(validate_inputs("TypeError", "print('hi')"))


class FormatLlmResponseTests(unittest.TestCase):
    """Test response formatting and defaults."""

    def test_format_llm_response_returns_trimmed_values(self) -> None:
        result = format_llm_response(
            {
                "explanation": "  Simple explanation.  ",
                "root_cause": "  Bad input type. ",
                "fix": "  Convert to string. ",
                "improved_code": "  print(str(age))  ",
            }
        )

        self.assertEqual(result["explanation"], "Simple explanation.")
        self.assertEqual(result["root_cause"], "Bad input type.")
        self.assertEqual(result["fix"], "Convert to string.")
        self.assertEqual(result["improved_code"], "print(str(age))")

    def test_format_llm_response_uses_defaults_for_missing_values(self) -> None:
        result = format_llm_response({})

        self.assertEqual(result["explanation"], "No explanation was returned.")
        self.assertEqual(result["root_cause"], "No root cause was returned.")
        self.assertEqual(result["fix"], "No fix was returned.")
        self.assertEqual(result["improved_code"], "# No improved code was returned.")


if __name__ == "__main__":
    unittest.main()
