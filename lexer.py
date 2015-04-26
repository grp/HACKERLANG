
class Token(object):
    SEPARATOR = 'SEPARATOR'

    SELF = 'SELF'
    SCOPE = 'SCOPE'
    ARGUMENT = 'ARGUMENT'

    NAME = 'NAME'
    SYMBOL = 'SYMBOL'
    STRING = 'STRING'
    IDENTIFIER = 'IDENTIFIER'

    OPEN_PARENTHESIS = 'OPEN_PARENTHESIS'
    CLOSE_PARENTHESIS = 'CLOSE_PARENTHESIS'

    OPEN_BLOCK = 'OPEN_BLOCK'
    CLOSE_BLOCK = 'CLOSE_BLOCK'

    def __init__(self, type, value):
        self.type = type
        self.value = value
    def __str__(self):
        if self.type == Token.SEPARATOR:
            return ' '
        elif self.type == Token.SELF:
            return '@'
        elif self.type == Token.SCOPE:
            return '#'
        elif self.type == Token.ARGUMENT:
            return '$'
        elif self.type == Token.NAME:
            return '&%s' % self.value
        elif self.type == Token.SYMBOL:
            return ':%s' % self.value
        elif self.type == Token.STRING:
            return '"%s"' % self.value
        elif self.type == Token.IDENTIFIER:
            return self.value
        elif self.type == OPEN_PARENTHESIS:
            return '('
        elif self.type == CLOSE_PARENTHESIS:
            return ')'
        elif self.type == OPEN_BLOCK:
            return '{'
        elif self.type == CLOSE_BLOCK:
            return '}'
    def __repr__(self):
        if self.value is not None:
            return '%s(%s)' % (self.type, self.value)
        else:
            return self.type

class State(object):
    def __init__(self, text):
        self.text = text
        self.index = 0
    def current(self):
        return self.text[self.index]
    def done(self):
        return self.index >= len(self.text)
    def next(self):
        c = self.current()
        self.index += 1
        return c
    def named(self, end = None):
        value = ''
        while not self.done() and self.current() not in end:
            value += self.next()
        return value
    def delimited(self, end = None):
        value = ''
        while self.current() not in end:
            value += self.next()
        self.next()
        return value

class Lexer(object):
    WHITESPACE_CHARACTERS = ' \t'
    SEPARATOR_CHARACTERS = ';\n'
    DELIMITER_CHARACTERS = '{}()'
    SPECIAL_CHARACTERS = DELIMITER_CHARACTERS + SEPARATOR_CHARACTERS + WHITESPACE_CHARACTERS

    def tokenize(self, text):
        state = State(text)
        tokens = []

        while not state.done():
            c = state.next()

            if c in Lexer.WHITESPACE_CHARACTERS:
                continue
            elif c in Lexer.SEPARATOR_CHARACTERS:
                t = Token(Token.SEPARATOR, None)
                tokens.append(t)
            elif c == '(':
                t = Token(Token.OPEN_PARENTHESIS, None)
                tokens.append(t)
            elif c == ')':
                t = Token(Token.CLOSE_PARENTHESIS, None)
                tokens.append(t)
            elif c == '{':
                t = Token(Token.OPEN_BLOCK, None)
                tokens.append(t)
            elif c == '}':
                t = Token(Token.CLOSE_BLOCK, None)
                tokens.append(t)
            elif c == '@':
                t = Token(Token.SELF, None)
                tokens.append(t)
            elif c == '#':
                t = Token(Token.SCOPE, None)
                tokens.append(t)
            elif c == '$':
                t = Token(Token.ARGUMENT, None)
                tokens.append(t)
            elif c == ':':
                t = Token(Token.SYMBOL, state.named(end = Lexer.SPECIAL_CHARACTERS))
                tokens.append(t)
            elif c == '&':
                t = Token(Token.NAME, state.named(end = Lexer.SPECIAL_CHARACTERS))
                tokens.append(t)
            elif c == '"' or c == "'":
                t = Token(Token.STRING, state.delimited(end = '"' + "'"))
                tokens.append(t)
            else:
                t = Token(Token.IDENTIFIER, c + state.named(end = Lexer.SPECIAL_CHARACTERS))
                tokens.append(t)

        t = Token(Token.SEPARATOR, None)
        tokens.append(t)
        return tokens
