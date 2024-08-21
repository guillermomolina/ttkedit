# Copyright 2024, Guillermo Adrián Molina
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os

from TermTk import TTkK
from TermTk import TTkCfg
from TermTk import TTkColor
from TermTk import TTkHelper
from TermTk import TTkString
from TermTk import TTkMenuBarLayout
from TermTk import TTkKodeTab
from TermTk import TTkAbout
from TermTk import TTkFileDialogPicker
from TermTk import TTkFileTree
from TermTk import TTkTextEdit
from TermTk import TTkLabel
from TermTk import TTkAppTemplate
from TermTk import TTkShortcut
from TermTk import pyTTkSlot

from .config import *
from .about import *
from .texteditview import TTkEditTextEditView
from .textdocument import TTkEditTextDocument


class TTkEdit(TTkAppTemplate):
    __slots__ = ('_toolBar', '_fileNameLabel', '_modified',
                 '_sigslotEditor', '_treeInspector', '_windowEditor', '_notepad',
                 '_fileName', '_currentPath',
                 '_snapshot', '_snapId', '_snapSaved',
                 # Signals
                 'weModified', 'thingSelected', 'widgetNameChanged'
                 '_kodeTab', '_documents')

    def __init__(self, files=None, *args, **kwargs):
        self._documents = {}
        self._modified = False

        super().__init__(**kwargs)
        appTemplate = self

        appTemplate.setMenuBar(
            appMenuBar := TTkMenuBarLayout(), TTkAppTemplate.HEADER)

        fileMenu = appMenuBar.addMenu("&File")
        fileMenu.addMenu("&Open").menuButtonClicked.connect(
            self._showFileDialog)
        fileMenu.addMenu("&Close")
        fileMenu.addMenu("E&xit Alt+X").menuButtonClicked.connect(self._quit)

        editMenu = appMenuBar.addMenu("&Edit")
        editMenu.addMenu("Search")
        editMenu.addMenu("Replace")

        def _showAbout(btn):
            TTkHelper.overlay(None, TTkEditAbout(), 30, 10)

        def _showAboutTTk(btn):
            TTkHelper.overlay(None, TTkAbout(), 30, 10)

        helpMenu = appMenuBar.addMenu("&Help", alignment=TTkK.RIGHT_ALIGN)
        helpMenu.addMenu("About ...").menuButtonClicked.connect(_showAbout)
        helpMenu.addMenu("About ttk").menuButtonClicked.connect(_showAboutTTk)

        fileTree = TTkFileTree(path='.')
        appTemplate.setWidget(fileTree, TTkAppTemplate.LEFT, 25)

        if files is not None:
            for file in files:
                self._openFile(file)

        fileTree.fileActivated.connect(lambda x: self._openFile(x.path()))

        self._kodeTab = TTkKodeTab(border=False, closable=True)
        appTemplate.setWidget(self._kodeTab, TTkAppTemplate.MAIN)

        self._statusBar = TTkLabel(maxHeight=1)
        appTemplate.setWidget(self._statusBar, TTkAppTemplate.FOOTER, border=0)
        statusStyle = {'default':  {'color': TTkColor.BG_BLUE}}
        self._statusBar.setStyle(statusStyle)
        self._statusBar.setText("[13:03] [Vulphere(+Ziw)] [2:liberachat/#archlinux(+Cnrt)]")

        TTkShortcut(TTkK.ALT | TTkK.Key_X).activated.connect(self._quit)

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
            doc = TTkEditTextDocument(text=content, filePath=filePath)
            self._documents[filePath] = {'doc': doc, 'tabs': []}
        tview = TTkEditTextEditView(document=doc, readOnly=False)
        tedit = TTkTextEdit(textEditView=tview,
                            lineNumber=True, lineNumberStarting=1)
        doc.kodeHighlightUpdate.connect(tedit.update)
        label = TTkString(TTkCfg.theme.fileIcon.getIcon(
            filePath), TTkCfg.theme.fileIconColor) + TTkColor.RST + " " + os.path.basename(filePath)

        self._kodeTab.addTab(tedit, label)
        self._kodeTab.setCurrentWidget(tedit)

        # def _closeFile():
        #     if (index := KodeTab.lastUsed.currentIndex()) >= 0:
        #         KodeTab.lastUsed.removeTab(index)

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
                TTkString( f'Do you want to save the changes to this document before closing?\nIf you don\'t save, your changes will be lost.', TTkColor.BOLD),
                cb=TTkHelper.quit)
        else:
            TTkHelper.quit()