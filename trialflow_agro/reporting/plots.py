"""
Lightweight HTML rendering helpers for trialflow-agro.

No actual plotting libraries yet; instead we render simple
HTML tables that can be embedded in reports.
"""

from typing import List, Mapping


def _html_escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def table_from_summaries(title: str, rows: List[Mapping[str, object]]) -> str:
    if not rows:
        return f"<h3>{_html_escape(title)}</h3><p>No data available.</p>"

    # assume all rows share same keys
    columns = list(rows[0].keys())

    header_cells = "".join(f"<th>{_html_escape(col)}</th>" for col in columns)
    body_rows = []
    for row in rows:
        cells = "".join(f"<td>{_html_escape(str(row[col]))}</td>" for col in columns)
        body_rows.append(f"<tr>{cells}</tr>")

    body_html = "\n".join(body_rows)

    return f"""
    <h3>{_html_escape(title)}</h3>
    <table border="1" cellspacing="0" cellpadding="4">
      <thead>
        <tr>{header_cells}</tr>
      </thead>
      <tbody>
        {body_html}
      </tbody>
    </table>
    """
