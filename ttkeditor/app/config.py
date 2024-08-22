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


import os
import yaml
from ttkeditor.version import __version__, NAME

class TTkEditConfig:
    version=__version__
    name=NAME
    cfgVersion = '1.0'
    pathCfg="."
    options={}
    maxsearches=200

    @staticmethod
    def save(searches=True, filters=True, colors=True, options=True):
        os.makedirs(TTkEditConfig.pathCfg, exist_ok=True)
        optionsPath  = os.path.join(TTkEditConfig.pathCfg,'options.yaml')

        def writeCfg(path, cfg):
            fullCfg = {
                'version':TTkEditConfig.cfgVersion,
                'cfg':cfg }
            with open(path, 'w') as f:
                yaml.dump(fullCfg, f, sort_keys=False, default_flow_style=False)

        if options:  writeCfg(optionsPath,  TTkEditConfig.options)

    @staticmethod
    def load():
        optionsPath  = os.path.join(TTkEditConfig.pathCfg,'options.yaml')

        if os.path.exists(optionsPath):
            with open(optionsPath) as f:
                TTkEditConfig.options = yaml.load(f, Loader=yaml.SafeLoader)['cfg']
