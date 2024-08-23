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


import argparse
import appdirs

from TermTk import TTk, TTkLog, TTkTheme, TTkTerm
from TermTk import TTkGridLayout

from .app import TTkEditorApp
from .config import TTKEditorConfig

def main():
    TTKEditorConfig.pathCfg = appdirs.user_config_dir("ttkeditor")

    parser = argparse.ArgumentParser()
    # parser.add_argument('-f', help='Full Screen', action='store_true')
    parser.add_argument(
        '-c', help=f'config folder (default: "{TTKEditorConfig.pathCfg}")', default=TTKEditorConfig.pathCfg)
    parser.add_argument('filename', type=str, nargs='*',
                        help='the filename/s')
    args = parser.parse_args()

    # TTkLog.use_default_file_logging()

    TTKEditorConfig.pathCfg = args.c
    TTkLog.debug(f"Config Path: {TTKEditorConfig.pathCfg}")

    TTKEditorConfig.load()

    # if 'theme' not in TTKEditorConfig.options:
    #     TTKEditorConfig.options['theme'] = 'NERD'
    # optionsLoadTheme(TTKEditorConfig.options['theme'])

    TTkTheme.loadTheme(TTkTheme.NERD)

    root = TTk( 
            title="TTk Editor",
            layout=TTkGridLayout(),             
            sigmask=(
                # TTkTerm.Sigmask.CTRL_C |
                TTkTerm.Sigmask.CTRL_Q |
                TTkTerm.Sigmask.CTRL_S |
                TTkTerm.Sigmask.CTRL_Z 
                )
            )

    root.layout().addWidget(_d:=TTkEditorApp(files=args.filename))

    # if args.showkeys:
    #     _d.setWidget(widget=TTkKeyPressView(maxHeight=3), position=_d.FOOTER, size=3)
    #     _d.setFixed(fixed=True, position=_d.FOOTER)


    root.mainloop()
