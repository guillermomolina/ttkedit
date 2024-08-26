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
from TermTk import TTkGridLayout
from TermTk import TTkAppTemplate
from TermTk import TTkMenuBarLayout
from TermTk import TTkTextCursor
from TermTk import TTkTabWidget
from TermTk import TTkWidget
from TermTk import pyTTkSlot
from TermTk import TTkWindow
from TermTk import TTkTerminal
from TermTk import TTkTerminalHelper
from TermTk import TTkSplitter
from TermTk import TTkList
from TermTk import TTkAbstractListItem

from ttkeditor.about import TTKEditorAbout
from ttkeditor.exceptions import TTkEditorNYIError
from ttkeditor.kodetab import TTkEditorKodeTab
from ttkeditor.logviewer import TTkEditorLogRepository, TTkEditorLogViewer
from ttkeditor.texteditview import TTKEditorTextEditView
from ttkeditor.textdocument import TTKEditorTextDocument


class TTkEditorApp(TTkAppTemplate):
    __slots__ = (
        '_modified', '_codeView', '_documents',
        '_cursorPositionStatus', '_encodingStatus', '_languageStatus'
    )

    def __init__(self, files=None, border=False, *args, **kwargs):
        self._documents = {}
        self._modified = False

        super().__init__(border=border, **kwargs)

        self._logRepository = TTkEditorLogRepository()

        self._sidePanel = TTkSplitter(orientation=TTkK.VERTICAL)
        self._openEditors = TTkList()
        self._openEditors.itemClicked.connect(self._openEditorsItemClicked)
        self._sidePanel.addWidget(self._openEditors, 5)
        fileTree = TTkFileTree(path='.')
        fileTree.fileActivated.connect(lambda x: self._openFileTab(x.path()))
        self._sidePanel.addWidget(fileTree)

        self._codeView = TTkEditorKodeTab(border=False, closable=True)
        self._codeView.currentChanged.connect(self._currentTabChanged)
        self._codeView.tabCloseRequested.connect(self._tabCloseRequested)

        self._toolsView = TTkKodeTab(border=False, closable=True)

        self.setWidget(self._sidePanel, TTkAppTemplate.LEFT, 20)
        self.setWidget(self._codeView)
        self.setWidget(self._toolsView, TTkAppTemplate.BOTTOM, 10)

        menuBar = TTkMenuBarLayout()
        self.setMenuBar(menuBar, TTkAppTemplate.HEADER)
        self.setFixed(True, TTkAppTemplate.HEADER)
        self.setBorder(False, TTkAppTemplate.HEADER)

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
        toolsMenu.addMenu("Logs").menuButtonClicked.connect(
            self._openLogViewerTab)
        toolsMenu.addMenu("Terminal").menuButtonClicked.connect(
            self._openTerminalTab)

        panelsMenu = menuBar.addMenu("&Panels", alignment=TTkK.RIGHT_ALIGN)
        self._sidePanelToggler = panelsMenu.addMenu("Side panel", checkable=True, checked=True)
        self._sidePanelToggler.toggled.connect(self._sidePanel.setVisible)

        self._toolsViewToggler = panelsMenu.addMenu("Tools panel", checkable=True, checked=False)
        self._toolsViewToggler.toggled.connect(self._toolsView.setVisible)
        self._toolsView.setVisible(False)

        helpMenu = menuBar.addMenu(
            "&Help", alignment=TTkK.RIGHT_ALIGN)
        helpMenu.addMenu("About ...").menuButtonClicked.connect(
            self._showAboutDialog)
        helpMenu.addMenu("About ttk").menuButtonClicked.connect(
            self._showAboutTTkDialog)

        self._statusBar = TTkMenuBarLayout()
        self.setMenuBar(self._statusBar,  TTkAppTemplate.FOOTER)
        self.setFixed(True, TTkAppTemplate.FOOTER)
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

        if files is not None:
            for file in files:
                self._openFileTab(file)

    pyTTkSlot()

    def _closeFile(self):
        if self._codeView.lastUsed:
            if (index := self._codeView.lastUsed.currentIndex()) >= 0:
                self._codeView.lastUsed.removeTab(index)

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
        self._toolsView.addTab(logViewer, "Logs")
        self._toolsView.setCurrentWidget(logViewer)
        self._toolsViewToggler.setChecked(True)

    def _openTerminalTab(self):
        term = TTkTerminal()
        self._toolsView.addTab(term, f"Terminal")
        self._toolsView.setCurrentWidget(term)
        self._toolsViewToggler.setChecked(True)
        th = TTkTerminalHelper(term=term)
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

        self._codeView.addTab(tedit, label)
        self._codeView.setCurrentWidget(tedit)

        self._openEditors.addItem(li := TTkAbstractListItem(text=label, data=tedit))
        self._openEditors.setCurrentItem(li)                  
 
    def _openEditorsItemClicked(self, item):
        self._codeView.setCurrentWidget(item.data())

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

    @pyTTkSlot(TTkTabWidget, int)
    def _tabCloseRequested(self, tabWidget, index):
        widget = tabWidget.widget(index)
        for index, item in enumerate(self._openEditors.items()):
            if item.data() == widget:
                self._openEditors.removeAt(index)
