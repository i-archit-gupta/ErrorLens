"""Streamlit app for explaining errors and suggesting fixes."""

from __future__ import annotations

import streamlit as st

from llm import analyze_error
from utils import clean_user_input, validate_inputs


st.set_page_config(page_title="Error Lens", page_icon=":warning:")


def main() -> None:
    """Render the Streamlit UI."""
    st.title("Error Lens")
    st.write(
        "Paste an error message and code snippet to get a plain-English explanation "
        "and a suggested fix."
    )

    error_text = st.text_area(
        "Error Message",
        placeholder="Paste the full traceback or error message here...",
        height=180,
    )
    code_text = st.text_area(
        "Code Snippet",
        placeholder="Paste the relevant code here...",
        height=260,
    )

    if st.button("Analyze Error", type="primary"):
        cleaned_error = clean_user_input(error_text)
        cleaned_code = clean_user_input(code_text)
        validation_error = validate_inputs(cleaned_error, cleaned_code)

        if validation_error:
            st.error(validation_error)
            return

        try:
            with st.spinner("Analyzing your error..."):
                result = analyze_error(cleaned_error, cleaned_code)
        except ValueError as exc:
            st.error(str(exc))
            return
        except RuntimeError as exc:
            st.error(f"Analysis failed: {exc}")
            return
        except Exception:
            st.error("Something unexpected went wrong while analyzing the error.")
            return

        st.subheader("Explanation")
        st.write(result["explanation"])

        st.subheader("Root Cause")
        st.write(result["root_cause"])

        st.subheader("Fix")
        st.write(result["fix"])

        st.subheader("Improved Code")
        st.code(result["improved_code"], language="python")


if __name__ == "__main__":
    main()
