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

__all__ = ['TTkStatusFrame']

from TermTk import TTkK
from TermTk import TTkColor
from TermTk import TTkCfg
from TermTk import TTkFrame


def drawStatusBarBg(canvas, pos, size, color=TTkColor.RST ):
    sb = TTkCfg.theme.statusBar
    canvas.drawText(pos=pos, text=f"{sb[3]}{sb[1]*(size-2)}{sb[4]}", color=color)


class TTkStatusFrame(TTkFrame):
    __slots__ = (
        '_statusbarTop', '_statusbarTopPosition', '_statusbarBottom', '_statusbarBottomPosition')
    def __init__(self, *args, **kwargs):
        self._statusbarTopPosition = 0
        self._statusbarBottomPosition = 0
        self._statusbarTop = None
        self._statusbarBottom = None
        super().__init__(*args, **kwargs)

    def statusBar(self, position=TTkK.TOP):
        if position == TTkK.TOP:
            return self._statusbarTop
        else:
            return self._statusbarBottom

    def setStatusBar(self, statusBar, position=TTkK.BOTTOM):
        if not statusBar: # a null statusBar remove the current one
            if position == TTkK.TOP and self._statusbarTop:
                self.rootLayout().removeItem(self._statusbarTop)
                self._statusbarTop = None
                if not self._border:
                    pt,pb,pl,pr = self.getPadding()
                    self.setPadding(0,pb,pl,pr)
            if position == TTkK.BOTTOM and self._statusbarBottom:
                self.rootLayout().removeItem(self._statusbarBottom)
                self._statusbarBottom = None
                if not self._border:
                    pt,pb,pl,pr = self.getPadding()
                    self.setPadding(pt,0,pl,pr)
            return
        # statusBar is not null and it must be added to the rootLayout
        self.rootLayout().addItem(statusBar)
        if position == TTkK.TOP:
            self._statusbarTop = statusBar
            statusBar.setGeometry(1,self._statusbarTopPosition,self.width()-2,1)
        else:
            self._statusbarBottom = statusBar
            statusBar.setGeometry(1,self.height()-1-self._statusbarBottomPosition,self.width()-2,1)
        if not self._border:
            pt,pb,pl,pr = self.getPadding()
            pt = 1 if position==TTkK.TOP    else pt
            pb = 1 if position==TTkK.BOTTOM else pb
            self.setPadding(pt,pb,pl,pr)

    def resizeEvent(self, w, h):
        if self._statusbarTop:
            self._statusbarTop.setGeometry(1,self._statusbarTopPosition,w-2,1)
        if self._statusbarBottom:
            self._statusbarBottom.setGeometry(1,h-1-self._statusbarBottomPosition,w-2,1)
        super().resizeEvent(w,h)

    def paintEvent(self, canvas):
        style = self.currentStyle()
        color = style['color']
        borderColor = style['borderColor']

        if self._border:
            canvas.drawBox(pos=(0,0),size=(self._width,self._height), color=borderColor)
            if len(self._title) != 0:
                canvas.drawBoxTitle(
                                pos=(0,0),
                                size=(self._width,self._height),
                                text=self._title,
                                align=self._titleAlign,
                                color=borderColor,
                                colorText=color)
        else:
            if self._statusbarTop:
                canvas.drawMEnuBarBg(pos=(0,0),size=self.width(),color=borderColor)
            if self._statusbarBottom:
                canvas.drawMEnuBarBg(pos=(0,self.height()-1),size=self.width(),color=borderColor)
        super().paintEvent(canvas)
