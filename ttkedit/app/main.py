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
import re
import sys
import argparse

import appdirs

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter, Terminal256Formatter, TerminalTrueColorFormatter

from TermTk import TTk, TTkK, TTkLog, TTkCfg, TTkColor, TTkTheme, TTkTerm, TTkHelper
from TermTk import TTkString
from TermTk import TTkColorGradient
from TermTk import pyTTkSlot, pyTTkSignal

from TermTk import TTkFrame, TTkButton
from TermTk import TTkTabWidget, TTkKodeTab
from TermTk import TTkAbstractScrollArea, TTkAbstractScrollView
from TermTk import TTkAbout
from TermTk import TTkFileDialogPicker
from TermTk import TTkFileTree, TTkTextEdit

from TermTk import TTkGridLayout
from TermTk import TTkSplitter

from ttkedit.app.options import optionsLoadTheme

from .config import *
from .about import *
# from .options import optionsFormLayout, optionsLoadTheme
from .texteditview import TTkEditTextEditView
from .textdocument import TTkEditTextDocument


class TTkEdit(TTkGridLayout):
    __slots__ = ('_kodeTab', '_documents')

    def __init__(self, *, files, **kwargs):
        self._documents = {}

        super().__init__(**kwargs)

        self.addWidget(splitter := TTkSplitter())

        layoutLeft = TTkGridLayout()
        splitter.addItem(layoutLeft, 20)

        hSplitter = TTkSplitter(parent=splitter,  orientation=TTkK.HORIZONTAL)

        menuFrame = TTkFrame(border=False, maxHeight=1)

        self._kodeTab = TTkKodeTab(
            parent=hSplitter, border=False, closable=True)

        fileMenu = menuFrame.newMenubarTop().addMenu("&File")
        fileMenu.addMenu("Open").menuButtonClicked.connect(
            self._showFileDialog)
        # .menuButtonClicked.connect(self._closeFile)
        fileMenu.addMenu("Close")
        fileMenu.addMenu("Exit").menuButtonClicked.connect(
            lambda _: TTkHelper.quit())

        def _showAbout(btn):
            TTkHelper.overlay(None, TTkEditAbout(), 30, 10)

        def _showAboutTTk(btn):
            TTkHelper.overlay(None, TTkAbout(), 30, 10)

        helpMenu = menuFrame.newMenubarTop().addMenu(
            "&Help", alignment=TTkK.RIGHT_ALIGN)
        helpMenu.addMenu("About ...").menuButtonClicked.connect(_showAbout)
        helpMenu.addMenu("About ttk").menuButtonClicked.connect(_showAboutTTk)

        fileTree = TTkFileTree(path='.')

        layoutLeft.addWidget(menuFrame, 0, 0)
        layoutLeft.addWidget(fileTree, 1, 0)
        # layoutLeft.addWidget(quitbtn := TTkButton(
        #     border=True, text="Quit", maxHeight=3), 2, 0)

        # quitbtn.clicked.connect(TTkHelper.quit)

        for file in files:
            self._openFile(file)

        fileTree.fileActivated.connect(lambda x: self._openFile(x.path()))

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
        tedit = TTkTextEdit(textEditView=tview, lineNumber=True, lineNumberStarting=1)
        doc.kodeHighlightUpdate.connect(tedit.update)
        label = TTkString(TTkCfg.theme.fileIcon.getIcon(
            filePath), TTkCfg.theme.fileIconColor) + TTkColor.RST + " " + os.path.basename(filePath)

        self._kodeTab.addTab(tedit, label)
        self._kodeTab.setCurrentWidget(tedit)

        # def _closeFile():
        #     if (index := KodeTab.lastUsed.currentIndex()) >= 0:
        #         KodeTab.lastUsed.removeTab(index)


def main():
    TTkEditConfig.pathCfg = appdirs.user_config_dir("ttkedit")

    parser = argparse.ArgumentParser()
    # parser.add_argument('-f', help='Full Screen', action='store_true')
    parser.add_argument(
        '-c', help=f'config folder (default: "{TTkEditConfig.pathCfg}")', default=TTkEditConfig.pathCfg)
    parser.add_argument('filename', type=str, nargs='*',
                        help='the filename/s')
    args = parser.parse_args()

    # TTkLog.use_default_file_logging()

    TTkEditConfig.pathCfg = args.c
    TTkLog.debug(f"Config Path: {TTkEditConfig.pathCfg}")

    TTkEditConfig.load()

    # if 'theme' not in TTkEditConfig.options:
    #     TTkEditConfig.options['theme'] = 'NERD'
    # optionsLoadTheme(TTkEditConfig.options['theme'])

    TTkTheme.loadTheme(TTkTheme.NERD)

    root = TTk(layout=TTkEdit(files=args.filename), title="TTkEdit",
               sigmask=(
        # TTkTerm.Sigmask.CTRL_C |
        TTkTerm.Sigmask.CTRL_Q |
        TTkTerm.Sigmask.CTRL_S |
        TTkTerm.Sigmask.CTRL_Z))

    root.mainloop()
