#!/usr/bin/env python3
"""Compare generated and committed brand assets by decoded pixel content."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


FILES = ("icon.png", "logo.png")


def compare_images(expected_path: Path, actual_path: Path) -> list[str]:
    errors: list[str] = []
    try:
        with Image.open(expected_path) as expected_image, Image.open(actual_path) as actual_image:
            expected_image.load()
            actual_image.load()
            if expected_image.size != actual_image.size:
                errors.append(
                    f"{expected_path.name}: size differs: {expected_image.size} != {actual_image.size}"
                )
            if expected_image.mode != actual_image.mode:
                errors.append(
                    f"{expected_path.name}: mode differs: {expected_image.mode} != {actual_image.mode}"
                )
            if expected_image.convert("RGBA").tobytes() != actual_image.convert("RGBA").tobytes():
                errors.append(f"{expected_path.name}: decoded RGBA pixels differ")
    except OSError as exc:
        errors.append(f"{expected_path.name}: cannot compare image: {exc}")
    return errors


def compare_directories(expected_dir: Path, actual_dir: Path) -> list[str]:
    errors: list[str] = []
    for filename in FILES:
        expected_path = expected_dir / filename
        actual_path = actual_dir / filename
        if not expected_path.is_file():
            errors.append(f"missing expected asset: {expected_path}")
            continue
        if not actual_path.is_file():
            errors.append(f"missing generated asset: {actual_path}")
            continue
        errors.extend(compare_images(expected_path, actual_path))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected", required=True)
    parser.add_argument("--actual", required=True)
    args = parser.parse_args()
    errors = compare_directories(Path(args.expected), Path(args.actual))
    if errors:
        for error in errors:
            print(error)
        return 1
    print("Brand asset pixels match committed files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
