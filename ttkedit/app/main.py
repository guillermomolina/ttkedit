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


import argparse
import appdirs

from TermTk import TTk, TTkLog, TTkTheme, TTkTerm

from TermTk import TTkGridLayout

from .edit import TTkEdit
from .config import *
from .about import *

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

    root = TTk(
            title="TTk Edit",
            mouseTrack=True,
            layout=TTkGridLayout(),
            sigmask=(
                # TTkTerm.Sigmask.CTRL_C |
                TTkTerm.Sigmask.CTRL_Q |
                TTkTerm.Sigmask.CTRL_S |
                TTkTerm.Sigmask.CTRL_Z ))

    root.layout().addWidget(_d:=TTkEdit(fileName=args.filename))

    # if args.showkeys:
    #     _d.setWidget(widget=TTkKeyPressView(maxHeight=3), position=_d.FOOTER, size=3)
    #     _d.setFixed(fixed=True, position=_d.FOOTER)


    root.mainloop()
