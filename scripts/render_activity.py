#!/usr/bin/env python3
"""Render assets/activity.svg from the public aggregate gist that feeds diego-nava.com."""
import json
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

FEED = "https://gist.githubusercontent.com/diegonava6/6bfd3cb89b08e457be05ef6920142cb7/raw/portfolio-activity.json"
METRICS = [
    ("authoredCommits", "Authored commits"),
    ("openedPullRequests", "Pull requests opened"),
    ("mergedPullRequests", "Pull requests merged"),
]
OUTPUT = Path(__file__).resolve().parent.parent / "assets" / "activity.svg"


def load_feed() -> dict:
    with urllib.request.urlopen(FEED, timeout=30) as response:
        data = json.load(response)
    counts = data["periods"]["allTime"]
    for key, _ in METRICS:
        if not isinstance(counts.get(key), int) or counts[key] < 0:
            sys.exit(f"Invalid {key} count in the activity feed.")
    return data


def render(data: dict) -> str:
    counts = data["periods"]["allTime"]
    updated = datetime.fromisoformat(data["updatedAt"].replace("Z", "+00:00")).strftime("%B %-d, %Y")
    sans = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
    columns = []
    for index, (key, label) in enumerate(METRICS):
        x = 56 + index * 300
        columns.append(
            f'  <text x="{x}" y="132" font-family="Georgia, \'Times New Roman\', serif" font-size="58" '
            f'letter-spacing="-2" fill="#e6e4df">{counts[key]:,}</text>\n'
            f'  <text x="{x}" y="160" font-family="{sans}" font-size="12" fill="#a6a6ac">{label}</text>'
        )
    summary = ", ".join(f"{counts[key]:,} {label.lower()}" for key, label in METRICS)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 230" width="1000" height="230" role="img" aria-labelledby="t">
  <title id="t">GitHub activity, all time: {summary}.</title>
  <rect width="1000" height="230" fill="#08090b"/>
  <line x1="56" y1="0.5" x2="944" y2="0.5" stroke="#ffffff" stroke-opacity=".13"/>
  <text x="56" y="56" font-family="{sans}" font-size="11" letter-spacing="1.4" fill="#b6b6be">GITHUB / CONTRIBUTIONS / ALL TIME</text>
{chr(10).join(columns)}
  <text x="56" y="204" font-family="{sans}" font-size="10" letter-spacing=".4" fill="#94949f">Counts from GitHub search, including accessible private repositories. Updated {updated}.</text>
</svg>
"""


if __name__ == "__main__":
    OUTPUT.write_text(render(load_feed()))
