
# Lexer's job is to turn the source code into tokens

from compiler.exceptions import SyntaxErrorException
from compiler.consts import KEYWORDS, Consts, TokenTypes


class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        if self.value: return f"{self.type}:{self.value}"
        return f"{self.type}"

class Lexer:
    def __init__(self, fs):
        self.fs = fs
        self.pos = -1

        self.curr_char = self.fs[self.pos]

        self.next()
    
    def next(self):
        self.pos += 1
        self.curr_char = self.fs[self.pos] if self.pos < len(self.fs) else None
    
    def generate_tokens(self):
        tokens = []
        
        while self.curr_char != None:
            if self.curr_char in '\n':
                tokens.append(Token(TokenTypes.NEWLINE))
                self.next()
            elif self.curr_char in ' ':
                self.next()
            elif self.curr_char in Consts.DIGITS:
                tokens.append(self.generate_numero())
            elif self.curr_char in Consts.LETTERS:
                tokens.append(self.generate_identifier())
            elif self.curr_char in '"':
                tokens.append(self.generate_letra())
            elif self.curr_char in ':':
                tokens.append(self.generate_equals())
            elif self.curr_char in '+':
                tokens.append(Token(TokenTypes.PLUS))
                self.next()
            elif self.curr_char in '-':
                tokens.append(Token(TokenTypes.MINUS))
                self.next()
            elif self.curr_char in '*':
                tokens.append(Token(TokenTypes.TIMES))
                self.next()
            elif self.curr_char in '/':
                tokens.append(Token(TokenTypes.DIVIDE))
                self.next()
            elif self.curr_char in '(':
                tokens.append(Token(TokenTypes.LEFT_PARENTHESIS))
                self.next()
            elif self.curr_char in ')':
                tokens.append(Token(TokenTypes.RIGHT_PARENTHESIS))
                self.next()
            elif self.curr_char in '[':
                tokens.append(Token(TokenTypes.LEFT_BRACKET))
                self.next()
            elif self.curr_char in ']':
                tokens.append(Token(TokenTypes.RIGHT_BRACKET))
                self.next()
            elif self.curr_char in '<':
                tokens.append(self.generate_type())
                self.next()
            elif self.curr_char in ',':
                tokens.append(Token(TokenTypes.COMMA))
                self.next()
            else:
                self.next()
                return []

        tokens.append(Token(TokenTypes.EOF))
            
        return tokens

    def generate_numero(self):
        number_prototype = ""

        while self.curr_char != None and self.curr_char in Consts.DIGITS:
            number_prototype += self.curr_char
            self.next()

        return Token(TokenTypes.NUMERO, number_prototype)

    def generate_letra(self):
        letra_prototype = ""
        escaped = False
        
        self.next()

        while self.curr_char != None and (self.curr_char != '"'):
            if escaped:
                letra_prototype += '\n'
            else:
                if self.curr_char == '\\':
                    escaped = True
                else:
                    letra_prototype += self.curr_char
            
            self.next()
            escaped = False

        self.next()

        return Token(TokenTypes.LETRA, letra_prototype)

    def generate_identifier(self):
        identifier_prototype = ""

        while self.curr_char != None and self.curr_char in Consts.LETTERS_DIGITS:
            identifier_prototype += self.curr_char
            self.next()

        type = TokenTypes.KEYWORD if identifier_prototype in KEYWORDS else TokenTypes.IDENTIFIER
        return Token(type, identifier_prototype)

    def generate_equals(self):
        equals_type = TokenTypes.EQUALS
        self.next()

        if self.curr_char == "=":
            self.next()
            equals_type = TokenTypes.DOUBLE_EQUALS

        return Token(equals_type)

    def generate_type(self):
        self.next()
        type_type = ""

        while self.curr_char != None and (self.curr_char != '>'):
            type_type += self.curr_char
            self.next()

        type_type = type_type.lower()
        type = None

        if type_type == "letra":
            type = TokenTypes.LETRA
        elif type_type == "numero":
            type = TokenTypes.NUMERO
        elif type_type == "ano":
            type = TokenTypes.ANO
        elif type_type == "kahitano":
            type = TokenTypes.KAHITANO
        else:
            SyntaxErrorException(type_type, self.pos)

        return Token(TokenTypes.TYPE, type)

