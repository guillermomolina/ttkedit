# MIT License
#
# Copyright (c) 2024 Guillermo A. Molina <guillermoadrianmolina AT gmail DOT com>
# Copyright (c) 2021 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

__all__ = ['TTkLogViewer']

import os
import TermTk as TTkK
from TermTk import TTkLog
from TermTk import TTkColor
from TermTk import TTkString
from TermTk import pyTTkSlot
from TermTk import pyTTkSignal
from TermTk import TTkAbstractScrollArea
from TermTk import TTkAbstractScrollView

class TTkEditorLogRepository:
    __slots__ = ('_messages', '_cwd', '_follow', 'messageAdded')
    def __init__(self):
        self._messages = [TTkString()]
        self._cwd = os.getcwd()
        self.messageAdded = pyTTkSignal(str)
        TTkLog.installMessageHandler(self.loggingCallback)

    def loggingCallback(self, mode, context, message):
        logType = "NONE"
        if mode == TTkLog.InfoMsg:       logType = TTkString("INFO "   ,TTkColor.fg("#00ff00"))
        elif mode == TTkLog.DebugMsg:    logType = TTkString("DEBUG"   ,TTkColor.fg("#00ffff"))
        elif mode == TTkLog.ErrorMsg:    logType = TTkString("ERROR"   ,TTkColor.fg("#ff0000"))
        elif mode == TTkLog.FatalMsg:    logType = TTkString("FATAL"   ,TTkColor.fg("#ff0000"))
        elif mode == TTkLog.WarningMsg:  logType = TTkString("WARNING ",TTkColor.fg("#ff0000"))
        elif mode == TTkLog.CriticalMsg: logType = TTkString("CRITICAL",TTkColor.fg("#ff0000"))
        message = f": {context.file}:{context.line} {message}".replace(self._cwd,"_")
        self._messages.append(logType+TTkString(message))
        self.messageAdded.emit(message)

    def messages(self):
        return self._messages


class _TTkEditorLogViewer(TTkAbstractScrollView):
    __slots__ = ('_messages', '_cwd', '_follow')
    def __init__(self, logRepository, *args, **kwargs):
        TTkAbstractScrollView.__init__(self, *args, **kwargs)
        self._follow = kwargs.get('follow' , False )
        self._logRepository = logRepository
        self._logRepository.messageAdded.connect(self._viewChangedHandler)

    @pyTTkSlot()
    def _viewChangedHandler(self):
        messages = self._logRepository.messages()
        offx, offy = self.getViewOffsets()
        _,h = self.size()
        if self._follow or offy == len(messages)-h-1:
            offy = len(messages)-h
        self.viewMoveTo(offx, offy)
        self.update()

    def viewFullAreaSize(self) -> tuple[int, int]:
        messages = self._logRepository.messages()
        w = max( m.termWidth() for m in messages)
        h = len(messages)
        return w , h

    def viewDisplayedSize(self) -> tuple[int, int]:
        return self.size()

    def paintEvent(self, canvas):
        messages = self._logRepository.messages()
        ox,oy = self.getViewOffsets()
        _,h = self.size()
        for y, message in enumerate(messages[oy:oy+h]):
            canvas.drawTTkString(pos=(-ox,y),text=message)

class TTkEditorLogViewer(TTkAbstractScrollArea):
    __slots__ = ('_logView')
    def __init__(self, logRepository, *args, **kwargs):
        TTkAbstractScrollArea.__init__(self, *args, **kwargs)
        kwargs.pop('parent',None)
        kwargs.pop('visible',None)
        self._logView = _TTkEditorLogViewer(logRepository, *args, **kwargs)
        self.setFocusPolicy(TTkK.TTkConstant.ClickFocus)
        self.setViewport(self._logView)
