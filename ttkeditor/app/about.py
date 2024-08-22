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



from TermTk.TTkCore.color import TTkColor
from TermTk import TTkWindow
from .config import TTKEditorConfig

class TTKEditorAbout(TTkWindow):
    ttkeditor = [
        r"__________________    _______                      ",
        r"\_______________ /   / / ____)  ┌─┐─┐─┐            ",
        r"    /\    /\   | |__/ /| |__  __| |─┘ └─┐ __   ___ ",
        r"   |  |  |  |  |  _  / |  __|/ _  |─┐  ┌┘/ _ \|  _|",
        r"   |  |  |  |  | | \ \ | |__( (_| | |  \( (_| ) |  ",
        r"   |  |  |  |  └─┘  \_)|_____)____|_|\___)___/|_|  ",
        r"   |  |  |  |                                      ",
        r"   └──┘  └──┘                                      ",]

    def __init__(self, *args, **kwargs):
        TTkWindow.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'About' )
        self.setTitle('Guillermo A. Molina proudly presents...')
        self.resize(57,14)

    def paintEvent(self, canvas):
        c = [0xFF,0xFF,0xFF]
        for y, line in enumerate(TTKEditorAbout.ttkeditor):
            canvas.drawText(pos=(3,3+y),text=line, color=TTkColor.fg(f'#{c[0]:02X}{c[1]:02X}{c[2]:02X}'))
            c[2]-=0x18
            c[0]-=0x08
        canvas.drawText(pos=(35,10),text=f"  Version: {TTKEditorConfig.version}", color=TTkColor.fg('#AAAAFF'))
        canvas.drawText(pos=( 6,12),text=f"https://github.com/guillermomolina/ttkeditor", color=TTkColor.fg('#44FFFF'))

        TTkWindow.paintEvent(self, canvas)
