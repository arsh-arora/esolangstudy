from .utils import LEX, ErrorHandler, ERROR, CONGRESS_RULE, STARTING_TROUBLE, MISQUOTE, WORDS
import re
import sys

mitrooon = re.compile(r'ama miyan sunte ho')
acche = re.compile(r'^ac[ch]?hee?$')
barabar = re.compile(r'^bara+bar$')
sach = re.compile(r'^sac[ch]?h$')
jhoot = re.compile(r'^jh?(oo|u)t$')


class Lexer:
    def __init__(self, value, value_type="filename"):
        self.contents = []
        if value_type == "filename":
            with open(value) as f: # open the .chai file
                self.contents = list(map(lambda x: x.lower(), f.readlines())) # list of all linescoverted to lower case
        else: # when is value_type not "filename"!!!
            self.contents = value.lower().split("\n")
        self.stack = []
        self.clear = False

    @staticmethod
    def lexeme(lex, value=None, line=0, offset=0):
        return locals()

    @staticmethod
    def normalize(word):
        if word in WORDS:
            word = WORDS[word]
        elif mitrooon.search(word):
            word = 'mitrooon'
        elif acche.search(word):
            word = 'acche'
        elif barabar.search(word):
            word = 'barabar'
        elif sach.search(word):
            word = 'sach'
        elif jhoot.search(word):
            word = 'jhoot'
        return word

    def _push(self, *lex): # All arguments are appended together as a single token at end 
        self.stack.append(lex)
        self.clear = True

    def on_top(self, *lex):
        i = len(self.stack) - 1
        for l in lex[::-1]:
            if i < 0 or self.stack[i][:2] != l:
                return False
            i -= 1
        return True

    def pop(self):
        if self.stack:
            return self.stack.pop()
        
        raise ErrorHandler(ERROR, 'Empty pop')

    @staticmethod
    def _is_var(lex, value):
        return lex['lex'] == LEX['var'] and lex['value'] == value

    def analyze(self):
        lexer = self._analyze_lexemes()
        lex = next(lexer)
        if not Lexer._is_var(lex, 'ama'):# IMPROVE THIS ONE
            raise ErrorHandler(STARTING_TROUBLE)
        lex = next(lexer)
        if not Lexer._is_var(lex, 'miyan'):# IMPROVE THIS ONE
            raise ErrorHandler(STARTING_TROUBLE)
        lex = next(lexer)
        if not Lexer._is_var(lex, 'sunte'):# IMPROVE THIS ONE
            raise ErrorHandler(STARTING_TROUBLE)
        lex = next(lexer)
        if not Lexer._is_var(lex, 'ho'):# IMPROVE THIS ONE
            raise ErrorHandler(STARTING_TROUBLE)
        lexemes = list(lexer)
        end = 'milte kabhi budhwara be'.split()
        try:
            while end:
                if not Lexer._is_var(lexemes.pop(), end.pop()):
                    raise ErrorHandler(CONGRESS_RULE)
        except IndexError:
            raise ErrorHandler(CONGRESS_RULE)
        return lexemes

    def _analyze_lexemes(self):
        """
        Identify lexemes and return tokens.
        """
        num = 0
        self.stack = []
        self.clear = False
        for line in self.contents:
            num += 1
            offset = 0 
            length = len(line)
            while offset < length:
                token = line[offset]
                if self.clear: # what does this part do 
                    for lex in self.stack:
                        yield Lexer.lexeme(*lex)
                    self.stack = []
                    self.clear = False
                elif token.isspace(): # if token is ' ' 
                    # ignore staring spaces of a line!!!
                    offset += 1
                elif line[offset: offset + 2] in ('==', '&&', '||', '<=', '>=', '!='):
                    self._push(LEX[line[offset: offset + 2]], None, num, offset)# LEX from utils
                    # Now clear is true(push is called)
                    offset += 2
                elif token in '+-*/%(){}=<>!': # arithmetic singleton
                    self._push(LEX[token], None, num, offset)
                    offset += 1
                elif token.isdigit():
                    # if a nuber appears push the whole number as a single token
                    n = ''
                    o = offset
                    while o < length and line[o].isdigit():
                        n += line[o]
                        o += 1
                    self._push(LEX['num'], int(n), num, offset)
                    offset = o
                elif token.isalpha():
                    # same as number(push the whole word as a singleton)
                    w = ''
                    o = offset
                    while o < length and line[o].isalpha():
                        w += line[o]
                        o += 1
                    w = Lexer.normalize(w)
                    if w == 'agar':# agar -> if
                        self._push(LEX['if'], None, num, offset)
                    elif w == 'mano' and self.on_top((LEX['var'], 'kilap'), (LEX['var'], 'kar')):
                        self.pop()
                        _, _, lex_line, lex_offset = self.pop()
                        self._push(LEX['else'], None, lex_line, lex_offset)
                    elif w == 'toh': # toh 
                        self._push(LEX['then'], None, num, offset)# What is "then"!!
                    elif w == 'jabtak' and self.on_top((LEX['var'], 'aahista'), (LEX['var'], 'chalna')):
                        self.pop()
                        _, _, lex_line, lex_offset = self.pop()
                        self._push(LEX['until'], None, lex_line, lex_offset)
                    elif w == 'ho' and self.on_top((LEX['var'], 'ustaad'), (LEX['var'], 'sunte')):
                        self.pop()
                        _, _, lex_line, lex_offset = self.pop() # bhaiyo aur behno -> print (var!!)
                        self._push(LEX['print'], None, lex_line, lex_offset)
                    elif w == 'khan' and self.on_top((LEX['var'], 'ko')):
                        _, _, lex_line, lex_offset = self.pop()
                        self._push(LEX['input'], None, lex_line, lex_offset) # mann ki baat -> input
                    elif w == 'de' and self.on_top((LEX['var'], 'jodh')):# NOT TESTED
                        _, _, lex_line, lex_offset = self.pop()
                        self._push(LEX['+'], None, num, offset)
                    elif w == 'ke' and self.on_top((LEX['var'], 'rok')):# NOT TESTED
                        _, _, lex_line, lex_offset = self.pop()
                        self._push(LEX['-'], None, num, offset)
                    elif w == 'guna':
                        self._push(LEX['*'], None, num, offset)
                    elif w == 'ghata':
                        self._push(LEX['/'], None, num, offset)
                    elif w == 'modi':
                        self._push(LEX['%'], None, num, offset)
                    elif w == 'ke' and self.on_top((LEX['var'], 'ghata')):
                        _, _, lex_line, lex_offset = self.pop()
                        self._push(LEX['<'], 'word', num, offset)
                    elif w == 'ke' and self.on_top((LEX['var'], 'badha')):
                        _, _, lex_line, lex_offset = self.pop()
                        self._push(LEX['>'], 'word', num, offset)
                    elif w == 'barabar':
                        self._push(LEX['=='], 'word', num, offset)
                    elif w == 'aur': # aur -> &&
                        self._push(LEX['&&'], None, num, offset)
                        self.clear = False
                    elif w == 'ya':
                        self._push(LEX['||'], None, num, offset)
                    elif w == 'hega':
                        self._push(LEX['hai'], None, num, offset)
                    elif w == 'se':
                        pass
                    elif w == 'karra' and self.on_top((LEX['var'], 'bahut')):
                        _, _, lex_line, lex_offset = self.pop()
                        self._push(LEX['true'], None, num, offset)
                    elif w == 'bete' and self.on_top((LEX['var'], 'behtereen')):# NOT TESTED
                        _, _, lex_line, lex_offset = self.pop()
                        self._push(LEX['false'], None, num, offset)
                    else:
                        self._push(LEX['var'], w, num, offset)
                        self.clear = False
                    offset = o # o is end of word
                elif token == '"' or token == "'":
                    w = ''
                    o = offset + 1
                    while o < length and line[o] != token:
                        if line[o] == '\\':
                            o += 1
                        w += line[o]
                        o += 1
                    if o == length:
                        raise ErrorHandler(MISQUOTE, line)
                    self._push(LEX['str'], w, num, offset) # store as string "(jo bhi likha hai)"
                    offset = o + 1
                else:
                    self._push(LEX['sym'], num, offset) # sym !!!
                    offset += 1
        for lex in self.stack:
            yield Lexer.lexeme(*lex)
        self.stack = []
        self.clear = False
        if sys.version_info >= (3, 7):
            return
        raise StopIteration()
