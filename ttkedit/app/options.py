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


import copy

from . import TTkEditConfig 
# from . import TloggGlbl

from TermTk import *

def optionsLoadTheme(theme):
    if theme == 'ASCII':
        TTkTheme.loadTheme(TTkTheme.ASCII)
    elif theme == 'UTF8':
        TTkTheme.loadTheme(TTkTheme.UTF8)
    elif theme == 'NERD':
        TTkTheme.loadTheme(TTkTheme.NERD)

def optionsFormLayout(win):
    options = copy.deepcopy(TTkEditConfig.options)

    retLayout    = TTkGridLayout()
    bottomLayout = TTkGridLayout()

    themesFrame = TTkFrame(title="Theme", border=True, layout=TTkVBoxLayout(), maxHeight=5, minHeight=5)
    # Themes
    themesFrame.layout().addWidget(r1 := TTkRadioButton(text="ASCII", name="theme", checked=options['theme'] == 'ASCII'))
    themesFrame.layout().addWidget(r2 := TTkRadioButton(text="UTF-8", name="theme", checked=options['theme'] == 'UTF8'))
    themesFrame.layout().addWidget(r3 := TTkRadioButton(text="Nerd",  name="theme", checked=options['theme'] == 'NERD'))

    retLayout.addWidget(themesFrame,0,0)
    retLayout.addWidget(TTkSpacer() ,1,0,1,2)

    retLayout.addItem(bottomLayout ,2,0,1,2)
    bottomLayout.addWidget(applyBtn  := TTkButton(text="Apply",  border=True, maxHeight=3),0,1)
    bottomLayout.addWidget(cancelBtn := TTkButton(text="Cancel", border=True, maxHeight=3),0,2)
    bottomLayout.addWidget(okBtn     := TTkButton(text="OK",     border=True, maxHeight=3),0,3)

    def _saveOptions():
        if r1.checkState() == TTkK.Checked: options['theme'] = 'ASCII'
        if r2.checkState() == TTkK.Checked: options['theme'] = 'UTF8'
        if r3.checkState() == TTkK.Checked: options['theme'] = 'NERD'
        TTkEditConfig.options = options
        TTkEditConfig.save(searches=False, filters=False, colors=False, options=True)
        optionsLoadTheme(options['theme'])
        # TloggGlbl.refreshViews()
        TTkHelper.updateAll()

    applyBtn.clicked.connect(_saveOptions)
    okBtn.clicked.connect(_saveOptions)
    okBtn.clicked.connect(win.close)
    cancelBtn.clicked.connect(win.close)

    return retLayout
