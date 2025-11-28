import json
import sys
from pathlib import Path

PROMPT_TEMPLATE = """
You will receive raw meeting notes from a startup meeting.

Your job:

1. Write a concise summary of the meeting (max 150 words).
2. Extract clear action items.

Return ONLY valid JSON in this exact structure:

{
  "summary": "short paragraph summary",
  "tasks": [
    {
      "description": "what needs to be done",
      "owner": "person responsible or null if unknown",
      "due_date": "ISO date string like 2025-12-01 or null if not specified"
    }
  ]
}

Meeting notes:
---
{notes}
---
"""

MOCK_RESPONSE = {
    "summary": "The team discussed user drop-off in the onboarding flow, assigned analytics and design tasks, and planned a small A/B test before rolling out. There was also a recurring request for dark mode to be considered for the next roadmap.",
    "tasks": [
        {
            "description": "Analyze onboarding step 2 funnel in Mixpanel and report numbers",
            "owner": "Sam",
            "due_date": None
        },
        {
            "description": "Design a shorter onboarding copy and add a progress bar",
            "owner": "Alex",
            "due_date": None
        },
        {
            "description": "Prepare a small A/B test for the onboarding flow",
            "owner": "Yara",
            "due_date": None
        },
        {
            "description": "Consider adding dark mode to the Q1 roadmap",
            "owner": None,
            "due_date": None
        }
    ]
}

USE_MOCK = True


def load_notes(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    return path.read_text(encoding="utf-8")


def call_llm(notes: str) -> dict:
    if USE_MOCK:
        return MOCK_RESPONSE
    raise NotImplementedError("Real LLM integration not available in mock mode.")


def save_outputs(data: dict, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    (out_dir / "summary.md").write_text(
        f"# Meeting summary\n\n{data['summary']}\n", encoding="utf-8"
    )

    with (out_dir / "tasks.json").open("w", encoding="utf-8") as f:
        json.dump(data["tasks"], f, indent=2, ensure_ascii=False)


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <notes_file.txt>")
        sys.exit(1)

    notes_file = Path(sys.argv[1])
    notes = load_notes(notes_file)

    data = call_llm(notes)
    save_outputs(data, Path("output"))


if __name__ == "__main__":
    main()
