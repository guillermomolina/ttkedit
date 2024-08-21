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


from pygments.formatter import Formatter
from pygments.token import Keyword, Name, Comment, String, Error, \
    Number, Operator, Generic, Token, Whitespace

from TermTk import TTkString, TTkColor, TTkLog

#: Map token types to a tuple of color values for light and dark
#: backgrounds.
TTKEDIT_COLORS = {
    Token:              TTkColor.RST, # ('',            ''),

    Whitespace:         TTkColor.fg('#888888') , # ('gray',   'brightblack'),
    Comment:            TTkColor.fg('#888888') , # ('gray',   'brightblack'),
    Comment.Preproc:    TTkColor.fg('#00FFFF') , # ('cyan',        'brightcyan'),
    Keyword:            TTkColor.fg('#0000FF') , # ('blue',    'brightblue'),
    Keyword.Type:       TTkColor.fg('#00FFFF') , # ('cyan',        'brightcyan'),
    Operator.Word:      TTkColor.fg('#FF8800') , # ('magenta',      'brightmagenta'),
    Name.Builtin:       TTkColor.fg('#00FFFF') , # ('cyan',        'brightcyan'),
    Name.Function:      TTkColor.fg('#00FF00') , # ('green',   'brightgreen'),
    Name.Namespace:     TTkColor.fg('#00FFFF') , # ('_cyan_',      '_brightcyan_'),
    Name.Class:         TTkColor.fg('#00FF00') , # ('_green_', '_brightgreen_'),
    Name.Exception:     TTkColor.fg('#00FFFF') , # ('cyan',        'brightcyan'),
    Name.Decorator:     TTkColor.fg('#888888') , # ('brightblack',    'gray'),
    Name.Variable:      TTkColor.fg('#888888') , # ('red',     'brightred'),
    Name.Constant:      TTkColor.fg('#888888') , # ('red',     'brightred'),
    Name.Attribute:     TTkColor.fg('#00FFFF') , # ('cyan',        'brightcyan'),
    Name.Tag:           TTkColor.fg('#0000FF') , # ('brightblue',        'brightblue'),
    String:             TTkColor.fg('#FFFF00') , # ('yellow',       'yellow'),
    Number:             TTkColor.fg('#0000FF') , # ('blue',    'brightblue'),

    Generic.Deleted:    TTkColor.fg('#FF0000') , # ('brightred',        'brightred'),
    Generic.Inserted:   TTkColor.fg('#00FF00') , # ('green',  'brightgreen'),
    Generic.Heading:    TTkColor.fg('#888888') , # ('**',         '**'),
    Generic.Subheading: TTkColor.fg('#FF8800') , # ('*magenta*',   '*brightmagenta*'),
    Generic.Prompt:     TTkColor.fg('#888888') , # ('**',         '**'),
    Generic.Error:      TTkColor.fg('#FF0000') , # ('brightred',        'brightred'),

    Error:              TTkColor.fg('#FF0000') , # ('_brightred_',      '_brightred_'),
}

class TTkEditFormatter(Formatter):
    class Data():
        __slots__=('lines', 'block', 'error', 'multiline')
        def __init__(self, lines, block):
            self.lines = lines
            self.block = block
            self.error = None
            self.multiline = False

    __slots__ = ('_dl', '_blockNum', '_kodeStyles')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._kodeStyles = {}
        self._blockNum = 1
        for token, style in self.style:
            # Token = Token.Comment.PreprocFile
            # style = {
            #   'color': '6272a4',
            #   'bgcolor': None,
            #   'bold': False, 'italic': False, 'underline': False,
            #   'border': None,
            #   'roman': None, 'sans': None, 'mono': None,
            #   'ansicolor': None, 'bgansicolor': None}

            # TTkLog.debug(f"{token=} {style=}")
            color = TTkColor.RST
            if style['color']:
                color += TTkColor.fg(f"#{style['color']}")
            if style['bgcolor']:
                color += TTkColor.bg(f"#{style['bgcolor']}")
            if style['bold']:
                color += TTkColor.BOLD
            if style['italic']:
                color += TTkColor.ITALIC
            if style['underline']:
                color += TTkColor.UNDERLINE
            self._kodeStyles[token] = color

        super().__init__()

    def setDl(self,dl):
        self._dl = dl

    def format(self, tokensource, _):
        multiline = False
        multilineId = 0
        for ttype, value in tokensource:
            if ttype == Error and self._dl.error is None:
                self._dl.error = len(self._dl.lines)-1
            # self._dl.multiline = ttype == Comment.Multiline
            multiline = ttype == Comment.Multiline

            while ttype not in self._kodeStyles:
                ttype = ttype.parent
            # TTkLog.debug (f"{ttype=}")
            # TTkLog.debug (f"{value=}")
            color = self._kodeStyles[ttype]

            values = value.split('\n')

            self._dl.lines[-1] += TTkString(values[0],color)
            self._dl.lines += [TTkString(t,color) for t in values[1:]]
            self._dl.block[-1] = self._blockNum
            self._dl.block += [self._blockNum]*(len(values)-1)

            # self._dl.lines += [TTkString(t) for t in value.split('\n')]

            # multiline = len(values)>1 if self._dl.lines[-1]._text == values[-1] else self._dl.multiline
            # if self._dl.lines[-1]._text == '' or not multiline:
            #     self._blockNum += 1
            #     multilineId = len(self._dl.lines)

            if multiline:
                multilineId += len(values)
            else:
                multilineId = 0
                self._blockNum += 1

        if multiline:
            self._dl.multiline = multilineId
