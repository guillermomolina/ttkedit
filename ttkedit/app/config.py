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


import os
import yaml
from ttkedit.version import __version__, NAME

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
