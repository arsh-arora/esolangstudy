from .lexer import Lexer
from .parser import Parser
import ast

class ModiScript:
    def __init__(self, debug=False): # default value of debug is false
        self.debug = debug

    def _compile_file(self, value, value_type="filename",):
        lex_out = Lexer(value, value_type).analyze() #Call to Lexer from lexer.py
        if self.debug and value_type == "filename": # if debug is true
            filename = value
            with open(filename.split('.', 1)[0] + ".txt", "w") as f: # create filename.txt from filename.chai
                print(*lex_out, sep='\n', file=f)
        parse_out = Parser(lex_out).parse()
        if self.debug and value_type == "filename":
            with open(filename.split('.', 1)[0] + ".py", "w") as f:
                print(ast.dump(parse_out), file=f)
        return compile(ast.unparse(parse_out),"<ast>", "exec",) # compiles python code

    def execute(self, value, value_type="filename"): # value is filename
        ast_module = self._compile_file(value, value_type)
        exec(ast_module) # Execute the program
