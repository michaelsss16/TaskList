import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class TestTaskListTasks(unittest.TestCase):
	def test_task_fields_and_priority_contract_exist(self):
		source = (ROOT / "addon" / "globalPlugins" / "TaskList" / "__init__.py").read_text(encoding="utf-8")
		for field in ("text", "priority", "notes", "created_at", "completed_at", "origin_list"):
			self.assertIn(field, source)
		for priority in ("Normal", "Baixa", "Média", "Alta"):
			self.assertIn(priority, source)
