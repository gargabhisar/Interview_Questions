import re
import sys
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4", "-q"])
    from bs4 import BeautifulSoup

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from interview_answers_generated import ANSWERS as OOPS_NET
from interview_answers_sql_design import ANSWERS as SQL_DESIGN
from interview_answers_async_other import ANSWERS as ASYNC_OTHER

HTML_PATH = REPO_ROOT / "Interview_Questions.html"

ANSWERS = {}
ANSWERS.update(OOPS_NET)
ANSWERS.update(SQL_DESIGN)
ANSWERS.update(ASYNC_OTHER)

EXTRA_CSS = """
.interview-tip {
    background: #f0f7ff;
    border-left: 4px solid #0066cc;
    padding: 12px 16px;
    margin: 16px 0;
    border-radius: 0 6px 6px 0;
}

.answer-pane h3 {
    margin-top: 20px;
    padding-bottom: 6px;
    border-bottom: 1px solid #e0e0e0;
}

.answer-pane pre {
    font-size: 13px;
    line-height: 1.5;
}
"""


def replace_pane_inner(soup, pane_id, html_content):
    pane = soup.find("div", id=pane_id, class_="answer-pane")
    if not pane:
        print(f"  WARNING: pane {pane_id} not found")
        return False

    active = "active" in pane.get("class", [])
    pane.clear()
    if active:
        pane["class"] = ["answer-pane", "active"]

    fragment = BeautifulSoup(html_content, "html.parser")
    for child in list(fragment.children):
        if getattr(child, "name", None) or str(child).strip():
            pane.append(child)

    return True


def main():
    content = HTML_PATH.read_text(encoding="utf-8")

    if ".interview-tip" not in content:
        content = content.replace("</style>", EXTRA_CSS + "\n</style>")

    soup = BeautifulSoup(content, "html.parser")

    updated = 0
    missing = []
    for qid, html in ANSWERS.items():
        if replace_pane_inner(soup, qid, html):
            updated += 1
        else:
            missing.append(qid)

    HTML_PATH.write_text(str(soup), encoding="utf-8")

    print(f"Updated {updated} answer panes.")
    if missing:
        print(f"Missing panes: {missing}")
    print(f"Total answers in dict: {len(ANSWERS)}")
    print(f"File saved: {HTML_PATH}")


if __name__ == "__main__":
    main()
