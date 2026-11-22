import os
import shutil
import json
from datetime import datetime
import wx
import globalPluginHandler
from scriptHandler import script
import globalVars
import api
import gui
import ui
import logHandler
import tones

# ============================================================
# CONSTANTES E CONFIGURAÇÕES
# ============================================================

DATA_FILE_NAME = "taskListData.json"
BACKUP_FILE_NAME = "taskListData.json.bak"

PRIORITY_SUFFIXES = {
	0: "",
	1: " [Baixa]",
	2: " [Média]",
	3: " [Alta]",
}

# ============================================================
# PERSISTÊNCIA, BACKUP E MODELAGEM DE DADOS
# ============================================================


def getDataFilePath(fileName=DATA_FILE_NAME):
	return os.path.join(globalVars.appArgs.configPath, fileName)


def makeTask(text, priority=0, notes="", created_at=None, completed_at=None, origin_list=None):
	if created_at is None:
		created_at = datetime.now().strftime("%d/%m/%Y %H:%M")
	return {
		"text": text,
		"priority": priority,  # 0: Normal, 1: Baixa, 2: Média, 3: Alta
		"notes": notes,
		"created_at": created_at,
		"completed_at": completed_at,
		"origin_list": origin_list,
	}


def normalizeTask(item):
	if isinstance(item, str):
		return makeTask(item)
	if isinstance(item, dict):
		return {
			"text": item.get("text", ""),
			"priority": item.get("priority", 0),
			"notes": item.get("notes", ""),
			"created_at": item.get("created_at", datetime.now().strftime("%d/%m/%Y %H:%M")),
			"completed_at": item.get("completed_at", None),
			"origin_list": item.get("origin_list", None),
		}
	return makeTask(str(item))


def formatTaskDisplay(task):
	text = task.get("text", "")
	priorityTag = PRIORITY_SUFFIXES.get(task.get("priority", 0), "")
	notesTag = " [com notas]" if task.get("notes", "").strip() else ""
	completedAt = task.get("completed_at")
	completedTag = f" (concluído em {completedAt})" if completedAt else ""
	return f"{text}{priorityTag}{notesTag}{completedTag}"


def sortTasksByPriority(tasks):
	"""Ordena de forma estável: Alta (3) -> Média (2) -> Baixa (1) -> Normal (0)."""
	tasks.sort(key=lambda t: t.get("priority", 0), reverse=True)


def getDefaultData():
	return {
		"settings": {
			"soundEnabled": True,
			"recentReadCount": 3,
		},
		"lists": [
			{"name": "Principal", "tasks": []},
			{"name": "Acompanhamento", "tasks": []},
			{"name": "Tarefas pessoais", "tasks": []},
			{"name": "Concluídas", "tasks": []},
		],
	}


def loadData():
	path = getDataFilePath()
	if not os.path.exists(path):
		return getDefaultData()

	try:
		with open(path, "r", encoding="utf-8") as f:
			raw = json.load(f)

		data = getDefaultData()

		# Suporte a formatos legados
		if isinstance(raw, dict) and "principal" in raw:
			data["lists"] = [
				{"name": "Principal", "tasks": [normalizeTask(t) for t in raw.get("principal", [])]},
				{
					"name": "Acompanhamento",
					"tasks": [normalizeTask(t) for t in raw.get("acompanhamento", [])],
				},
				{"name": "Tarefas pessoais", "tasks": []},
				{"name": "Concluídas", "tasks": [normalizeTask(t) for t in raw.get("completas", [])]},
			]
			return data

		if isinstance(raw, list):
			data["lists"] = [
				{
					"name": item.get("name", "Lista"),
					"tasks": [normalizeTask(t) for t in item.get("tasks", [])],
				}
				for item in raw
			]
			return data

		if isinstance(raw, dict):
			data["settings"].update(raw.get("settings", {}))
			rawLists = raw.get("lists", [])
			data["lists"] = [
				{
					"name": item.get("name", "Lista"),
					"tasks": [normalizeTask(t) for t in item.get("tasks", [])],
				}
				for item in rawLists
			]

		names = [taskList["name"] for taskList in data["lists"]]
		if "Principal" not in names:
			data["lists"].insert(0, {"name": "Principal", "tasks": []})
		if "Concluídas" not in names:
			data["lists"].append({"name": "Concluídas", "tasks": []})

		return data
	except Exception:
		logHandler.log.error("Erro ao carregar dados do TaskList", exc_info=True)
		return getDefaultData()


def saveData(data):
	"""Gravação atômica para evitar corrupção em caso de fechamento abrupto."""
	path = getDataFilePath()
	tempPath = path + ".tmp"
	try:
		# Cria backup antes de gravar
		if os.path.exists(path):
			try:
				shutil.copy2(path, getDataFilePath(BACKUP_FILE_NAME))
			except Exception:
				pass

		with open(tempPath, "w", encoding="utf-8") as f:
			json.dump(data, f, ensure_ascii=False, indent=2)
		os.replace(tempPath, path)
	except Exception:
		logHandler.log.error("Erro ao salvar dados do TaskList", exc_info=True)
		if os.path.exists(tempPath):
			try:
				os.remove(tempPath)
			except Exception:
				pass


