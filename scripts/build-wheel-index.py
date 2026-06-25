#!/usr/bin/env python3
"""Build a PEP 503 static simple index for Vulkan PyTorch wheels."""

from __future__ import annotations

import hashlib
import html
import re
import shutil
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX_ROOT = ROOT / "static" / "index" / "whl" / "vulkan"
WHEEL_DIR = INDEX_ROOT / "_wheels"

NORMALIZE_RE = re.compile(r"[-_.]+")


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


def write_html(path: Path, title: str, links: list[tuple[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = [
        "<!doctype html>",
        "<html>",
        "  <head>",
        '    <meta charset="utf-8">',
        f"    <title>{html.escape(title)}</title>",
        "  </head>",
        "  <body>",
    ]
    for href, label in links:
        body.append(
            f'    <a href="{html.escape(href, quote=True)}">{html.escape(label)}</a><br>'
        )
    body.extend(["  </body>", "</html>", ""])
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

    project_links = [(f"{project}/", project) for project in sorted(by_project)]
    write_html(INDEX_ROOT / "index.html", "Vulkan wheel index", project_links)

    for project, project_wheels in sorted(by_project.items()):
        links = []
        for wheel in project_wheels:
            digest = sha256(wheel)
            href = f"../_wheels/{wheel.name}#sha256={digest}"
            links.append((href, wheel.name))
        write_html(INDEX_ROOT / project / "index.html", project, links)


if __name__ == "__main__":
    main()
