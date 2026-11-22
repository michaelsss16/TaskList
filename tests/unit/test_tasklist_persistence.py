import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class TestTaskListPersistence(unittest.TestCase):
	def test_persistence_contract_is_preserved_in_source(self):
		source = (ROOT / "addon" / "globalPlugins" / "TaskList" / "__init__.py").read_text(encoding="utf-8")
		self.assertIn("taskListData.json", source)
		self.assertIn("taskListData.json.bak", source)
		self.assertIn(".tmp", source)
		self.assertIn('"soundEnabled"', source)
		self.assertIn('"recentReadCount"', source)

	def test_legacy_formats_are_documented_and_implemented(self):
		source = (ROOT / "addon" / "globalPlugins" / "TaskList" / "__init__.py").read_text(encoding="utf-8")
		for value in ("principal", "acompanhamento", "completas"):
			self.assertIn(value, source)
		self.assertIn("normalizeTask", source)
