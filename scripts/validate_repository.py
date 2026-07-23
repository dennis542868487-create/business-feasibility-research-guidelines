#!/usr/bin/env python3
"""Validate the repository without network access or third-party packages."""

from __future__ import annotations

import json
import re
import struct
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "business-feasibility-research-guidelines"
SKILLS = PLUGIN / "skills"
MAIN_SKILL = SKILLS / "business-feasibility-research-guidelines"
SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PLACEHOLDER = re.compile(
    "|".join(
        re.escape(token)
        for token in (
            "[" + "TO" + "DO",
            "TO" + "DO:",
            "github.com/" + "OWNER",
            "TBD" + "_PLACEHOLDER",
        )
    ),
    re.IGNORECASE,
)
TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".py", ".csv", ".txt"}
REQUIRED_ROOT_FILES = (
    "README.md",
    "LICENSE",
    "PRIVACY.md",
    "SECURITY.md",
    "TERMS.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "VERSION",
    "docs/PRODUCT_REQUIREMENTS.md",
    "docs/EVALUATION_GUIDE.md",
    "docs/INSTALLATION.md",
    "docs/LIMITATIONS.md",
    "docs/REFERENCES.md",
    "prompts/manual-mode.md",
)
REQUIRED_INTERFACE = (
    "displayName",
    "shortDescription",
    "longDescription",
    "developerName",
    "category",
    "capabilities",
    "defaultPrompt",
)


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("frontmatter must start on line 1")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("frontmatter closing delimiter is missing")
    values: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key in values:
            raise ValueError(f"duplicate frontmatter key: {key}")
        values[key] = value
    return values


