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
from TermTk import TTkTextCursor
from TermTk import TTkTabWidget
from TermTk import TTkWidget
from TermTk import pyTTkSlot
from TermTk import TTkWindow
from TermTk.TTkTestWidgets.logviewer import _TTkLogViewer
from TermTk import TTkTerminal
from TermTk import TTkTerminalHelper

from ttkeditor.about import TTKEditorAbout
from ttkeditor.exceptions import TTkEditorNYIError
from ttkeditor.logviewer import TTkEditorLogRepository, TTkEditorLogViewer
from ttkeditor.texteditview import TTKEditorTextEditView
from ttkeditor.textdocument import TTKEditorTextDocument


class TTkEditorApp(TTkFrame):
    __slots__ = (
        '_modified', '_kodeTab', '_documents',
        '_cursorPositionStatus', '_encodingStatus', '_languageStatus'
    )

    def __init__(self, files=None, border=False, *args, **kwargs):
        self._documents = {}
        self._modified = False

        super().__init__(border=border, **kwargs)

        self._logRepository = TTkEditorLogRepository()

        menuBar = TTkMenuBarLayout()
        self.setMenuBar(menuBar)

        fileMenu = menuBar.addMenu("&File")
        fileMenu.addMenu("Open").menuButtonClicked.connect(
            self._showFileDialog)
        fileMenu.addMenu("Close").menuButtonClicked.connect(self._closeFile)
        fileMenu.addMenu("E&xit Alt+X").menuButtonClicked.connect(self._quit)
        TTkShortcut(TTkK.ALT | TTkK.Key_X).activated.connect(self._quit)

        editMenu = menuBar.addMenu("&Edit")
        editMenu.addMenu("Search")
        editMenu.addMenu("Replace")

        toolsMenu = menuBar.addMenu("&Tools")
        toolsMenu.addMenu("Logs").menuButtonClicked.connect(self._openLogViewerTab)
        toolsMenu.addMenu("Terminal").menuButtonClicked.connect(self._openTerminalTab)

        helpMenu = menuBar.addMenu(
            "&Help", alignment=TTkK.RIGHT_ALIGN)
        helpMenu.addMenu("About ...").menuButtonClicked.connect(
            self._showAboutDialog)
        helpMenu.addMenu("About ttk").menuButtonClicked.connect(
            self._showAboutTTkDialog)

        self._statusBar = TTkMenuBarLayout()
        self.setMenuBar(self._statusBar, TTkK.BOTTOM)
        self._cursorPositionStatus = self._statusBar.addMenu(
            "", alignment=TTkK.RIGHT_ALIGN)
        self._cursorPositionStatus.setVisible(False)
        self._encodingStatus = self._statusBar.addMenu(
            "", alignment=TTkK.RIGHT_ALIGN)
        self._encodingStatus.setVisible(False)
        self._languageStatus = self._statusBar.addMenu(
            "", alignment=TTkK.RIGHT_ALIGN)
        self._languageStatus.setVisible(False)

        nf_cod_bell = ""
        nf_cod_bell_dot = ""
        self._notificationStatus = self._statusBar.addMenu(
            nf_cod_bell, alignment=TTkK.RIGHT_ALIGN).menuButtonClicked.connect(self._showNotificationsDialog)

        fileTree = TTkFileTree(path='.')
        fileTree.fileActivated.connect(lambda x: self._openFileTab(x.path()))
        self._kodeTab = TTkKodeTab(border=False, closable=True)
        self._kodeTab.currentChanged.connect(self._currentTabChanged)

        self._tabWidget = TTkKodeTab(border=False, closable=True)

        self.setLayout(TTkGridLayout())
        self.layout().addWidget(vSplitter := TTkSplitter())
        vSplitter.addWidget(fileTree, 20)
        vSplitter.addWidget(hSplitter := TTkSplitter(orientation=TTkK.VERTICAL))
        hSplitter.addWidget(self._kodeTab)
        hSplitter.addWidget(self._tabWidget, 10)

        if files is not None:
            for file in files:
                self._openFileTab(file)

    pyTTkSlot()

    def _closeFile(self):
        if self._kodeTab.lastUsed:
            if (index := self._kodeTab.lastUsed.currentIndex()) >= 0:
                self._kodeTab.lastUsed.removeTab(index)

    def _showAboutDialog(self, btn):
        TTkHelper.overlay(None, TTKEditorAbout(), 30, 10)

    def _showAboutTTkDialog(self, btn):
        TTkHelper.overlay(None, TTkAbout(), 30, 10)

    def _showNotificationsDialog(self, btn):
        notificationsWindow = TTkWindow(size=(80, 20), title="Log viewr", layout=TTkGridLayout(),
                                    flags=TTkK.WindowFlag.WindowMaximizeButtonHint | TTkK.WindowFlag.WindowCloseButtonHint)
        logViewer = TTkEditorLogViewer(self._logRepository, follow=True)
        notificationsWindow.layout().addWidget(logViewer)
        TTkHelper.overlay(None, notificationsWindow, 10, 5)

    def _openLogViewerTab(self, btn):
        logViewer = TTkEditorLogViewer(self._logRepository, follow=True)
        self._tabWidget.addTab(logViewer, "Logs")
        self._tabWidget.setCurrentWidget(logViewer)

    def _openTerminalTab(self):
        term = TTkTerminal()
        th = TTkTerminalHelper(term=term)
        self._tabWidget.addTab(term, f"Terminal")
        self._tabWidget.setCurrentWidget(term)
        th.runShell()

    def _showFileDialog(self):
        filePicker = TTkFileDialogPicker(pos=(3, 3), size=(75, 24), caption="Pick Something", path=".", fileMode=TTkK.FileMode.AnyFile,
                                         filter="All Files (*);;Python Files (*.py);;Bash scripts (*.sh);;Markdown Files (*.md)")
        filePicker.pathPicked.connect(self._openFileTab)
        TTkHelper.overlay(None, filePicker, 20, 5, True)

    def _openFileTab(self, filePath):
        encoding = TTKEditorTextDocument.DEFAULT_ENCODING
        filePath = os.path.realpath(filePath)
        if filePath in self._documents:
            doc = self._documents[filePath]['doc']
        else:
            with open(filePath, 'r', encoding=encoding) as f:
                content = f.read()
            doc = TTKEditorTextDocument(
                text=content, filePath=filePath, encoding=encoding)
            self._documents[filePath] = {'doc': doc, 'tabs': [], }
        tview = TTKEditorTextEditView(document=doc, readOnly=False)
        tedit = TTkTextEdit(textEditView=tview,
                            lineNumber=True, lineNumberStarting=1)
        doc.cursorPositionChanged.connect(self._cursorChanged)
        doc.kodeHighlightUpdate.connect(tedit.update)
        doc.lexerNameChanged.connect(self._lexerNameChanged)
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

    @pyTTkSlot(TTkTextCursor)
    def _cursorChanged(self, cursor):
        cP = cursor.position()
        self._setCursorPositionStatus(f"Ln {cP.line+1}, Col {cP.pos+1}")

    @pyTTkSlot(str)
    def _lexerNameChanged(self, lexerName):
        self._setLanguageStatus(lexerName)

    def _setCursorPositionStatus(self, text):
        self._cursorPositionStatus.setText(TTkString(text))
        # FIXME: We just need to resize, anyway
        self._cursorPositionStatus.setVisible(True)
        self._cursorPositionStatus.setCheckable(False)
        self._statusBar.update()

    def _setEncodingStatus(self, encoding):
        self._encodingStatus.setText(TTkString(encoding))
        # FIXME: We just need to resize, anyway
        self._encodingStatus.setVisible(True)
        self._encodingStatus.setCheckable(False)
        self._statusBar.update()

    def _setLanguageStatus(self, language):
        self._languageStatus.setText(TTkString(language))
        # FIXME: We just need to resize, anyway
        self._languageStatus.setVisible(True)
        self._languageStatus.setCheckable(False)
        self._statusBar.update()

    @pyTTkSlot(TTkTabWidget, int, TTkWidget, object)
    def _currentTabChanged(self, tabWidget, index, tview):
        if tview is None or not isinstance(tview, TTkTextEdit):
            self._cursorPositionStatus.setVisible(False)
            self._encodingStatus.setVisible(False)
            self._languageStatus.setVisible(False)
            return
        tedit = tview.textEditView()
        self._cursorChanged(tedit.textCursor())
        doc = tedit.document()
        tedit.setFocus()
        self._setEncodingStatus(doc.encoding())
        lexer = doc.lexer()
        if lexer is None:
            self._languageStatus.setVisible(False)
        else:
            self._setLanguageStatus(lexer.name)