# ============================================================
# FEEDBACK SONORO (EARCONS)
# ============================================================


def playAudioFeedback(action, enabled=True):
	if not enabled:
		return
	try:
		if action == "complete":
			tones.beep(523, 40)
			tones.beep(784, 60)
		elif action == "reopen":
			tones.beep(784, 40)
			tones.beep(523, 60)
		elif action == "delete":
			tones.beep(400, 40)
			tones.beep(250, 60)
		elif action == "undo":
			tones.beep(300, 40)
			tones.beep(600, 60)
		elif action == "move":
			tones.beep(650, 35)
		elif action == "priority":
			tones.beep(880, 45)
	except Exception:
		pass


# ============================================================
# DIÁLOGOS AUXILIARES
# ============================================================


class TaskNotesDialog(wx.Dialog):
	"""Editor de notas adicionais para a tarefa."""

	def __init__(self, parent, taskText, currentNotes):
		super().__init__(
			parent,
			title=f"Notas da Tarefa: {taskText[:40]}",
			size=(600, 400),
			style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
		)
		sizer = wx.BoxSizer(wx.VERTICAL)

		lbl = wx.StaticText(self, label="Edite as notas (pressione Tab até OK ou Esc para cancelar):")
		sizer.Add(lbl, 0, wx.ALL, 8)

		self.textCtrl = wx.TextCtrl(self, value=currentNotes, style=wx.TE_MULTILINE | wx.HSCROLL)
		sizer.Add(self.textCtrl, 1, wx.EXPAND | wx.ALL, 8)

		btnSizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)
		sizer.Add(btnSizer, 0, wx.ALIGN_RIGHT | wx.ALL, 8)

		self.SetSizer(sizer)
		self.textCtrl.SetFocus()

	def getNotes(self):
		return self.textCtrl.GetValue().strip()


class HelpDialog(wx.Dialog):
	"""Exibição de todos os atalhos disponíveis."""

	def __init__(self, parent):
		super().__init__(
			parent,
			title="Ajuda - Atalhos do TaskList",
			size=(650, 450),
			style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
		)
		sizer = wx.BoxSizer(wx.VERTICAL)

		helpInfo = (
			"ATALHOS DAS TAREFAS:\n"
			"• Ctrl + N: Criar nova tarefa\n"
			"• Enter: Editar o texto da tarefa\n"
			"• Shift + Enter: Editar notas/detalhes da tarefa\n"
			"• Ctrl + P: Alternar prioridade (reordena automaticamente por urgência)\n"
			"• Espaço: Concluir (move para Concluídas) ou Reabrir\n"
			"• Delete: Excluir tarefa\n"
			"• Ctrl + Z: Desfazer última exclusão\n"
			"• Ctrl + C: Copiar tarefa e notas para a área de transferência\n"
			"• Ctrl + Shift + C: Copiar toda a lista atual formatada em Markdown\n"
			"• Ctrl + Setas Cima / Baixo: Reordenar tarefa verticalmente\n"
			"• Ctrl + Setas Esquerda / Direita: Mover tarefa entre as listas\n"
			"• Ctrl + F: Localizar tarefa na lista atual\n\n"
			"ATALHOS DAS LISTAS/ABAS:\n"
			"• Ctrl + 1 a 9: Ir diretamente para a lista correspondente\n"
			"• Ctrl + Tab / Ctrl + Shift + Tab: Alternar sequencialmente entre as abas\n"
			"• Ctrl + Shift + N: Criar nova lista à direita\n"
			"• F2: Renomear a lista atual\n"
			"• Ctrl + Shift + Delete: Limpar tarefas ou excluir lista\n"
			"• Ctrl + Alt + Setas Esquerda / Direita: Mover a posição da lista/aba\n"
			"• Ctrl + E: Exportar tarefas para arquivo (.txt / .md)\n"
			"• Ctrl + I: Importar tarefas de um arquivo (.txt)\n\n"
			"ATALHOS GLOBAIS (FORA DA JANELA):\n"
			"• NVDA + ç: Abrir o TaskList\n"
			"• NVDA + Shift + ç: Ouvir tarefas mais recentes da Principal\n"
			"• NVDA + Alt + ç: Adição rápida de tarefa na Principal"
		)

		textCtrl = wx.TextCtrl(self, value=helpInfo, style=wx.TE_MULTILINE | wx.TE_READONLY)
		sizer.Add(textCtrl, 1, wx.EXPAND | wx.ALL, 10)

		okBtn = wx.Button(self, wx.ID_OK, "Fechar")
		sizer.Add(okBtn, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)

		self.SetSizer(sizer)
		okBtn.SetFocus()


# ============================================================
# JANELA PRINCIPAL DE GERENCIAMENTO
# ============================================================


