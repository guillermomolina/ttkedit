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


from TermTk import TTkHBoxLayout
from TermTk import TTkLayout
from TermTk import TTkString
from TermTk import TTkLabel
from TermTk.TTkCore.constant import TTkK

class TTkEditStatusBar(TTkHBoxLayout):
    '''TTkEditStatusBar'''
    __slots__ = ('_itemsLeft', '_itemsCenter', '_itemsRight')
    def __init__(self, *args, **kwargs):
        self._labels = []
        TTkHBoxLayout.__init__(self, *args, **kwargs)
        self._itemsLeft   = TTkHBoxLayout()
        self._itemsCenter = TTkHBoxLayout()
        self._itemsRight  = TTkHBoxLayout()
        self.addItem(self._itemsLeft)
        self.addItem(TTkLayout())
        self.addItem(self._itemsCenter)
        self.addItem(TTkLayout())
        self.addItem(self._itemsRight)

    def addLabel(self,text:TTkString, alignment=TTkK.RIGHT_ALIGN):
        '''addLabel'''
        text = text if issubclass(type(text),TTkString) else TTkString(text)
        label = TTkLabel(self, text=text)
        self._sbItems(alignment).addWidget(label)
        self._labels.append(label)
        self.update()
        return label

    def _sbItems(self, alignment=TTkK.RIGHT_ALIGN):
        return {
            TTkK.LEFT_ALIGN:   self._itemsLeft   ,
            TTkK.CENTER_ALIGN: self._itemsCenter ,
            TTkK.RIGHT_ALIGN:  self._itemsRight
        }.get(alignment, self._itemsLeft)

    def clear(self):
        self._labels = []
        self._itemsLeft.removeItems(self._itemsLeft.children())
        self._itemsCenter.removeItems(self._itemsCenter.children())
        self._itemsRight.removeItems(self._itemsRight.children())
    
    def isVisible(self):
        return True