"""Tests for prompt generation."""

from __future__ import annotations

import unittest

from prompts import SYSTEM_INSTRUCTIONS, build_analysis_prompt


class PromptTests(unittest.TestCase):
    """Test the analysis prompt content."""

    def test_build_analysis_prompt_includes_inputs_and_json_rules(self) -> None:
        error_text = "NameError: name 'user_name' is not defined"
        code_text = "print(user_name)"

        prompt = build_analysis_prompt(error_text=error_text, code_text=code_text)

        self.assertIn(SYSTEM_INSTRUCTIONS, prompt)
        self.assertIn("Return only valid JSON", prompt)
        self.assertIn(error_text, prompt)
        self.assertIn(code_text, prompt)
        self.assertIn("Error Message:", prompt)
        self.assertIn("Code Snippet:", prompt)


if __name__ == "__main__":
    unittest.main()
