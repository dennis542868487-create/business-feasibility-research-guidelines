from __future__ import annotations

import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_release_packages import build  # noqa: E402
from validate_repository import validate_repository  # noqa: E402


class RepositoryTests(unittest.TestCase):
    def test_repository_validation(self):
        self.assertEqual(validate_repository(ROOT), [])

    def test_release_archive_roots(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            artifacts = build(Path(temp_dir))
            self.assertEqual(len(artifacts), 4)
            plugin_zip = next(path for path in artifacts if path.name.endswith("-plugin.zip"))
            standalone_zip = next(path for path in artifacts if path.name.endswith("-standalone-skill.zip"))
            manual_zip = next(path for path in artifacts if path.name.endswith("-manual-mode.zip"))
            with zipfile.ZipFile(plugin_zip) as archive:
                names = archive.namelist()
                self.assertTrue(all(name.startswith("business-feasibility-research-guidelines/") for name in names))
                self.assertIn("business-feasibility-research-guidelines/.codex-plugin/plugin.json", names)
            with zipfile.ZipFile(standalone_zip) as archive:
                names = archive.namelist()
                self.assertIn("business-feasibility-research-guidelines/SKILL.md", names)
                self.assertFalse(any("evidence-source-audit" in name for name in names))
            with zipfile.ZipFile(manual_zip) as archive:
                names = archive.namelist()
                self.assertIn("business-feasibility-research-guidelines-manual-mode/manual-mode.md", names)
                self.assertTrue(any(name.endswith("templates/evidence-ledger.csv") for name in names))


if __name__ == "__main__":
    unittest.main()
