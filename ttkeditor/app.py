# MIT License
#
# Copyright (c) 2024 Guillermo A. Molina <guillermoadrianmolina AT gmail DOT com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os

from TermTk import TTkK
from TermTk import TTkCfg
from TermTk import TTkColor
from TermTk import TTkHelper
from TermTk import TTkString
from TermTk import TTkKodeTab
from TermTk import TTkAbout
from TermTk import TTkFileDialogPicker
from TermTk import TTkFileTree
from TermTk import TTkTextEdit
from TermTk import TTkShortcut
from TermTk import TTkSplitter
from TermTk import TTkGridLayout
from TermTk import TTkFrame
from TermTk import TTkMenuBarLayout
from TermTk import pyTTkSlot

from .config import *
from .about import *
from .texteditview import TTKEditorTextEditView
from .textdocument import TTKEditorTextDocument
from .statusbarlayout import TTkEditorStatusBarLayout
from .frame import TTkStatusFrame


class TTkEditorApp(TTkStatusFrame):
    __slots__ = ('_modified', '_kodeTab', '_documents')

    def __init__(self, files=None, border=True, *args, **kwargs):
        self._documents = {}
        self._modified = False

        super().__init__(border=border, **kwargs)

        def _closeFile():
            if (index := self._kodeTab.lastUsed.currentIndex()) >= 0:
                self._kodeTab.lastUsed.removeTab(index)

        def _showAbout(btn):
            TTkHelper.overlay(None, TTKEditorAbout(), 30, 10)

        def _showAboutTTk(btn):
            TTkHelper.overlay(None, TTkAbout(), 30, 10)

        appMenuBar = TTkMenuBarLayout()
        self.setMenuBar(appMenuBar)

        fileMenu = appMenuBar.addMenu("&File")
        fileMenu.addMenu("Open").menuButtonClicked.connect(
            self._showFileDialog)
        fileMenu.addMenu("Close").menuButtonClicked.connect(_closeFile)
        fileMenu.addMenu("E&xit Alt+X").menuButtonClicked.connect(self._quit)
        TTkShortcut(TTkK.ALT | TTkK.Key_X).activated.connect(self._quit)

        editMenu = appMenuBar.addMenu("&Edit")
        editMenu.addMenu("Search")
        editMenu.addMenu("Replace")

        helpMenu = appMenuBar.addMenu(
            "&Help", alignment=TTkK.RIGHT_ALIGN)
        helpMenu.addMenu("About ...").menuButtonClicked.connect(_showAbout)
        helpMenu.addMenu("About ttk").menuButtonClicked.connect(_showAboutTTk)

        self.setStatusBar(statusBar := TTkEditorStatusBarLayout())
        statusBar.addLabel("ONLINE")

        fileTree = TTkFileTree(path='.')
        fileTree.fileActivated.connect(lambda x: self._openFile(x.path()))
        self._kodeTab = TTkKodeTab(border=False, closable=True)

        self.setLayout(TTkGridLayout())
        self.addWidget(splitter := TTkSplitter())
        splitter.addWidget(fileTree, 20)
        splitter.addWidget(self._kodeTab)

        if files is not None:
            for file in files:
                self._openFile(file)

    pyTTkSlot()

    def _showFileDialog(self):
        filePicker = TTkFileDialogPicker(pos=(3, 3), size=(75, 24), caption="Pick Something", path=".", fileMode=TTkK.FileMode.AnyFile,
                                         filter="All Files (*);;Python Files (*.py);;Bash scripts (*.sh);;Markdown Files (*.md)")
        filePicker.pathPicked.connect(self._openFile)
        TTkHelper.overlay(None, filePicker, 20, 5, True)

    def _openFile(self, filePath):
        filePath = os.path.realpath(filePath)
        if filePath in self._documents:
            doc = self._documents[filePath]['doc']
        else:
            with open(filePath, 'r') as f:
                content = f.read()
            doc = TTKEditorTextDocument(text=content, filePath=filePath)
            self._documents[filePath] = {'doc': doc, 'tabs': []}
        tview = TTKEditorTextEditView(document=doc, readOnly=False)
        tedit = TTkTextEdit(textEditView=tview,
                            lineNumber=True, lineNumberStarting=1)
        doc.kodeHighlightUpdate.connect(tedit.update)
        label = TTkString(TTkCfg.theme.fileIcon.getIcon(
            filePath), TTkCfg.theme.fileIconColor) + TTkColor.RST + " " + os.path.basename(filePath)

        self._kodeTab.addTab(tedit, label)
        self._kodeTab.setCurrentWidget(tedit)

    def modified(self):
        return self._modified

    def setModified(self, modified):
        # if self._modified == modified: return
        self._modified = modified
        if modified:
            self._fileNameLabel.setText(f"( ● {self._fileName} )")
        else:
            self._fileNameLabel.setText(f"( {self._fileName} )")
            self._snapSaved = self._snapId

    def _quit(self):
        if self.modified():
            self.askToSave(
                TTkString(
                    f'Do you want to save the changes to this document before closing?\nIf you don\'t save, your changes will be lost.', TTkColor.BOLD),
                cb=TTkHelper.quit)
        else:
            TTkHelper.quit()

    def isVisible(self):
        return True
