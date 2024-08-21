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


from threading import Lock

from pygments import highlight
from pygments.util import ClassNotFound
from pygments.lexers import guess_lexer, guess_lexer_for_filename, special
from pygments.formatters import TerminalFormatter, Terminal256Formatter, TerminalTrueColorFormatter

from TermTk import TTk, TTkK, TTkLog, TTkCfg, TTkTheme, TTkTerm, TTkHelper, TTkTimer
from TermTk import TTkString
from TermTk import TTkColor, TTkColorGradient
from TermTk import pyTTkSlot, pyTTkSignal

from TermTk import TTkTextDocument
from .formatter import TTkEditFormatter


class TTkEditTextDocument(TTkTextDocument):
    _linesRefreshed = 30
    __slots__ = (
        '_filePath', '_timerRefresh',
        'kodeHighlightUpdate', '_kodeDocMutex',
        '_blocks', '_changedContent', '_refreshContent',
        '_lexer', '_formatter')

    def __init__(self, *args, **kwargs):
        self.kodeHighlightUpdate = pyTTkSignal()
        self._kodeDocMutex = Lock()
        self._lexer = None
        self._blocks = []
        self._formatter = TTkEditFormatter(style='gruvbox-dark')
        super().__init__(*args, **kwargs)
        self._filePath = kwargs.get('filePath', "")
        self._timerRefresh = TTkTimer()
        self._timerRefresh.timeout.connect(self._refreshEvent)
        self._timerRefresh.start(0.3)
        self._changedContent = (0, 0, len(self._dataLines))
        self._refreshContent = (0, TTkEditTextDocument._linesRefreshed)
        self.contentsChange.connect(
            lambda a, b, c: TTkLog.debug(f"{a=} {b=} {c=}"))
        self.contentsChange.connect(self._saveChangedContent)

    @pyTTkSlot(int, int, int)
    def _saveChangedContent(self, a, b, c):
        if self._changedContent:
            self._changedContent = TTkTextDocument._mergeChangesSlices(
                self._changedContent, (a, b, c))
        else:
            self._changedContent = (a, b, c)
        if not self._refreshContent:
            self._refreshContent = (
                self._changedContent[0], TTkEditTextDocument._linesRefreshed)
        self._timerRefresh.start(0.1)

    @pyTTkSlot()
    def _refreshEvent(self):
        if not self._refreshContent:
            return
        self._kodeDocMutex.acquire()

        ra, rb = self._refreshContent

        if self._changedContent:
            ca, cb, cc = self._changedContent
            self._changedContent = None
            self._blocks[ca:ca+cb] = [0]*cc
            ra = min(ra, ca)

        # find the beginning of the current block
        # TTkLog.debug(self._blocks)
        if ra and self._blocks:
            blockId = self._blocks[ra]
            for i, v in enumerate(reversed(self._blocks[:ra])):
                # TTkLog.debug(f"{i=}:{v=} {blockId=}")
                if v == blockId or not blockId:
                    blockId = v
                    ra -= 1
                    rb += 1
                else:
                    break

        # TTkLog.debug(f"{ra=} {rb=}")

        eof = False
        if (ra+rb) >= len(self._dataLines):
            rb = len(self._dataLines)-ra
            eof = True

        tsl = self._dataLines[ra:ra+rb]
        # Find the offset from the first not empty line
        # because pygments autostrip the heading empty lines
        offset = 0
        for i, l in enumerate(tsl):
            if l != '':
                offset = i
                break

        rawl = [l._text for l in tsl[offset:]]
        rawt = '\n'.join(rawl)
        if not self._lexer:
            try:
                self._lexer = guess_lexer_for_filename(self._filePath, rawt)
            except ClassNotFound:
                self._lexer = special.TextLexer()

        # TTkLog.debug(f"Refresh {self._lexer.name} {ra=} {rb=}")
        tsl1 = [TTkString()]*(offset+1)
        block = [0]*(offset+1)

        kfd = TTkEditFormatter.Data(tsl1, block)
        self._formatter.setDl(kfd)

        highlight(rawt, self._lexer, self._formatter)

        # for ll in tsl:
        #     TTkLog.debug(f"1: -{ll}-")
        # for ll in tsl1:
        #     TTkLog.debug(f"2: -{ll}-")

        tsl1 = tsl1[:rb]
        block = block[:rb]
        self._dataLines[ra:ra+rb] = tsl1 + tsl[len(tsl1):]
        self._blocks[ra:ra+rb] = block + [-1]*(rb-len(block))
        # TTkLog.debug(self._blocks)

        if kfd.error is not None:
            self._refreshContent = (ra+kfd.error, rb << 1)
            # TTkLog.debug(f"Error: {self._refreshContent=}")
        elif kfd.multiline is not None:
            self._refreshContent = (ra+kfd.multiline, rb << 1)
        elif (ra+rb) < len(self._dataLines):
            self._refreshContent = (ra+rb, TTkEditTextDocument._linesRefreshed)
        else:
            self._refreshContent = None
        # TTkLog.debug(f"{self._refreshContent=}")

        if not eof:
            self._timerRefresh.start(0.03)
        else:
            TTkLog.debug(f"Refresh {self._lexer.name} DONE!!!")

        self._kodeDocMutex.release()
        self.kodeHighlightUpdate.emit()

    def getLock(self):
        return self._kodeDocMutex

    def filePath(self):
        return self._filePath
