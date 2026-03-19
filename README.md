# Error Lens

Error Lens is a minimal Streamlit app that uses the Gemini API to explain Python errors in plain English, identify likely root causes, suggest fixes, and generate an improved code snippet.

## Project Structure

- `app.py` - Streamlit user interface
- `llm.py` - Gemini API integration
- `prompts.py` - Prompt template for structured analysis
- `utils.py` - Input cleaning, validation, and response formatting
- `requirements.txt` - Python dependencies
- `.env.example` - Example environment file

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file from the example:

```bash
cp .env.example .env
```

4. Add your Gemini API key to `.env`:

```env
GEMINI_API_KEY=your_api_key_here
```

## Run the App

```bash
streamlit run app.py
```

## Run the Tests

```bash
python3 -m unittest discover -s tests -v
```

## Example Usage

Error message:

```text
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

Code snippet:

```python
age = 25
message = "Your age is: " + age
print(message)
```

The app will return:

- A simple explanation of the error
- The likely root cause
- A suggested fix
- An improved code snippet
