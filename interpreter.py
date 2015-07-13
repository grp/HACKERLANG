
from lexer import Token
from parser import Expression, Block

class Value(object):
    def __init__(self, interpreter):
        self.interpreter = interpreter
        pass
    def evaluate(self, arg):
        self.scope = {}
        self.argument = arg
        return self

class InterpretedBlock(Value):
    def __init__(self, interpreter, block):
        Value.__init__(self, interpreter)
        self.block = block
    def evaluate(self, arg):
        Value.evaluate(self, arg)

        ret = None
        self.interpreter.stack.append(self)
        for expr in self.block.expressions:
            ret = self.interpreter.expression(expr)
        self.interpreter.stack.pop()
        return ret
        
class NativeBlock(Value):
    def __init__(self, interpreter, impl):
        Value.__init__(self, interpreter)
        self.impl = impl
    def evaluate(self, arg):
        Value.evaluate(self, arg)
        return self.impl(self, arg)

class RootBlock(Value):
    def __init__(self, interpreter, block, block_arg):
        Value.__init__(self, interpreter)
        self.block = block
        self.block_arg = block_arg
    def evaluate(self, arg):
        Value.evaluate(self, arg)

        import sys
        self.scope = {
            Token(Token.IDENTIFIER, 'hello') : NativeBlock(self.interpreter, lambda block, arg: sys.stdout.write('Hello, World!\n')),
        }

        self.interpreter.stack.append(self)
        ret = self.block.evaluate(self.block_arg)
        self.interpreter.stack.pop()
        return ret

class Interpreter(object):
    def __init__(self):
        self.stack = []
    def interpret(self, ast, arg):
        interpreted = InterpretedBlock(self, ast)
        root = RootBlock(self, interpreted, arg)
        return root.evaluate(arg)
    def expression(self, expr):
        assert isinstance(expr, Expression)
        target = self.value(expr.target)
        action = None
        if expr.action is not None:
            action = self.value(expr.action)
        return target.evaluate(action)
    def lookup(self, identifier):
        assert isinstance(identifier, Token)
        assert identifier.type == Token.IDENTIFIER

        for block in reversed(self.stack):
            if identifier in block.scope:
                return block.scope[identifier]
        print 'Error: Unable to lookup identifier %s' % identifier
    def value(self, value):
        if isinstance(value, Expression):
            return self.expression(value)
        elif isinstance(value, Block):
            return InterpretedBlock(value)
        else:
            assert isinstance(value, Token)
            if value.type == Token.SELF:
                return self.stack[-1]
            elif value.type == Token.ARGUMENT:
                return self.stack[-1].argument
            elif value.type == Token.SCOPE:
                return self.stack[-1].scope
            elif value.type == Token.IDENTIFIER:
                return self.lookup(value)
            else:
                return value
            

