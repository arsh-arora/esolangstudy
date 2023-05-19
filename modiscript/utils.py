PROGRAM = "MODI"
FNF = 404
MISQUOTE = 500
STARTING_TROUBLE = 'Go lzisten to Modi'
CONGRESS_RULE = 'Acche din nahi aaye'
ERROR = "Oops. Are you sure you're right?"

LEX = {
    '+': 0,
    '-': 1,
    '*': 2,
    '/': 3,
    '%': 4,
    '==': 10,
    '<': 11,
    '>': 12,
    '<=': 13,
    '>=': 14,
    '!=': 15,
    '!': 20,
    '&&': 21,
    '||': 22,
    '(': 30,
    ')': 31,
    '{': 32,
    '}': 33,
    '=': 34,
    'if': 40,
    'then': 41,
    'else': 42,
    'until': 43,
    'print': 44,
    'input': 45,
    'hai': 50,
    'var': 100,
    'num': 101,
    'str': 102,
    'sym': 103,
    'true': 104,
    'false': 105
}

WORDS = { # change this
    "nahin": "nahi", # CHANGE THESE
    "tho": "toh",
    "bhayyo": "bhaiyo",
    "beheno": "behno",
    "thak": "tak",
    "jyada": "zyada",
    "ahista": "aahista"
}


def usage():
    print("Usage:", PROGRAM, "[options]", "filename")
    print("-d, --debug\n\toutput lex and parse details to files.")
    quit()


class ErrorHandler(Exception):
    def __init__(self, code, *args):
        self.code = code
        self.args = args

    def __str__(self):
        return ('Error: %s\n:' % self.code) + str(self.args)
