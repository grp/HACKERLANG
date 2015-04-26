
from lexer import Token

class Block(object):
    def __init__(self, exprs):
        self.expressions = exprs
    def __repr__(self):
        return '{%s}' % ', '.join(repr(x) for x in self.expressions)

class Value(object):
    def __init__(self, token):
        self.token = token
    def __repr__(self):
        return '<%s>' % repr(self.token)

class Expression(object):
    def __init__(self, target, action):
        self.target = target
        self.action = action
    def __repr__(self):
        return '(%s %s)' % (repr(self.target), repr(self.action))

class Parser(object):
    def next(self, tokens, index):
        token = tokens[index]
        index += 1
        return token, index
    def value(self, tokens, index):
        token, index = self.next(tokens, index)

        if token.type == Token.OPEN_PARENTHESIS:
            value, index = self.expression(tokens, index, Token.CLOSE_PARENTHESIS)
            _, index = self.next(tokens, index)
        elif token.type == Token.OPEN_BLOCK:
            exprs, index = self.expressions(tokens, index, Token.CLOSE_BLOCK)
            value = Block(exprs)
            _, index = self.next(tokens, index)
        elif token.type == Token.CLOSE_PARENTHESIS or token.type == Token.CLOSE_BLOCK:
            raise Exception('Error: Expected value, but was %s' % token)
        elif token.type == Token.SEPARATOR:
            value = None
        else:
            value = Value(token)

        return value, index
    def expression(self, tokens, index, end_type, target=None):
        if target is None:
            target, index = self.value(tokens, index)        
        if target is None:
            return None, index

        token, _ = self.next(tokens, index)

        if token.type != end_type:
            action, index = self.value(tokens, index)
            if action:
                expr = Expression(target, action)
                expr, index = self.expression(tokens, index, end_type, expr)
                return expr, index
            else:
                return target, index
        else:
            return target, index
    def expressions(self, tokens, index, end_type):
        expressions = []

        print end_type, 'hi'

        while index < len(tokens) and tokens[index].type != end_type:
            expr, index = self.expression(tokens, index, end_type or Token.SEPARATOR)
            if expr is not None:
                expressions.append(expr)
            
        return expressions, index
    def parse(self, tokens, index=0):
        exprs, _ = self.expressions(tokens, index, None)
        return Block(exprs)


