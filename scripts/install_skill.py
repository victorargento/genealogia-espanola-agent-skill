#!/usr/bin/env python3
"""Install the canonical skill for Codex, Claude Code, or both."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


SKILL_NAME = "investigacion-genealogica-es"
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SOURCE = REPOSITORY_ROOT / "skills" / SKILL_NAME
TOOL_DIRECTORIES = {
    "codex": Path(".agents") / "skills",
    "claude": Path(".claude") / "skills",
}


def destinations(target: str, scope: str, project_dir: Path | None) -> list[tuple[str, Path]]:
    tools = list(TOOL_DIRECTORIES) if target == "both" else [target]
    if scope == "project":
        if project_dir is None:
            raise ValueError("--project-dir es obligatorio para scope project")
        base = project_dir.resolve()
    else:
        base = Path.home()
    return [(tool, base / TOOL_DIRECTORIES[tool] / SKILL_NAME) for tool in tools]


def install(target: str, scope: str, project_dir: Path | None = None) -> list[dict[str, str]]:
    assert SOURCE.is_dir(), f"No se encuentra la skill canónica: {SOURCE}"
    assert (SOURCE / "SKILL.md").is_file(), "La skill no contiene SKILL.md"
    planned = destinations(target, scope, project_dir)
    existing = [str(path) for _, path in planned if path.exists()]
    if existing:
        raise FileExistsError(
            "La instalación se ha detenido porque ya existe: " + ", ".join(existing)
        )

    result: list[dict[str, str]] = []
    for tool, destination in planned:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(SOURCE, destination, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        result.append({"tool": tool, "destination": str(destination)})
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", choices=["codex", "claude", "both"], default="both")
    parser.add_argument("--scope", choices=["user", "project"], default="user")
    parser.add_argument("--project-dir", type=Path)
    args = parser.parse_args()
    installed = install(args.target, args.scope, args.project_dir)
    print(json.dumps({"status": "OK", "installed": installed}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
