#!/usr/bin/env python3
"""Discover Fullsend installation evidence in a repository checkout."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


WORKFLOW_SUFFIXES = {".yml", ".yaml"}
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
USES_RE = re.compile(r"^\s*uses:\s*([^\s#]+)", re.MULTILINE)
SLASH_COMMAND_RE = re.compile(r"(?<![\w-])/fs-[a-z0-9][a-z0-9-]*")


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            command,
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
        )
    except FileNotFoundError as error:
        return subprocess.CompletedProcess(command, 127, "", str(error))


def resolve_repo(start: Path) -> Path:
    start = start.expanduser().resolve()
    if start.is_file():
        start = start.parent

    result = run(["git", "rev-parse", "--show-toplevel"], start)
    if result.returncode == 0 and result.stdout.strip():
        return Path(result.stdout.strip()).resolve()

    for candidate in (start, *start.parents):
        if (candidate / ".fullsend").is_dir() or has_fullsend_workflow(candidate):
            return candidate
    return start


def has_fullsend_workflow(root: Path) -> bool:
    workflow_dir = root / ".github" / "workflows"
    if not workflow_dir.is_dir():
        return False
    return any(
        path.is_file()
        and path.suffix in WORKFLOW_SUFFIXES
        and "fullsend" in path.name.lower()
        for path in workflow_dir.iterdir()
    )


def relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def yaml_scalar(text: str, key: str) -> str | None:
    match = re.search(
        rf"^\s*{re.escape(key)}:\s*([^#\n]+?)\s*(?:#.*)?$", text, re.MULTILINE
    )
    if not match:
        return None
    return match.group(1).strip().strip("'\"") or None


def yaml_list(text: str, key: str) -> list[str]:
    inline = re.search(
        rf"^\s*{re.escape(key)}:\s*\[([^\]]*)\]", text, re.MULTILINE
    )
    if inline:
        return [
            value.strip().strip("'\"")
            for value in inline.group(1).split(",")
            if value.strip()
        ]

    lines = text.splitlines()
    for index, line in enumerate(lines):
        match = re.match(rf"^(\s*){re.escape(key)}:\s*$", line)
        if not match:
            continue
        indent = len(match.group(1))
        values: list[str] = []
        for child in lines[index + 1 :]:
            if not child.strip() or child.lstrip().startswith("#"):
                continue
            child_indent = len(child) - len(child.lstrip())
            if child_indent <= indent:
                break
            item = re.match(r"^\s*-\s*([^#]+?)\s*(?:#.*)?$", child)
            if item:
                values.append(item.group(1).strip().strip("'\""))
        return values
    return []


def frontmatter(path: Path) -> dict[str, str]:
    text = read_text(path)
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    block = match.group(1)
    result: dict[str, str] = {}
    current: str | None = None
    for line in block.splitlines():
        field = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if field:
            current = field.group(1)
            value = field.group(2).strip().strip("'\"")
            result[current] = value if value not in {"|", ">", "|-", ">-"} else ""
        elif current and line.startswith((" ", "\t")):
            value = line.strip()
            if value:
                result[current] = " ".join(filter(None, [result[current], value]))
        else:
            current = None
    return result


def candidate_dirs(root: Path, leaf: str) -> list[Path]:
    candidates = [
        root / ".fullsend" / leaf,
        root / ".fullsend" / "customized" / leaf,
        root / leaf,
        root / "customized" / leaf,
    ]
    seen: set[Path] = set()
    result: list[Path] = []
    for candidate in candidates:
        try:
            resolved = candidate.resolve()
        except OSError:
            resolved = candidate
        if candidate.is_dir() and resolved not in seen:
            seen.add(resolved)
            result.append(candidate)
    return result


def inspect_harnesses(root: Path) -> list[dict[str, Any]]:
    harnesses: list[dict[str, Any]] = []
    for directory in candidate_dirs(root, "harness"):
        for path in sorted(directory.glob("*.y*ml")):
            text = read_text(path)
            harnesses.append(
                {
                    "name": path.stem,
                    "path": relative(path, root),
                    "role": yaml_scalar(text, "role"),
                    "slug": yaml_scalar(text, "slug"),
                    "agent": yaml_scalar(text, "agent"),
                    "base": yaml_scalar(text, "base"),
                    "source": yaml_scalar(text, "source"),
                    "model": yaml_scalar(text, "model"),
                    "image": yaml_scalar(text, "image"),
                    "runtime": yaml_scalar(text, "runtime"),
                    "policy": yaml_scalar(text, "policy"),
                    "timeout_minutes": yaml_scalar(text, "timeout_minutes"),
                    "skills": yaml_list(text, "skills"),
                    "plugins": yaml_list(text, "plugins"),
                    "providers": yaml_list(text, "providers"),
                    "host_file_sources": sorted(
                        set(
                            re.findall(
                                r"^\s*-?\s*src:\s*([^#\n]+?)\s*(?:#.*)?$",
                                text,
                                re.MULTILINE,
                            )
                        )
                    ),
                }
            )
    return harnesses


def inspect_agent_definitions(root: Path) -> list[dict[str, Any]]:
    agents: list[dict[str, Any]] = []
    for directory in candidate_dirs(root, "agents"):
        for path in sorted(directory.glob("*.md")):
            metadata = frontmatter(path)
            agents.append(
                {
                    "name": metadata.get("name") or path.stem,
                    "path": relative(path, root),
                    "description": metadata.get("description"),
                }
            )
    return agents


def skill_roots(root: Path) -> list[tuple[str, Path]]:
    return [
        ("repository", root / ".agents" / "skills"),
        ("repository", root / ".claude" / "skills"),
        ("fullsend", root / ".fullsend" / "skills"),
        ("legacy-fullsend", root / ".fullsend" / "customized" / "skills"),
        ("fullsend", root / "skills"),
        ("legacy-fullsend", root / "customized" / "skills"),
    ]


def inspect_skills(root: Path) -> list[dict[str, Any]]:
    skills: list[dict[str, Any]] = []
    seen: set[Path] = set()
    for scope, directory in skill_roots(root):
        if not directory.is_dir():
            continue
        for skill_file in sorted(directory.glob("*/SKILL.md")):
            try:
                resolved = skill_file.resolve()
            except OSError:
                resolved = skill_file
            if resolved in seen:
                continue
            seen.add(resolved)
            metadata = frontmatter(skill_file)
            skills.append(
                {
                    "name": metadata.get("name") or skill_file.parent.name,
                    "description": metadata.get("description"),
                    "path": relative(skill_file, root),
                    "scope": scope,
                    "symlinked": skill_file.is_symlink() or skill_file.parent.is_symlink(),
                }
            )
    return skills


def inspect_workflows(root: Path) -> list[dict[str, Any]]:
    workflow_dir = root / ".github" / "workflows"
    if not workflow_dir.is_dir():
        return []
    workflows: list[dict[str, Any]] = []
    for path in sorted(workflow_dir.iterdir()):
        if not path.is_file() or path.suffix not in WORKFLOW_SUFFIXES:
            continue
        text = read_text(path)
        if "fullsend" not in path.name.lower() and "fullsend" not in text.lower():
            continue
        workflows.append(
            {
                "path": relative(path, root),
                "name": yaml_scalar(text, "name") or path.stem,
                "uses": sorted(set(USES_RE.findall(text))),
                "slash_commands": sorted(set(SLASH_COMMAND_RE.findall(text))),
            }
        )
    return workflows


def detect_mode(root: Path, workflows: list[dict[str, Any]]) -> tuple[str, list[str]]:
    evidence: list[str] = []
    texts = [read_text(root / item["path"]) for item in workflows]
    if any(re.search(r"install_mode:\s*per-repo", text) for text in texts):
        evidence.extend(
            item["path"]
            for item, text in zip(workflows, texts)
            if re.search(r"install_mode:\s*per-repo", text)
        )
        return "per-repo", evidence
    if any(re.search(r"install_mode:\s*per-org", text) for text in texts):
        evidence.extend(
            item["path"]
            for item, text in zip(workflows, texts)
            if re.search(r"install_mode:\s*per-org", text)
        )
        return "per-org", evidence
    if (root / "config.yaml").is_file() and (root / "harness").is_dir():
        return "fullsend-config-repository", ["config.yaml", "harness/"]
    if candidate_dirs(root, "harness"):
        return "local-definitions", [relative(path, root) for path in candidate_dirs(root, "harness")]
    return "unknown", evidence


def cli_agents(root: Path) -> dict[str, Any] | None:
    fullsend_dirs = []
    if (root / ".fullsend").is_dir():
        fullsend_dirs.append(root / ".fullsend")
    if (root / "config.yaml").is_file():
        fullsend_dirs.append(root)
    for directory in fullsend_dirs:
        result = run(
            ["fullsend", "agent", "list", "--fullsend-dir", str(directory)], root
        )
        if result.returncode == 0:
            return {
                "fullsend_dir": relative(directory, root),
                "output": result.stdout.strip(),
            }
    return None


def inspect(root: Path) -> dict[str, Any]:
    workflows = inspect_workflows(root)
    harnesses = inspect_harnesses(root)
    definitions = inspect_agent_definitions(root)
    skills = inspect_skills(root)
    mode, mode_evidence = detect_mode(root, workflows)

    config_files = []
    for path in (
        root / ".fullsend" / "config.yaml",
        root / ".fullsend" / "config.base.yaml",
        root / "config.yaml",
        root / "config.base.yaml",
    ):
        if path.is_file():
            config_files.append(relative(path, root))

    markers = sorted(
        set(
            config_files
            + [item["path"] for item in workflows]
            + [item["path"] for item in harnesses]
        )
    )
    remote_sources = sorted(
        {
            source
            for workflow in workflows
            for source in workflow["uses"]
            if not source.startswith("./")
            and ("fullsend" in source.lower() or ".github/workflows/" in source)
        }
    )

    return {
        "repo_root": str(root),
        "found": bool(markers),
        "installation": {"mode": mode, "evidence": mode_evidence},
        "markers": markers,
        "config_files": config_files,
        "harnesses": harnesses,
        "agent_definitions": definitions,
        "skills": skills,
        "workflows": workflows,
        "remote_sources": remote_sources,
        "cli_agent_list": cli_agents(root),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Inspect a repository checkout for Fullsend configuration, agents, "
            "skills, and workflows. Outputs JSON and never reads secret values."
        )
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Path inside the target repository (default: current directory).",
    )
    args = parser.parse_args()

    root = resolve_repo(Path(args.repo))
    result = inspect(root)
    json.dump(result, sys.stdout, indent=2 if sys.stdout.isatty() else None)
    sys.stdout.write("\n")
    return 0 if result["found"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
