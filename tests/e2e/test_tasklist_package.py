import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class TestTaskListPackage(unittest.TestCase):
	def test_generated_manifest_metadata(self):
		manifest = (ROOT / "addon" / "manifest.ini").read_text(encoding="utf-8")
		self.assertIn("name = TaskList", manifest)
		self.assertIn("summary =", manifest)
		self.assertIn("description =", manifest)
		self.assertIn("version = 1.0.0", manifest)
		self.assertIn("minimumNVDAVersion = 2026.3", manifest)
		self.assertNotIn("ClipBoardEditor", manifest)

	def test_package_source_paths_and_documentation_exist(self):
		self.assertTrue((ROOT / "addon" / "globalPlugins" / "TaskList" / "__init__.py").is_file())
		self.assertTrue((ROOT / "addon" / "doc" / "pt_BR" / "readme.md").is_file())
		self.assertTrue((ROOT / "readme.md").is_file())
