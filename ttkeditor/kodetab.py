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

from TermTk import TTkKodeTab
from TermTk import pyTTkSlot
from TermTk import TTkWidget
from TermTk.TTkWidgets.kodetab import _TTkKodeTab


def findWidgetOwner(kodetab, widget):
    for w in kodetab._tabWidgets:
        if w == widget:
            return kodetab
    for w in kodetab.layout().iterWidgets():
        if type(w) is _TTkKodeTab:
            child = findWidgetOwner(w, widget)
            if child is not None:
                return child
    return None

class TTkEditorKodeTab(TTkKodeTab):

    @pyTTkSlot(TTkWidget)
    def setCurrentWidget(self, widget):
        for w in self.layout().iterWidgets():
            if type(w) is _TTkKodeTab:
                kodetab = findWidgetOwner(w, widget)
                if kodetab is not None: 
                    self._lastKodeTabWidget = kodetab
                    kodetab.setFocus()
                    return super().setCurrentWidget(widget)
