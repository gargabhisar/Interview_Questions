# Interview HTML maintenance scripts

Optional build helpers for `Interview_Questions.html`. The live site does not need Python.

## Setup

```bash
pip install -r scripts/requirements.txt
```

## Apply answer enhancements

Merges HTML snippets from the `interview_answers_*.py` modules into answer panes by question id (`q_*`).

```bash
python scripts/apply_enhancements.py
```

Reads and writes `Interview_Questions.html` in the repo root.

## Data modules

| File | Content |
|------|---------|
| `interview_answers_generated.py` | OOPS / .NET answer HTML |
| `interview_answers_sql_design.py` | SQL / database answer HTML |
| `interview_answers_async_other.py` | Async / threading answer HTML |
