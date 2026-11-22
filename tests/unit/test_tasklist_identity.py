import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class TestTaskListIdentity(unittest.TestCase):
	def test_plugin_identity_and_window_are_tasklist(self):
		source = (ROOT / "addon" / "globalPlugins" / "TaskList" / "__init__.py").read_text(encoding="utf-8")
		self.assertIn('scriptCategory = "TaskList"', source)
		self.assertIn('title="TaskList"', source)
		self.assertIn("NVDA+ç", source)
		self.assertIn("NVDA+shift+ç", source)
		self.assertIn("NVDA+alt+ç", source)

	def test_build_metadata_matches_tasklist(self):
		build_vars = (ROOT / "buildVars.py").read_text(encoding="utf-8")
		self.assertIn('addon_name="TaskList"', build_vars)
		self.assertIn('addon_version="1.0.0"', build_vars)
		self.assertIn("addon/globalPlugins/TaskList/*.py", build_vars)
		self.assertNotIn("addon/globalPlugins/ClipBoardEditor", build_vars)