def markdown_links(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return re.findall(r"\[[^\]]*\]\(([^)]+)\)", text)


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()[:24]
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise ValueError("not a valid PNG header")
    return struct.unpack(">II", data[16:24])


def validate_repository(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    plugin = root / "plugins" / "business-feasibility-research-guidelines"
    skills = plugin / "skills"
    main_skill = skills / "business-feasibility-research-guidelines"

    for relative in REQUIRED_ROOT_FILES:
        if not (root / relative).is_file():
            errors.append(f"Missing required file: {relative}")

    manifest_path = plugin / ".codex-plugin" / "plugin.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"Invalid plugin manifest: {exc}")
        manifest = {}
    if manifest.get("name") != plugin.name:
        errors.append("Plugin folder and manifest name differ")
    if not SEMVER.fullmatch(str(manifest.get("version", ""))):
        errors.append("Plugin version is not strict semver")
    if not str(manifest.get("description", "")).strip():
        errors.append("Plugin description is missing")
    if not str(manifest.get("author", {}).get("name", "")).strip():
        errors.append("Plugin author.name is missing")
    if manifest.get("skills") != "./skills/":
        errors.append("Plugin skills path must be ./skills/")
    if "apps" in manifest or "mcpServers" in manifest:
        errors.append("Skills-only plugin must not declare apps or mcpServers")
    interface = manifest.get("interface", {})
    for field in REQUIRED_INTERFACE:
        if field not in interface or interface[field] in (None, "", []):
            errors.append(f"Plugin interface.{field} is missing")
    prompts = interface.get("defaultPrompt", [])
    if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3:
        errors.append("Plugin interface.defaultPrompt must contain 1-3 strings")
    elif any(not isinstance(item, str) or len(item) > 128 for item in prompts):
        errors.append("Plugin starter prompts must be strings of at most 128 characters")
    for field in ("composerIcon", "logo", "logoDark"):
        value = interface.get(field)
        if value:
            target = plugin / value.removeprefix("./")
            if not target.is_file():
                errors.append(f"Plugin asset does not exist: {value}")

    version_file = (root / "VERSION").read_text(encoding="utf-8").strip() if (root / "VERSION").exists() else ""
    if manifest.get("version") != version_file:
        errors.append("VERSION and plugin manifest version differ")

    marketplace_path = root / ".agents" / "plugins" / "marketplace.json"
    try:
        marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"Invalid marketplace manifest: {exc}")
        marketplace = {}
    entries = marketplace.get("plugins", [])
    matching = [item for item in entries if item.get("name") == plugin.name] if isinstance(entries, list) else []
    if len(matching) != 1:
        errors.append("Marketplace must contain exactly one matching plugin entry")
    else:
        entry = matching[0]
        source = entry.get("source", {})
        source_path = source.get("path") if isinstance(source, dict) else None
        if source_path != f"./plugins/{plugin.name}":
            errors.append("Marketplace source.path is incorrect")
        if source_path and not (root / source_path.removeprefix("./")).is_dir():
            errors.append("Marketplace source.path does not resolve")
        policy = entry.get("policy", {})
        if policy.get("installation") not in {"AVAILABLE", "NOT_AVAILABLE", "INSTALLED_BY_DEFAULT"}:
            errors.append("Marketplace installation policy is invalid")
        if policy.get("authentication") not in {"ON_INSTALL", "ON_USE"}:
            errors.append("Marketplace authentication policy is invalid")
        if not entry.get("category"):
            errors.append("Marketplace category is missing")

    skill_dirs = sorted(path for path in skills.iterdir() if path.is_dir()) if skills.is_dir() else []
    if len(skill_dirs) != 6:
        errors.append(f"Expected 6 skill directories, found {len(skill_dirs)}")
    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            errors.append(f"Missing SKILL.md: {skill_dir.name}")
            continue
        try:
            frontmatter = parse_frontmatter(skill_md)
        except ValueError as exc:
            errors.append(f"Invalid {skill_dir.name}/SKILL.md: {exc}")
            continue
        if set(frontmatter) != {"name", "description"}:
            errors.append(f"{skill_dir.name} frontmatter must contain only name and description")
        if frontmatter.get("name") != skill_dir.name or not SKILL_NAME.fullmatch(skill_dir.name):
            errors.append(f"Invalid or mismatched skill name: {skill_dir.name}")
        if len(frontmatter.get("description", "")) < 40:
            errors.append(f"Skill description is too short: {skill_dir.name}")
        openai_yaml = skill_dir / "agents" / "openai.yaml"
        if not openai_yaml.is_file():
            errors.append(f"Missing agents/openai.yaml: {skill_dir.name}")
        else:
            yaml_text = openai_yaml.read_text(encoding="utf-8")
            if f"${skill_dir.name}" not in yaml_text:
                errors.append(f"openai.yaml default_prompt does not mention ${skill_dir.name}")
        for link in markdown_links(skill_md):
            if link.startswith(("http://", "https://", "#", "mailto:")):
                continue
            target = (skill_md.parent / link.split("#", 1)[0]).resolve()
            if not target.exists():
                errors.append(f"Broken relative link in {skill_md.relative_to(root)}: {link}")

    if (main_skill / "SKILL.md").is_file():
        line_count = len((main_skill / "SKILL.md").read_text(encoding="utf-8").splitlines())
        if line_count >= 500:
            errors.append(f"Main SKILL.md has {line_count} lines; keep it under 500")

    for relative, expected in (("assets/icon.png", (256, 256)), ("assets/logo.png", (1024, 1024))):
        path = plugin / relative
        try:
            actual = png_size(path)
            if actual != expected:
                errors.append(f"{relative} has size {actual}, expected {expected}")
        except (OSError, ValueError) as exc:
            errors.append(f"Invalid {relative}: {exc}")

    cases_dir = root / "evals" / "cases"
    cases = []
    for case_path in sorted(cases_dir.glob("*.json")):
        try:
            case = json.loads(case_path.read_text(encoding="utf-8"))
            cases.append(case)
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid Eval JSON {case_path.name}: {exc}")
            continue
        for key in ("id", "type", "prompt", "required_concepts", "forbidden_patterns", "critical_failures", "human_rubric"):
            if key not in case:
                errors.append(f"Eval {case_path.name} missing {key}")
    positives = sum(1 for case in cases if case.get("type") == "positive")
    negatives = sum(1 for case in cases if case.get("type") == "negative")
    if positives < 5 or negatives < 3:
        errors.append(f"Need at least 5 positive and 3 negative Evals; found {positives} and {negatives}")

    ignored_parts = {".venv", ".git", "releases", "__pycache__"}
    for path in root.rglob("*"):
        if ignored_parts.intersection(path.relative_to(root).parts):
            continue
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if PLACEHOLDER.search(text):
            errors.append(f"Unresolved placeholder in {path.relative_to(root)}")
    plugin_scripts = main_skill / "scripts"
    for path in plugin_scripts.glob("*.py"):
        text = path.read_text(encoding="utf-8")
        if re.search(r"\b(?:requests|urllib\.request|http\.client|socket)\b", text):
            errors.append(f"Unexpected network-capable import in core script: {path.name}")

    return errors


def main() -> int:
    errors = validate_repository()
    payload: dict[str, Any] = {
        "repository": str(ROOT),
        "passed": not errors,
        "error_count": len(errors),
        "errors": errors,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
