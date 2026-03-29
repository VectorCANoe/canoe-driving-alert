from __future__ import annotations

import subprocess
from pathlib import Path

import markdown


DATE_STAMP = "2026-03-28"
REPO_ROOT = Path(__file__).resolve().parents[5]
ARCH_ROOT = Path(__file__).resolve().parents[1]
MASTER_BOOK = ARCH_ROOT / f"ECU_METADATA_BOOK_{DATE_STAMP}.md"
HTML_OUT = ARCH_ROOT / f"ECU_METADATA_BOOK_{DATE_STAMP}.html"
PDF_OUT = ARCH_ROOT / f"ECU_METADATA_BOOK_{DATE_STAMP}.pdf"

EDGE_CANDIDATES = [
    Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
]


def find_browser() -> Path | None:
    for candidate in EDGE_CANDIDATES:
        if candidate.exists():
            return candidate
    return None


def build_html(markdown_text: str) -> str:
    body = markdown.markdown(
        markdown_text,
        extensions=[
            "extra",
            "tables",
            "sane_lists",
            "md_in_html",
        ],
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>CANoe Runtime ECU Master Book ({DATE_STAMP})</title>
  <style>
    @page {{
      size: A4;
      margin: 14mm 12mm 16mm 12mm;
    }}

    :root {{
      --paper: #f6f1e8;
      --ink: #0f172a;
      --muted: #475569;
      --line: #dbe4ee;
      --accent: #0f766e;
      --card: #ffffff;
    }}

    html {{
      background: var(--paper);
    }}

    body {{
      margin: 0;
      font-family: "Segoe UI", "Noto Sans KR", sans-serif;
      color: var(--ink);
      background: var(--paper);
      line-height: 1.55;
      font-size: 14px;
    }}

    main {{
      max-width: 1180px;
      margin: 0 auto;
      padding: 20px 18px 40px;
    }}

    article {{
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 20px;
      padding: 28px 32px 36px;
      box-shadow: 0 20px 48px rgba(15, 23, 42, 0.05);
    }}

    h1 {{
      margin: 0 0 12px;
      font-size: 34px;
      line-height: 1.1;
      letter-spacing: -0.03em;
    }}

    h2 {{
      margin: 34px 0 14px;
      padding-top: 18px;
      border-top: 2px solid #e2e8f0;
      font-size: 24px;
      line-height: 1.2;
    }}

    h3 {{
      margin: 26px 0 10px;
      font-size: 18px;
      line-height: 1.25;
    }}

    h4 {{
      margin: 20px 0 8px;
      font-size: 15px;
      line-height: 1.3;
      color: var(--accent);
    }}

    p, ul, ol, table {{
      margin: 0 0 14px;
    }}

    ul, ol {{
      padding-left: 22px;
    }}

    li {{
      margin: 0 0 6px;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      table-layout: fixed;
    }}

    th, td {{
      border: 1px solid var(--line);
      padding: 10px 12px;
      vertical-align: top;
      text-align: left;
      word-break: break-word;
    }}

    th {{
      background: #f8fafc;
      font-weight: 700;
    }}

    td:first-child,
    th:first-child {{
      width: 210px;
    }}

    img {{
      display: block;
      width: 100%;
      max-width: 100%;
      height: auto;
      margin: 16px 0 24px;
      border: 1px solid var(--line);
      border-radius: 18px;
      background: #fff;
    }}

    code {{
      font-family: "Cascadia Code", "Consolas", monospace;
      font-size: 12px;
      background: #f8fafc;
      padding: 0.1em 0.35em;
      border-radius: 6px;
    }}

    a {{
      color: #0f4c81;
      text-decoration: none;
    }}

    blockquote {{
      margin: 0 0 16px;
      padding: 0 0 0 16px;
      border-left: 4px solid #cbd5e1;
      color: var(--muted);
    }}

    div[style*="page-break-before"] {{
      page-break-before: always;
      break-before: page;
      height: 0;
      margin: 0;
      padding: 0;
      border: 0;
    }}

    @media print {{
      img {{
        break-inside: avoid;
        page-break-inside: avoid;
      }}
    }}
  </style>
</head>
<body>
  <main>
    <article>
{body}
    </article>
  </main>
</body>
</html>
"""


def render() -> None:
    if not MASTER_BOOK.exists():
        raise FileNotFoundError(f"Master book not found: {MASTER_BOOK}")

    markdown_text = MASTER_BOOK.read_text(encoding="utf-8")
    html = build_html(markdown_text)
    HTML_OUT.write_text(html, encoding="utf-8")

    browser = find_browser()
    if browser is None:
        raise FileNotFoundError("No supported browser found for PDF rendering.")

    command = [
        str(browser),
        "--headless",
        "--disable-gpu",
        "--allow-file-access-from-files",
        "--hide-scrollbars",
        "--no-first-run",
        "--print-to-pdf-no-header",
        f"--virtual-time-budget={60000}",
        f"--print-to-pdf={PDF_OUT}",
        HTML_OUT.resolve().as_uri(),
    ]
    subprocess.run(command, check=True)
    print(f"[master-book-render] html: {HTML_OUT}")
    print(f"[master-book-render] pdf: {PDF_OUT}")


if __name__ == "__main__":
    render()
