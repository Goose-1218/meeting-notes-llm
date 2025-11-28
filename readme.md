# Meeting Notes → Summary & Action Items (LLM-style Demo)

This is a tiny demo of how an LLM-powered tool can take unstructured meeting notes and convert them into:

- a readable summary
- structured action items in JSON

Currently the project uses a temp api key for demonstration 

An  LLM call can be plugged in later inside `call_llm()` in `main.py`.

## Usage

```bash
python main.py example_notes.txt
