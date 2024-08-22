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

__all__ = ['TTkEditorFrame']

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkWidgets.container import TTkContainer

from .exceptions import TTkEditorNYIError


def drawStatusBarBg(canvas, pos, size, color=TTkColor.RST ):
    sb = TTkCfg.theme.menuBar
    canvas.drawText(pos=pos, text=f"{sb[3]}{sb[1]*(size-2)}{sb[4]}", color=color)


class TTkEditorFrame(TTkContainer):
    '''

    ::

        ┌──────│Title│──────┐
        │                   │
        │                   │
        │                   │
        │                   │
        │                   │
        └───────────────────┘

    Demo1: `layout_nested.py  <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/demo/showcase/layout_nested.py>`_

    Demo2: `splitter.py  <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/demo/showcase/splitter.py>`_

    :param title: the title displayed at the top border of the frame, defaults to ""
    :type title: str, optional
    :param border: Enable/Disable the border, defaults to **True**
    :type border: bool, optional

    '''

    classStyle = {
                'default':     {'color': TTkColor.fg("#dddddd")+TTkColor.bg("#222222"),
                                'borderColor': TTkColor.RST},
                'disabled':    {'color': TTkColor.fg('#888888'),
                                'borderColor':TTkColor.fg('#888888')}
            }

    MENUBAR_POSITION = 0
    STATUSBAR_POSITION = -1

    __slots__ = (
        '_border','_title', '_titleAlign',
        '_menubar', '_menubarPosition', '_statusbar', '_statusbarPosition')
    def __init__(self, *args, **kwargs):
        self._titleAlign = kwargs.get('titleAlign' , TTkK.CENTER_ALIGN )
        self._title = TTkString(kwargs.get('title' , '' ))
        self._border = kwargs.get('border', True )
        self._menubarPosition = TTkK.TOP
        self._statusbarPosition = TTkK.BOTTOM
        self._menubar = None
        self._statusbar = None
        super().__init__(*args, **kwargs)
        self.setBorder(self._border)

    def menuBar(self):
        return self._menubar

    def statusBar(self):
        return self._statusbar

    def setMenuBar(self, menuBar, position=TTkK.TOP):
        if not menuBar: # a null menuBar remove the current one
            raise TTkEditorNYIError()
            if position == TTkK.TOP and self._menubarTop:
                self.rootLayout().removeItem(self._menubarTop)
                self._menubarTop = None
                if not self._border:
                    pt,pb,pl,pr = self.getPadding()
                    self.setPadding(0,pb,pl,pr)
            if position == TTkK.BOTTOM and self._menubarBottom:
                self.rootLayout().removeItem(self._menubarBottom)
                self._menubarBottom = None
                if not self._border:
                    pt,pb,pl,pr = self.getPadding()
                    self.setPadding(pt,0,pl,pr)
            return
        # menuBar is not null and it must be added to the rootLayout
        self.rootLayout().addItem(menuBar)
        self._menubar = menuBar
        self._menubarPosition = position
        if position == TTkK.TOP:
            menuBar.setGeometry(1,self.MENUBAR_POSITION,self.width()-2,1)
        else:
            menuBar.setGeometry(1,self.height()-1-self.MENUBAR_POSITION,self.width()-2,1)
        if not self._border:
            pt,pb,pl,pr = self.getPadding()
            pt = 1 if position==TTkK.TOP    else pt
            pb = 1 if position==TTkK.BOTTOM else pb
            self.setPadding(pt,pb,pl,pr)

    def setstatusBar(self, statusBar, position=TTkK.BOTTOM):
        if not statusBar: # a null statusBar remove the current one
            raise TTkEditorNYIError()
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
        self._statusbar = statusBar
        self._statusbarPosition = position
        if position == TTkK.TOP:
            statusBar.setGeometry(1,self.STATUSBAR_POSITION,self.width()-2,1)
        else:
            statusBar.setGeometry(1,self.height()-1-self.STATUSBAR_POSITION,self.width()-2,1)
        if not self._border:
            pt,pb,pl,pr = self.getPadding()
            pt = 1 if position==TTkK.TOP    else pt
            pb = 1 if position==TTkK.BOTTOM else pb
            self.setPadding(pt,pb,pl,pr)

    def resizeEvent(self, w, h):
        if self._menubar:
            if self._menubarPosition == TTkK.TOP:
                self._menubar.setGeometry(1,self.MENUBAR_POSITION,w-2,1)
            else:
                self._menubar.setGeometry(1,h-1-self.MENUBAR_POSITION,w-2,1)
        if self._statusbar:
            if self._statusbarPosition == TTkK.TOP:
                self._statusbar.setGeometry(1,self.STATUSBAR_POSITION,w-2,1)
            else:
                self._statusbar.setGeometry(1,h-1-self.STATUSBAR_POSITION,w-2,1)
        super().resizeEvent(w,h)

    def title(self):
        '''title'''
        return self._title

    def setTitle(self, title):
        '''setTitle'''
        if self._title.sameAs(title): return
        self._title = TTkString(title)
        self.update()

    def titleAlign(self):
        return self._titleAlign

    def setTitleAlign(self, align):
        if align == self._titleAlign: return
        self._titleAlign = align
        self.update()

    def setBorder(self, border):
        '''setBorder'''
        self._border = border
        if border: self.setPadding(1,1,1,1)
        else:      self.setPadding(0,0,0,0)
        self.update()

    def border(self):
        '''border'''
        return self._border

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
            if self._menubar:
                if self._menubarPosition == TTkK.TOP:
                    canvas.drawMenuBarBg(pos=(0,0),size=self.width(),color=borderColor)
                else:
                    canvas.drawMenuBarBg(pos=(0,self.height()-1),size=self.width(),color=borderColor)
            if self._statusbar:
                if self._statusbarPosition == TTkK.TOP:
                    drawStatusBarBg(canvas, pos=(0,0),size=self.width(),color=borderColor)
                else:
                    drawStatusBarBg(canvas, pos=(0,self.height()-1),size=self.width(),color=borderColor)
