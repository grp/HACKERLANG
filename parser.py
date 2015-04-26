
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
    def __init__(self, target, action, param=None):
        self.target = target
        self.action = action
        self.param = param
    def __repr__(self):
        if self.param is not None:
            return '(%s %s %s)' % (repr(self.target), repr(self.action), repr(self.param))
        else:
            return '(%s %s)' % (repr(self.target), repr(self.action))

class Parser(object):
    def next(self, tokens, index):
        token = tokens[index]
        index += 1
        return token, index
    def value(self, tokens, index):
        token, index = self.next(tokens, index)

        if token.type == Token.OPEN_PARENTHESIS:
            value, index = self.expression(tokens, index)
            _, index = self.next(tokens, index)
        elif token.type == Token.OPEN_BLOCK:
            exprs, index = self.expressions(tokens, index, end_type=Token.CLOSE_BLOCK)
            value = Block(exprs)
            _, index = self.next(tokens, index)
        elif token.type == Token.SEPARATOR:
            value = None
        else:
            value = Value(token)

        return value, index
    def expression(self, tokens, index, target=None):
        if target is None:
            target, index = self.value(tokens, index)        
        if target is None:
            return None, index

        token, index = self.next(tokens, index)

        if token.type == Token.IDENTIFIER:
            value = None
            if token.value[-1:] != '!':
                value, index = self.value(tokens, index)
            e = Expression(target, Value(token), value)
            expr, index = self.expression(tokens, index, e)
            return expr, index
        else:
            index -= 1
            return target, index
    def expressions(self, tokens, index, end_type=None):
        expressions = []

        while index < len(tokens) and tokens[index].type != end_type:
            expr, index = self.expression(tokens, index)
            if expr is not None:
                expressions.append(expr)
            
        return expressions, index
    def parse(self, tokens, index=0):
        return Block(self.expressions(tokens, index)[0])


