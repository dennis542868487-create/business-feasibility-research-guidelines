from __future__ import annotations

import sys
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_brand_assets as brand  # noqa: E402


class BrandAssetTests(unittest.TestCase):
    def test_committed_icon_matches_rendered_pixels(self):
        self.assert_matches_render(256, "icon.png")

    def test_committed_logo_matches_rendered_pixels(self):
        self.assert_matches_render(1024, "logo.png")

    def assert_matches_render(self, size: int, filename: str):
        generated = brand.render(size).convert("RGBA")
        path = ROOT / "plugins" / "business-feasibility-research-guidelines" / "assets" / filename
        with Image.open(path) as committed:
            committed_rgba = committed.convert("RGBA")
            self.assertEqual(generated.size, committed_rgba.size)
            self.assertEqual(generated.tobytes(), committed_rgba.tobytes())