class TaskListDialog(wx.Dialog):
	PROTECTED_LISTS = ["Principal", "Concluídas"]

	def __init__(self, parent, data):
		super().__init__(
			parent,
			title="TaskList",
			size=(800, 560),
			style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
		)

		self.data = data
		self.settings = self.data.setdefault("settings", {"soundEnabled": True, "recentReadCount": 3})
		self.undoStack = []
		self.lastSearchTerm = ""

		# Garante que todas as listas iniciem ordenadas por prioridade
		for item in self.data["lists"]:
			sortTasksByPriority(item.get("tasks", []))

		mainSizer = wx.BoxSizer(wx.VERTICAL)

		helpText = wx.StaticText(
			self,
			label="Ctrl+1..9: Abas | Ctrl+N: Nova | Enter: Editar | Ctrl+P: Prioridade | Espaço: Concluir | F1: Ajuda",
		)
		mainSizer.Add(helpText, 0, wx.ALL, 8)

		self.notebook = wx.Notebook(self)
		self.listControls = []
		mainSizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 5)

		# Botões inferiores
		bottomSizer = wx.BoxSizer(wx.HORIZONTAL)
		helpBtn = wx.Button(self, label="Ajuda (F1)")
		exportBtn = wx.Button(self, label="Exportar (Ctrl+E)")
		importBtn = wx.Button(self, label="Importar (Ctrl+I)")
		closeBtn = wx.Button(self, wx.ID_CLOSE, "Fechar (Esc)")

		bottomSizer.Add(helpBtn, 0, wx.RIGHT, 5)
		bottomSizer.Add(exportBtn, 0, wx.RIGHT, 5)
		bottomSizer.Add(importBtn, 0, wx.RIGHT, 5)
		bottomSizer.AddStretchSpacer()
		bottomSizer.Add(closeBtn, 0)

		mainSizer.Add(bottomSizer, 0, wx.EXPAND | wx.ALL, 8)
		self.SetSizer(mainSizer)

		self.rebuildAllPages()

		# Eventos de botões
		helpBtn.Bind(wx.EVT_BUTTON, lambda evt: self.showHelp())
		exportBtn.Bind(wx.EVT_BUTTON, lambda evt: self.exportTasks())
		importBtn.Bind(wx.EVT_BUTTON, lambda evt: self.importTasks())
		closeBtn.Bind(wx.EVT_BUTTON, lambda evt: self.Close())

		self.Bind(wx.EVT_CHAR_HOOK, self.onCharHook)
		self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onPageChanged)

		if self.listControls:
			self.setListSelection(0, 0)
			self.listControls[0].SetFocus()

	# --------------------------------------------------------
	# RENDERIZAÇÃO DAS ABAS E ITENS
	# --------------------------------------------------------

	def rebuildAllPages(self, selectIndex=0):
		self.notebook.DeleteAllPages()
		self.listControls.clear()

		for item in self.data["lists"]:
			name = item["name"]
			tasks = item.get("tasks", [])
			sortTasksByPriority(tasks)

			panel = wx.Panel(self.notebook)
			panelSizer = wx.BoxSizer(wx.VERTICAL)

			listBox = wx.ListBox(panel, style=wx.LB_SINGLE)
			listBox.SetName(f"Lista de {name}")
			if tasks:
				listBox.Set([formatTaskDisplay(t) for t in tasks])

			panelSizer.Add(listBox, 1, wx.EXPAND | wx.ALL, 5)
			panel.SetSizer(panelSizer)

			self.notebook.AddPage(panel, name)
			self.listControls.append(listBox)

		target = max(0, min(selectIndex, self.notebook.GetPageCount() - 1))
		self.notebook.SetSelection(target)

	def getCurrentListIndex(self):
		return self.notebook.GetSelection()

	def getCurrentListBox(self):
		idx = self.getCurrentListIndex()
		if 0 <= idx < len(self.listControls):
			return self.listControls[idx]
		return None

	def getCurrentTasks(self):
		idx = self.getCurrentListIndex()
		if 0 <= idx < len(self.data["lists"]):
			return self.data["lists"][idx]["tasks"]
		return []

	def setListSelection(self, listIdx, itemIdx):
		if 0 <= listIdx < len(self.listControls):
			lb = self.listControls[listIdx]
			count = lb.GetCount()
			if count > 0:
				target = max(0, min(itemIdx, count - 1))
				lb.SetSelection(target)

	def onPageChanged(self, event):
		idx = self.getCurrentListIndex()
		if 0 <= idx < len(self.data["lists"]):
			listObj = self.data["lists"][idx]
			tasks = listObj.get("tasks", [])

			# Garante ordenação por prioridade sempre ao mudar de lista
			sortTasksByPriority(tasks)

			lb = self.getCurrentListBox()
			if lb:
				lb.Set([formatTaskDisplay(t) for t in tasks])

			name = listObj["name"]
			total = len(tasks)
			ui.message(f"{name}, {total} tarefas")

			if lb:
				lb.SetFocus()
				if total > 0 and lb.GetSelection() == wx.NOT_FOUND:
					lb.SetSelection(0)
		event.Skip()

	# --------------------------------------------------------
	# INTERCEPTAÇÃO GLOBAL DE TECLADO
	# --------------------------------------------------------

	def onCharHook(self, event):
		keyCode = event.GetKeyCode()
		modifiers = event.GetModifiers()
		curLb = self.getCurrentListBox()
		isListFocused = curLb is not None and self.FindFocus() == curLb

		# ----------------------------------------------------
		# NAVEGAÇÃO ENTRE ABAS: Ctrl + 1 a Ctrl + 9
		# ----------------------------------------------------
		if modifiers == wx.MOD_CONTROL:
			targetIdx = None
			if ord("1") <= keyCode <= ord("9"):
				targetIdx = keyCode - ord("1")
			elif wx.WXK_NUMPAD1 <= keyCode <= wx.WXK_NUMPAD9:
				targetIdx = keyCode - wx.WXK_NUMPAD1

			if targetIdx is not None:
				event.StopPropagation()
				if targetIdx < self.notebook.GetPageCount():
					self.notebook.SetSelection(targetIdx)
					lb = self.getCurrentListBox()
					if lb:
						lb.SetFocus()
				else:
					ui.message(f"Aba {targetIdx + 1} não existe.")
				return

		# F1: Ajuda
		if keyCode == wx.WXK_F1:
			event.StopPropagation()
			self.showHelp()
			return

		# ESC: Fechar
		if keyCode == wx.WXK_ESCAPE:
			event.StopPropagation()
			self.Close()
			return

		# F2: Renomear lista atual
		if keyCode == wx.WXK_F2:
			event.StopPropagation()
			self.renameCurrentList()
			return

		# Ctrl + Shift + N: Nova Lista
		if modifiers == (wx.MOD_CONTROL | wx.MOD_SHIFT) and keyCode in (ord("N"), ord("n")):
			event.StopPropagation()
			self.addNewList()
			return

		# Ctrl + Shift + Delete: Excluir/Limpar Lista
		if modifiers == (wx.MOD_CONTROL | wx.MOD_SHIFT) and keyCode == wx.WXK_DELETE:
			event.StopPropagation()
			self.deleteOrClearList()
			return

		# Ctrl + Alt + Esquerda / Direita: Reordenar abas
		if (modifiers == (wx.MOD_CONTROL | wx.MOD_ALT)) and keyCode in (wx.WXK_LEFT, wx.WXK_RIGHT):
			event.StopPropagation()
			self.moveTab(direction=-1 if keyCode == wx.WXK_LEFT else 1)
			return

		# Ctrl + E: Exportar
		if modifiers == wx.MOD_CONTROL and keyCode in (ord("E"), ord("e")):
			event.StopPropagation()
			self.exportTasks()
			return

		# Ctrl + I: Importar
		if modifiers == wx.MOD_CONTROL and keyCode in (ord("I"), ord("i")):
			event.StopPropagation()
			self.importTasks()
			return

		# Ctrl + Shift + C: Copiar lista inteira em Markdown
		if modifiers == (wx.MOD_CONTROL | wx.MOD_SHIFT) and keyCode in (ord("C"), ord("c")):
			event.StopPropagation()
			self.copyEntireList()
			return

		# Ações exclusivas com foco na lista de itens
		if isListFocused:
			curIdx = self.getCurrentListIndex()
			sel = curLb.GetSelection()
			tasks = self.getCurrentTasks()

			# Shift + Enter: Editar Notas da Tarefa
			if modifiers == wx.MOD_SHIFT and keyCode in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
				event.StopPropagation()
				if sel != wx.NOT_FOUND and sel < len(tasks):
					self.editTaskNotes(curIdx, sel)
				return

			# Enter: Editar Texto da Tarefa
			if modifiers == 0 and keyCode in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
				event.StopPropagation()
				if sel != wx.NOT_FOUND and sel < len(tasks):
					self.editTask(curIdx, sel)
				return

			# Ctrl + N: Nova Tarefa
			if modifiers == wx.MOD_CONTROL and keyCode in (ord("N"), ord("n")):
				event.StopPropagation()
				self.addTask(curIdx, sel)
				return

			# Espaço: Concluir ou Reabrir
			if modifiers == 0 and keyCode == wx.WXK_SPACE:
				event.StopPropagation()
				if sel != wx.NOT_FOUND and sel < len(tasks):
					self.toggleComplete(curIdx, sel)
				return

			# Ctrl + P: Alternar Prioridade
			if modifiers == wx.MOD_CONTROL and keyCode in (ord("P"), ord("p")):
				event.StopPropagation()
				if sel != wx.NOT_FOUND and sel < len(tasks):
					self.cyclePriority(curIdx, sel)
				return

			# Delete: Excluir Tarefa
			if modifiers == 0 and keyCode == wx.WXK_DELETE:
				event.StopPropagation()
				if sel != wx.NOT_FOUND and sel < len(tasks):
					self.deleteTask(curIdx, sel)
				return

			# Ctrl + Z: Desfazer
			if modifiers == wx.MOD_CONTROL and keyCode in (ord("Z"), ord("z")):
				event.StopPropagation()
				self.undoDelete()
				return

			# Ctrl + C: Copiar tarefa selecionada
			if modifiers == wx.MOD_CONTROL and keyCode in (ord("C"), ord("c")):
				event.StopPropagation()
				if sel != wx.NOT_FOUND and sel < len(tasks):
					self.copyCurrentTask(curIdx, sel)
				return

			# Ctrl + F: Buscar tarefa
			if modifiers == wx.MOD_CONTROL and keyCode in (ord("F"), ord("f")):
				event.StopPropagation()
				self.searchTask()
				return

			# Ctrl + Cima / Baixo: Mover manualmente na lista
			if modifiers == wx.MOD_CONTROL and keyCode in (wx.WXK_UP, wx.WXK_DOWN):
				event.StopPropagation()
				if sel != wx.NOT_FOUND:
					self.moveTaskVertical(curIdx, sel, -1 if keyCode == wx.WXK_UP else 1)
				return

			# Ctrl + Esquerda / Direita: Mover entre listas
			if modifiers == wx.MOD_CONTROL and keyCode in (wx.WXK_LEFT, wx.WXK_RIGHT):
				event.StopPropagation()
				if sel != wx.NOT_FOUND and sel < len(tasks):
					self.moveTaskHorizontal(curIdx, sel, -1 if keyCode == wx.WXK_LEFT else 1)
				return

		event.Skip()

	# --------------------------------------------------------
	# AÇÕES DE TAREFAS
	# --------------------------------------------------------

	def addTask(self, curIdx, currentIndex):
		entryDlg = wx.TextEntryDialog(self, "Digite a nova tarefa:", "Nova Tarefa")
		if entryDlg.ShowModal() == wx.ID_OK:
			text = entryDlg.GetValue().strip()
			if text:
				tasks = self.getCurrentTasks()
				newTask = makeTask(text)
				tasks.append(newTask)
				sortTasksByPriority(tasks)

				newIndex = next(i for i, t in enumerate(tasks) if t is newTask)
				lb = self.listControls[curIdx]
				lb.Set([formatTaskDisplay(t) for t in tasks])
				self.setListSelection(curIdx, newIndex)

				playAudioFeedback("move", self.settings.get("soundEnabled", True))
				ui.message(f"Adicionada: {text}")
		entryDlg.Destroy()

	def editTask(self, curIdx, index):
		task = self.getCurrentTasks()[index]
		entryDlg = wx.TextEntryDialog(self, "Editar tarefa:", "Editar Tarefa", value=task["text"])
		if entryDlg.ShowModal() == wx.ID_OK:
			newText = entryDlg.GetValue().strip()
			if newText and newText != task["text"]:
				task["text"] = newText
				lb = self.listControls[curIdx]
				lb.SetString(index, formatTaskDisplay(task))
				lb.SetSelection(index)
				ui.message(f"Atualizada: {newText}")
		entryDlg.Destroy()

	def editTaskNotes(self, curIdx, index):
		task = self.getCurrentTasks()[index]
		dlg = TaskNotesDialog(self, task["text"], task.get("notes", ""))
		if dlg.ShowModal() == wx.ID_OK:
			task["notes"] = dlg.getNotes()
			lb = self.listControls[curIdx]
			lb.SetString(index, formatTaskDisplay(task))
			lb.SetSelection(index)
			ui.message("Notas atualizadas.")
		dlg.Destroy()

	def cyclePriority(self, curIdx, index):
		tasks = self.getCurrentTasks()
		task = tasks[index]
		currentP = task.get("priority", 0)
		nextP = (currentP + 1) % 4
		task["priority"] = nextP

		# Reordena por prioridade mantendo estabilidade
		sortTasksByPriority(tasks)
		newIndex = next(i for i, t in enumerate(tasks) if t is task)

		lb = self.listControls[curIdx]
		lb.Set([formatTaskDisplay(t) for t in tasks])
		lb.SetSelection(newIndex)

		playAudioFeedback("priority", self.settings.get("soundEnabled", True))
		pNames = {0: "Normal", 1: "Baixa", 2: "Média", 3: "Alta"}
		ui.message(f"Prioridade: {pNames[nextP]}, posição {newIndex + 1} de {len(tasks)}")

	def toggleComplete(self, curIdx, index):
		task = self.getCurrentTasks().pop(index)
		lbCur = self.listControls[curIdx]
		lbCur.Delete(index)

		curName = self.data["lists"][curIdx]["name"]

		if curName == "Concluídas":
			targetName = task.get("origin_list") or "Principal"
			task["completed_at"] = None
			actionSound = "reopen"
		else:
			task["origin_list"] = curName
			targetName = "Concluídas"
			task["completed_at"] = datetime.now().strftime("%d/%m/%Y %H:%M")
			actionSound = "complete"

		targetIdx = next((i for i, item in enumerate(self.data["lists"]) if item["name"] == targetName), None)
		if targetIdx is None:
			targetIdx = 0

		targetTasks = self.data["lists"][targetIdx]["tasks"]
		targetTasks.append(task)
		sortTasksByPriority(targetTasks)

		self.listControls[targetIdx].Set([formatTaskDisplay(t) for t in targetTasks])

		playAudioFeedback(actionSound, self.settings.get("soundEnabled", True))
		if targetName == "Concluídas":
			ui.message(f"Concluída: {task['text']}")
		else:
			ui.message(f"Reaberta para {self.data['lists'][targetIdx]['name']}: {task['text']}")

		self.setListSelection(curIdx, index)

	def deleteTask(self, curIdx, index):
		listName = self.data["lists"][curIdx]["name"]
		task = self.getCurrentTasks().pop(index)
		self.undoStack.append((listName, index, task))
		self.listControls[curIdx].Delete(index)
		self.setListSelection(curIdx, index)

		playAudioFeedback("delete", self.settings.get("soundEnabled", True))
		ui.message("Excluída. Pressione Ctrl+Z para desfazer.")

	def undoDelete(self):
		if not self.undoStack:
			ui.message("Nada para desfazer.")
			return

		targetListName, targetIndex, task = self.undoStack.pop()
		targetIdx = next(
			(i for i, item in enumerate(self.data["lists"]) if item["name"] == targetListName), None
		)
		if targetIdx is None:
			targetIdx = self.getCurrentListIndex()

		tasks = self.data["lists"][targetIdx]["tasks"]
		insertPos = min(targetIndex, len(tasks))
		tasks.insert(insertPos, task)
		sortTasksByPriority(tasks)

		newIndex = next(i for i, t in enumerate(tasks) if t is task)

		lb = self.listControls[targetIdx]
		lb.Set([formatTaskDisplay(t) for t in tasks])

		self.notebook.SetSelection(targetIdx)
		self.setListSelection(targetIdx, newIndex)
		lb.SetFocus()

		playAudioFeedback("undo", self.settings.get("soundEnabled", True))
		ui.message(f"Restaurada em {self.data['lists'][targetIdx]['name']}: {task['text']}")

	def copyCurrentTask(self, curIdx, index):
		task = self.getCurrentTasks()[index]
		text = task["text"]
		if task.get("priority", 0) > 0:
			text += PRIORITY_SUFFIXES.get(task["priority"], "")
		if task.get("notes"):
			text += f"\nNotas:\n{task['notes']}"
		api.copyToClip(text)
		ui.message("Tarefa copiada para a área de transferência.")

	def copyEntireList(self):
		curIdx = self.getCurrentListIndex()
		listName = self.data["lists"][curIdx]["name"]
		tasks = self.getCurrentTasks()
		if not tasks:
			ui.message("Lista vazia.")
			return

		isDone = listName == "Concluídas"
		lines = [f"# {listName}\n"]
		for idx, t in enumerate(tasks, 1):
			box = "[x]" if isDone else "[ ]"
			line = f"{idx}. {box} {formatTaskDisplay(t)}"
			if t.get("notes"):
				line += f"\n   * Notas: {t['notes']}"
			lines.append(line)

		api.copyToClip("\n".join(lines))
		ui.message(f"Todas as tarefas de {listName} copiadas.")

	def searchTask(self):
		entryDlg = wx.TextEntryDialog(
			self, "Digite o termo para buscar:", "Buscar Tarefa", value=self.lastSearchTerm
		)
		if entryDlg.ShowModal() == wx.ID_OK:
			term = entryDlg.GetValue().strip().lower()
			if term:
				self.lastSearchTerm = term
				tasks = self.getCurrentTasks()
				curLb = self.getCurrentListBox()
				startPos = (curLb.GetSelection() + 1) if curLb.GetSelection() != wx.NOT_FOUND else 0

				indices = list(range(startPos, len(tasks))) + list(range(0, startPos))
				for i in indices:
					t = tasks[i]
					if term in t["text"].lower() or term in t.get("notes", "").lower():
						curLb.SetSelection(i)
						playAudioFeedback("move", self.settings.get("soundEnabled", True))
						ui.message(f"Encontrada ({i + 1} de {len(tasks)}): {formatTaskDisplay(t)}")
						entryDlg.Destroy()
						return
				ui.message("Nenhuma tarefa correspondente encontrada.")
		entryDlg.Destroy()

	def moveTaskVertical(self, curIdx, index, direction):
		tasks = self.getCurrentTasks()
		newIndex = index + direction
		if newIndex < 0 or newIndex >= len(tasks):
			return

		task = tasks.pop(index)
		tasks.insert(newIndex, task)

		lb = self.listControls[curIdx]
		lb.Delete(index)
		lb.Insert(formatTaskDisplay(task), newIndex)
		lb.SetSelection(newIndex)

		playAudioFeedback("move", self.settings.get("soundEnabled", True))
		ui.message(f"Posição {newIndex + 1} de {len(tasks)}")

	def moveTaskHorizontal(self, curIdx, index, direction):
		targetIdx = curIdx + direction
		if 0 <= targetIdx < len(self.data["lists"]):
			task = self.getCurrentTasks().pop(index)
			self.listControls[curIdx].Delete(index)

			targetTasks = self.data["lists"][targetIdx]["tasks"]
			targetTasks.append(task)
			sortTasksByPriority(targetTasks)

			self.listControls[targetIdx].Set([formatTaskDisplay(t) for t in targetTasks])

			self.setListSelection(curIdx, index)
			playAudioFeedback("move", self.settings.get("soundEnabled", True))
			ui.message(f"Movida para {self.data['lists'][targetIdx]['name']}: {task['text']}")

	# --------------------------------------------------------
	# GERENCIAMENTO DE ABAS/LISTAS
	# --------------------------------------------------------

	def addNewList(self):
		curIdx = self.getCurrentListIndex()
		entryDlg = wx.TextEntryDialog(self, "Nome da nova lista:", "Nova Lista")
		if entryDlg.ShowModal() == wx.ID_OK:
			name = entryDlg.GetValue().strip()
			if name:
				insertIdx = curIdx + 1
				self.data["lists"].insert(insertIdx, {"name": name, "tasks": []})
				self.rebuildAllPages(selectIndex=insertIdx)
				self.listControls[insertIdx].SetFocus()
				ui.message(f"Lista criada: {name}")
		entryDlg.Destroy()

	def renameCurrentList(self):
		curIdx = self.getCurrentListIndex()
		listObj = self.data["lists"][curIdx]
		oldName = listObj["name"]

		if oldName in self.PROTECTED_LISTS:
			ui.message(f"A lista '{oldName}' não pode ser renomeada.")
			return

		entryDlg = wx.TextEntryDialog(self, "Novo nome para a lista:", "Renomear Lista", value=oldName)
		if entryDlg.ShowModal() == wx.ID_OK:
			newName = entryDlg.GetValue().strip()
			if newName and newName != oldName:
				listObj["name"] = newName
				self.notebook.SetPageText(curIdx, newName)
				self.listControls[curIdx].SetName(f"Lista de {newName}")
				ui.message(f"Lista renomeada para: {newName}")
		entryDlg.Destroy()

	def moveTab(self, direction):
		curIdx = self.getCurrentListIndex()
		newIdx = curIdx + direction
		if 0 <= newIdx < len(self.data["lists"]):
			listObj = self.data["lists"].pop(curIdx)
			self.data["lists"].insert(newIdx, listObj)
			self.rebuildAllPages(selectIndex=newIdx)
			self.listControls[newIdx].SetFocus()
			playAudioFeedback("move", self.settings.get("soundEnabled", True))
			ui.message(f"Aba {listObj['name']} movida para posição {newIdx + 1}")

	def deleteOrClearList(self):
		curIdx = self.getCurrentListIndex()
		listObj = self.data["lists"][curIdx]
		listName = listObj["name"]

		if listName in self.PROTECTED_LISTS:
			confirm = wx.MessageBox(
				f"A lista '{listName}' não pode ser excluída.\nDeseja apagar todas as tarefas dela?",
				"Limpar tarefas",
				wx.YES_NO | wx.ICON_QUESTION | wx.NO_DEFAULT,
				self,
			)
			if confirm == wx.YES:
				listObj["tasks"].clear()
				self.listControls[curIdx].Clear()
				playAudioFeedback("delete", self.settings.get("soundEnabled", True))
				ui.message(f"Todas as tarefas de {listName} foram apagadas.")
			return

		confirm = wx.MessageBox(
			f"Deseja realmente excluir a lista '{listName}' e todas as suas tarefas?",
			"Excluir lista",
			wx.YES_NO | wx.ICON_WARNING | wx.NO_DEFAULT,
			self,
		)
		if confirm == wx.YES:
			self.data["lists"].pop(curIdx)
			newIndex = max(0, curIdx - 1)
			self.rebuildAllPages(selectIndex=newIndex)
			if self.listControls:
				self.listControls[newIndex].SetFocus()
			playAudioFeedback("delete", self.settings.get("soundEnabled", True))
			ui.message(f"Lista '{listName}' excluída.")

	# --------------------------------------------------------
	# IMPORTAÇÃO E EXPORTAÇÃO
	# --------------------------------------------------------

	def exportTasks(self):
		fileDlg = wx.FileDialog(
			self,
			message="Exportar tarefas",
			wildcard="Arquivo de Texto (*.txt)|*.txt|Markdown (*.md)|*.md",
			style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
		)
		if fileDlg.ShowModal() == wx.ID_OK:
			filePath = fileDlg.GetPath()
			try:
				with open(filePath, "w", encoding="utf-8") as f:
					for taskList in self.data["lists"]:
						f.write(f"=== {taskList['name']} ===\n")
						for t in taskList.get("tasks", []):
							line = f"- {formatTaskDisplay(t)}"
							f.write(line + "\n")
							if t.get("notes"):
								f.write(f"  Notas: {t['notes']}\n")
						f.write("\n")
				ui.message("Tarefas exportadas com sucesso!")
			except Exception:
				logHandler.log.error("Erro ao exportar tarefas", exc_info=True)
				ui.message("Erro ao exportar tarefas.")
		fileDlg.Destroy()

	def importTasks(self):
		fileDlg = wx.FileDialog(
			self,
			message="Importar tarefas para a lista atual",
			wildcard="Arquivo de Texto (*.txt)|*.txt",
			style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
		)
		if fileDlg.ShowModal() == wx.ID_OK:
			filePath = fileDlg.GetPath()
			try:
				with open(filePath, "r", encoding="utf-8") as f:
					lines = [line.strip() for line in f.readlines() if line.strip()]

				curIdx = self.getCurrentListIndex()
				tasks = self.getCurrentTasks()

				for line in lines:
					cleanText = line.lstrip("-*0123456789. ")
					if cleanText:
						tasks.append(makeTask(cleanText))

				sortTasksByPriority(tasks)
				self.listControls[curIdx].Set([formatTaskDisplay(t) for t in tasks])

				ui.message(f"{len(lines)} tarefas importadas para {self.data['lists'][curIdx]['name']}!")
			except Exception:
				logHandler.log.error("Erro ao importar tarefas", exc_info=True)
				ui.message("Erro ao importar arquivo.")
		fileDlg.Destroy()

	def showHelp(self):
		dlg = HelpDialog(self)
		dlg.ShowModal()
		dlg.Destroy()


