#!/usr/bin/env python3
"""Render deterministic PNG plugin assets from the documented vector geometry."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw


COLORS = {
    "teal": "#0F766E",
    "dark": "#115E59",
    "darkest": "#134E4A",
    "mint": "#CCFBF1",
    "gold": "#FBBF24",
    "white": "#FFFFFF",
}


def render(size: int) -> Image.Image:
    scale = 4
    canvas = size * scale
    image = Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    unit = canvas / 1024

    def box(values: tuple[float, float, float, float]) -> tuple[int, int, int, int]:
        return tuple(round(value * unit) for value in values)

    draw.rounded_rectangle(box((0, 0, 1024, 1024)), radius=round(224 * unit), fill=COLORS["teal"])
    draw.ellipse(box((220, 220, 804, 804)), outline=COLORS["mint"], width=round(48 * unit))
    draw.ellipse(box((302, 302, 722, 722)), fill=COLORS["dark"])
    draw.line(
        [(round(300 * unit), round(718 * unit)), (round(468 * unit), round(550 * unit)), (round(724 * unit), round(294 * unit))],
        fill=COLORS["gold"],
        width=round(64 * unit),
        joint="curve",
    )
    draw.polygon(
        [(round(650 * unit), round(292 * unit)), (round(736 * unit), round(282 * unit)), (round(726 * unit), round(368 * unit))],
        fill=COLORS["gold"],
    )
    for x, y in ((300, 718), (468, 550), (724, 294)):
        draw.ellipse(box((x - 72, y - 72, x + 72, y + 72)), fill=COLORS["white"], outline=COLORS["darkest"], width=round(28 * unit))
    draw.line(
        [(round(438 * unit), round(550 * unit)), (round(462 * unit), round(574 * unit)), (round(505 * unit), round(525 * unit))],
        fill=COLORS["teal"],
        width=round(30 * unit),
        joint="curve",
    )
    return image.resize((size, size), Image.Resampling.LANCZOS)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--plugin-root",
        default=str(Path(__file__).resolve().parents[1] / "plugins" / "business-feasibility-research-guidelines"),
    )
    parser.add_argument(
        "--output-dir",
        help="Write generated PNG files here instead of the Plugin assets directory.",
    )
    args = parser.parse_args()
    asset_dir = Path(args.output_dir) if args.output_dir else Path(args.plugin_root) / "assets"
    asset_dir.mkdir(parents=True, exist_ok=True)
    render(256).save(asset_dir / "icon.png", optimize=True)
    render(1024).save(asset_dir / "logo.png", optimize=True)
    print(asset_dir / "icon.png")
    print(asset_dir / "logo.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
