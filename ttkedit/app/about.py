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


from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.color import TTkColor
from TermTk import TTkWindow
from .config import TTkEditConfig

class TTkEditAbout(TTkWindow):
    ttkedit = [
        "__________________    _______              ",
        "\_______________ /   / / ____)  ┌─┐─┐─┐   ",
        "    /\    /\   | |__/ /| |__  __| |─┘ └─┐ ",
        "   |  |  |  |  |  _  / |  __|/ _  |─┐  ┌┘ ",
        "   |  |  |  |  | | \ \ | |__( (_| | |  \_ ",
        "   |  |  |  |  └─┘  \_)|_____)____|_|\___)",
        "   |  |  |  |                              ",
        "   └──┘  └──┘                              ",]

    def __init__(self, *args, **kwargs):
        TTkWindow.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'About' )
        self.setTitle('Guillermo A. Molina proudly presents...')
        self.resize(48,15)

    def paintEvent(self, canvas):
        c = [0xFF,0xFF,0xFF]
        for y, line in enumerate(TTkEditAbout.ttkedit):
            canvas.drawText(pos=(3,3+y),text=line, color=TTkColor.fg(f'#{c[0]:02X}{c[1]:02X}{c[2]:02X}'))
            c[2]-=0x18
            c[0]-=0x08
        canvas.drawText(pos=(26, 9),text=f"  Version: {TTkEditConfig.version}", color=TTkColor.fg('#AAAAFF'))
        canvas.drawText(pos=(14,11),text=f"Powered By, pyTermTk")
        canvas.drawText(pos=( 3,13),text=f"https://github.com/guillermomolina/ttkedit", color=TTkColor.fg('#44FFFF'))

        TTkWindow.paintEvent(self, canvas)
