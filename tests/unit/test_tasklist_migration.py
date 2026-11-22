import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FORBIDDEN = ("ClipBoardEditor", "Editor da área de transferência")
SEARCH_ROOTS = (
	"addon",
	"buildVars.py",
	"pyproject.toml",
	"sconstruct",
	"readme.md",
	"changelog.md",
	"DocumentaçãoTecnica.md",
)


class TestTaskListMigration(unittest.TestCase):
	def test_no_old_identity_in_distributed_sources(self):
		for relative in SEARCH_ROOTS:
			path = ROOT / relative
			files = (
				[path]
				if path.is_file()
				else [
					item
					for item in path.rglob("*")
					if item.is_file() and item.suffix.lower() in {".py", ".ini", ".toml", ".md", ".html"}
				]
			)
			for file in files:
				if "specs" in file.parts:
					continue
				content = file.read_text(encoding="utf-8", errors="ignore")
				for forbidden in FORBIDDEN:
					self.assertNotIn(forbidden, content, f"{forbidden} encontrado em {file}")

	def test_plugin_directory_has_no_old_source_directory(self):
		self.assertTrue((ROOT / "addon" / "globalPlugins" / "TaskList" / "__init__.py").is_file())
		self.assertFalse((ROOT / "addon" / "globalPlugins" / "ClipBoardEditor").exists())
