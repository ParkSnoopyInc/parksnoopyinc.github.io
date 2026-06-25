#!/usr/bin/env python3
"""Build a PEP 503 static simple index for Vulkan PyTorch wheels."""

from __future__ import annotations

import hashlib
import html
import re
import shutil
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX_ROOT = ROOT / "static" / "index" / "whl" / "vulkan"
WHEEL_DIR = INDEX_ROOT / "_wheels"

NORMALIZE_RE = re.compile(r"[-_.]+")


@dataclass(frozen=True)
class Link:
    href: str
    label: str
    modified: str
    size: str


def normalize_project(name: str) -> str:
    return NORMALIZE_RE.sub("-", name).lower()


def project_from_wheel(path: Path) -> str:
    # Wheel format: {distribution}-{version}-{build?}-{python}-{abi}-{platform}.whl
    distribution = path.name.split("-", 1)[0]
    return normalize_project(distribution)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def human_size(size: int) -> str:
    units = ["B", "KiB", "MiB", "GiB"]
    value = float(size)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.1f} {unit}" if unit != "B" else f"{size} B"
        value /= 1024
    raise AssertionError("unreachable")


def modified(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).strftime(
        "%Y-%m-%d %H:%M UTC"
    )


def write_html(
    path: Path, title: str, heading: str, stylesheet: str, links: list[Link]
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = [
        "<!doctype html>",
        '<html lang="en">',
        "  <head>",
        '    <meta charset="utf-8">',
        '    <meta name="viewport" content="width=device-width, initial-scale=1">',
        f'    <link rel="stylesheet" href="{html.escape(stylesheet, quote=True)}">',
        '    <script src="/js/wheel-index.js" defer></script>',
        f"    <title>{html.escape(title)}</title>",
        "  </head>",
        "  <body>",
        "    <main>",
        "      <header>",
        "        <p class=\"eyebrow\">Python Simple Repository</p>",
        f"        <h1>{html.escape(heading)}</h1>",
        '        <nav class="actions" aria-label="Index actions">',
        '          <a class="button" href="/">Back To Blog</a>',
        '          <button class="button" type="button" data-theme-toggle>Dark Mode</button>',
        "        </nav>",
        "      </header>",
        '      <div class="listing">',
        "        <table>",
        "          <thead>",
        "            <tr><th>Name</th><th>Last Modified</th><th>Size</th></tr>",
        "          </thead>",
        "          <tbody>",
    ]
    for link in links:
        body.append(
            '            <tr>'
            f'<td class="name"><a href="{html.escape(link.href, quote=True)}">{html.escape(link.label)}</a></td>'
            f'<td class="modified">{html.escape(link.modified)}</td>'
            f'<td class="size">{html.escape(link.size)}</td>'
            "</tr>"
        )
    body.extend(
        [
            "          </tbody>",
            "        </table>",
            "      </div>",
            "      <footer>PEP 503 simple repository</footer>",
            "    </main>",
            "  </body>",
            "</html>",
            "",
        ]
    )
    path.write_text("\n".join(body), encoding="utf-8")


def main() -> None:
    WHEEL_DIR.mkdir(parents=True, exist_ok=True)
    for child in INDEX_ROOT.iterdir():
        if child.is_dir() and child.name != "_wheels":
            shutil.rmtree(child)

    wheels = sorted(WHEEL_DIR.glob("*.whl"))
    by_project: dict[str, list[Path]] = defaultdict(list)
    for wheel in wheels:
        by_project[project_from_wheel(wheel)].append(wheel)

    project_links = []
    for project, project_wheels in sorted(by_project.items()):
        latest_wheel = max(project_wheels, key=lambda wheel: wheel.stat().st_mtime)
        project_links.append(Link(f"{project}/", f"{project}/", modified(latest_wheel), "-"))
    write_html(
        INDEX_ROOT / "index.html",
        "Index of /index/whl/vulkan/",
        "Index of /index/whl/vulkan/",
        "/css/wheel-index.css",
        project_links,
    )

    for project, project_wheels in sorted(by_project.items()):
        links = []
        for wheel in project_wheels:
            digest = sha256(wheel)
            href = f"../_wheels/{wheel.name}#sha256={digest}"
            links.append(
                Link(href, wheel.name, modified(wheel), human_size(wheel.stat().st_size))
            )
        write_html(
            INDEX_ROOT / project / "index.html",
            f"Index of /index/whl/vulkan/{project}/",
            f"Index of /index/whl/vulkan/{project}/",
            "/css/wheel-index.css",
            links,
        )


if __name__ == "__main__":
    main()