# ============================================================
# PLUGIN GLOBAL
# ============================================================


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	scriptCategory = "TaskList"

	def __init__(self):
		super().__init__()
		self.activeDialog = None

	# --------------------------------------------------------
	# ATALHOS GLOBAIS
	# --------------------------------------------------------

	@script(
		description="Abre a janela principal do gerenciador de tarefas",
		gesture="kb:NVDA+ç",
	)
	def script_openTaskList(self, gesture):
		wx.CallAfter(self.openDialog)

	@script(
		description="Lê em voz alta as tarefas mais recentes da lista principal",
		gesture="kb:NVDA+shift+ç",
	)
	def script_readRecentTasks(self, gesture):
		# Se a janela estiver aberta, usa os dados em memória; senão, carrega do disco
		if self.activeDialog is not None:
			data = self.activeDialog.data
		else:
			data = loadData()

		pList = next((taskList for taskList in data["lists"] if taskList["name"] == "Principal"), None)
		tasks = pList["tasks"] if pList else []

		if not tasks:
			ui.message("Lista principal vazia.")
			return

		sortTasksByPriority(tasks)
		count = data.get("settings", {}).get("recentReadCount", 3)
		top = tasks[:count]
		total = len(tasks)

		parts = [f"{i}: {formatTaskDisplay(t)}" for i, t in enumerate(top, 1)]
		ui.message(f"Principal ({total} tarefas): " + " | ".join(parts))

	@script(
		description="Adiciona rapidamente uma nova tarefa à lista principal",
		gesture="kb:NVDA+alt+ç",
	)
	def script_quickAddTask(self, gesture):
		def _prompt():
			parent = self.activeDialog if self.activeDialog is not None else gui.mainFrame
			dlg = wx.TextEntryDialog(parent, "Digite a tarefa para a lista Principal:", "Tarefa Rápida")
			if dlg.ShowModal() == wx.ID_OK:
				text = dlg.GetValue().strip()
				if text:
					newTask = makeTask(text)
					if self.activeDialog is not None:
						# Sincroniza diretamente na janela ativa
						pList = next(
							(
								taskList
								for taskList in self.activeDialog.data["lists"]
								if taskList["name"] == "Principal"
							),
							None,
						)
						if pList is not None:
							pList["tasks"].append(newTask)
							sortTasksByPriority(pList["tasks"])
							pIdx = next(
								i
								for i, taskList in enumerate(self.activeDialog.data["lists"])
								if taskList["name"] == "Principal"
							)
							self.activeDialog.listControls[pIdx].Set(
								[formatTaskDisplay(t) for t in pList["tasks"]]
							)
						saveData(self.activeDialog.data)
					else:
						# Salva direto no arquivo
						data = loadData()
						pList = next(
							(taskList for taskList in data["lists"] if taskList["name"] == "Principal"),
							None,
						)
						if pList is not None:
							pList["tasks"].append(newTask)
							sortTasksByPriority(pList["tasks"])
							saveData(data)

					playAudioFeedback("move", True)
					ui.message(f"Adicionada na Principal: {text}")
			dlg.Destroy()

		wx.CallAfter(_prompt)

	# --------------------------------------------------------
	# ABERTURA DA JANELA
	# --------------------------------------------------------

	def openDialog(self):
		if self.activeDialog is not None:
			self.activeDialog.Raise()
			self.activeDialog.SetFocus()
			return

		data = loadData()
		dialog = None
		try:
			dialog = TaskListDialog(gui.mainFrame, data)
			self.activeDialog = dialog
			dialog.ShowModal()
		except Exception:
			logHandler.log.error("Erro no TaskListDialog", exc_info=True)
			ui.message("Erro ao abrir lista de tarefas.")
		finally:
			if dialog is not None:
				saveData(dialog.data)
				if self.activeDialog is dialog:
					self.activeDialog = None
				dialog.Destroy()

	def terminate(self):
		if self.activeDialog is not None:
			try:
				saveData(self.activeDialog.data)
				self.activeDialog.EndModal(wx.ID_CANCEL)
			except Exception:
				pass
		super().terminate()
