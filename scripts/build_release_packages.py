#!/usr/bin/env python3
"""Build reproducible Plugin, standalone Skill, and Manual Mode release ZIPs."""

from __future__ import annotations

import argparse
import hashlib
import os
import zipfile
from pathlib import Path

from validate_repository import validate_repository


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_NAME = "business-feasibility-research-guidelines"
PLUGIN = ROOT / "plugins" / PLUGIN_NAME
MAIN_SKILL = PLUGIN / "skills" / PLUGIN_NAME
FIXED_TIME = (2026, 1, 1, 0, 0, 0)


def iter_files(directory: Path):
    for path in sorted(directory.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc":
            yield path


def add_file(archive: zipfile.ZipFile, source: Path, archive_name: str) -> None:
    info = zipfile.ZipInfo(archive_name, date_time=FIXED_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    mode = 0o755 if source.suffix == ".py" else 0o644
    info.external_attr = (mode & 0xFFFF) << 16
    archive.writestr(info, source.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def zip_tree(output: Path, source: Path, prefix: str) -> None:
    with zipfile.ZipFile(output, "w") as archive:
        for path in iter_files(source):
            relative = path.relative_to(source).as_posix()
            add_file(archive, path, f"{prefix}/{relative}")


def build(output_dir: Path) -> list[Path]:
    errors = validate_repository(ROOT)
    if errors:
        raise RuntimeError("Repository validation failed:\n" + "\n".join(errors))
    output_dir.mkdir(parents=True, exist_ok=True)
    plugin_zip = output_dir / f"{PLUGIN_NAME}-plugin.zip"
    standalone_zip = output_dir / f"{PLUGIN_NAME}-standalone-skill.zip"
    manual_zip = output_dir / f"{PLUGIN_NAME}-manual-mode.zip"
    for target in (plugin_zip, standalone_zip, manual_zip, output_dir / "checksums.txt"):
        if target.exists():
            target.unlink()

    zip_tree(plugin_zip, PLUGIN, PLUGIN_NAME)
    zip_tree(standalone_zip, MAIN_SKILL, PLUGIN_NAME)

    manual_prefix = f"{PLUGIN_NAME}-manual-mode"
    manual_files = {
        ROOT / "prompts" / "manual-mode.md": "manual-mode.md",
        ROOT / "docs" / "LIMITATIONS.md": "LIMITATIONS.md",
        ROOT / "PRIVACY.md": "PRIVACY.md",
        ROOT / "LICENSE": "LICENSE",
        ROOT / "VERSION": "VERSION",
    }
    with zipfile.ZipFile(manual_zip, "w") as archive:
        for source, relative in manual_files.items():
            add_file(archive, source, f"{manual_prefix}/{relative}")
        for source in iter_files(MAIN_SKILL / "assets" / "templates"):
            relative = source.relative_to(MAIN_SKILL / "assets" / "templates").as_posix()
            add_file(archive, source, f"{manual_prefix}/templates/{relative}")
        for source in iter_files(MAIN_SKILL / "scripts"):
            relative = source.relative_to(MAIN_SKILL / "scripts").as_posix()
            add_file(archive, source, f"{manual_prefix}/scripts/{relative}")

    artifacts = [plugin_zip, standalone_zip, manual_zip]
    checksum_lines = []
    for artifact in artifacts:
        digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
        checksum_lines.append(f"{digest}  {artifact.name}")
    checksums = output_dir / "checksums.txt"
    checksums.write_text("\n".join(checksum_lines) + "\n", encoding="utf-8")
    artifacts.append(checksums)
    return artifacts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=str(ROOT / "releases"))
    args = parser.parse_args()
    try:
        artifacts = build(Path(args.output).resolve())
    except RuntimeError as exc:
        print(str(exc))
        return 1
    for artifact in artifacts:
        print(artifact)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
