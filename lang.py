



class LObjectClass(object):
    def __init__(self, prototype):
        self.slots = {}
        self.slots['prototype'] = prototype
        self.slots['clone'] = self._clone

        self.repr = lambda self: "<object prototype=%s>" % (self, self.slots['prototype'].repr())
    def get(self, name):
        if name in self.slots: return self.slots[name]
        obj = self
        while obj.slots['prototype'] is not None:
            obj = obj.slots['prototype']
            if name in obj.slots: return obj.slots[name]
        return None
    def method_call(self, name, argument):
        target = self.get(name)
        return target(self, argument)
    def clone(self, arg=None):
        return self.method_call('clone', arg) 
    def _clone(self, prototype, arg=None):
        prototype = self
        ret = LObjectClass(prototype)
        ret.repr = prototype.repr
        # ret.__call__ = prototype.__call__
        if arg is not None: arg(prototype, ret)
        return ret

LObject = LObjectClass(None)

LString = LObject.clone()
LString.slots['length'] = lambda self, arg: LNumberCreate(len(self.value))
LString.slots['+'] = lambda self, arg: LStringCreate(self.string + arg.string)
LString.repr = lambda self: "<string %s>" % self.string

LSymbol = LObject.clone()
LSymbol.repr = lambda self: "<symbol :%s>" % self.symbol

LName = LObject.clone()
LName.repr = lambda self: "<name &%s>" % self.name

LNumber = LObject.clone()
LNumber.slots['+'] = lambda self, arg: LNumberCreate(self.number + arg.number)
LNumber.slots['*'] = lambda self, arg: LNumberCreate(self.number * arg.number)
LNumber.slots['/'] = lambda self, arg: LNumberCreate(self.number / arg.number)
LNumber.slots['-'] = lambda self, arg: LNumberCreate(self.number - arg.number)
LNumber.repr = lambda self: "<number %s>" % self.number

LBlock = LObject.clone()
LBlock.__call__ = lambda self, target, arg: self.code(target, arg)
LBlock.slots['call'] = lambda self, arg: self(self, arg)
LBlock.repr = lambda self: "<block %s>" % repr(self.code)

LTuple = LObject.clone()
LTuple.slots['at'] = lambda self, arg: self.value[arg]
LTuple.repr = lambda self: "<tuple %s>" % repr(self.value)

LList = LObject.clone()
LList.slots['at'] = lambda self, arg: self.value[arg]
LTuple.repr = lambda self: "<list %s>" % repr(self.value)

def LSymbolCreate(symbol):
    s = LSymbol.clone()
    s.symbol = symbol
    return s

def LStringCreate(string):
    s = LString.clone()
    s.string = string
    return s

def LNumberCreate(number):
    n = LNumber.clone()
    n.number = number
    return n

def LNameCreate(name):
    n = LName.clone()
    n.name = name
    return n

def LBlockCreate(code):
    b = LBlock.clone()
    b.code = code
    return b

def LTupleCreate(tuple):
    t = LTuple.clone()
    t.value = tuple
    return t

def LListCreate(list):
    l = LList.clone()
    l.value = list
    return l

def LObjectRepr(obj):
    return obj.repr(obj)

# global_scope = LScope.clone()

print LObjectRepr(LStringCreate("hello").method_call('+', LStringCreate(" world")))
print LObjectRepr(LNumberCreate(75).method_call('+', LNumberCreate(22).method_call('/', LNumberCreate(2))))
print LObjectRepr(LSymbolCreate("stdout"))
print LObjectRepr(LNameCreate("variable"))

from pyparsing import *

# parse action -maker
def makeLRlike(numterms):
    if numterms is None:
        # None operator can only by binary op
        initlen = 2
        incr = 1
    else:
        initlen = {0:1,1:2,2:3,3:5}[numterms]
        incr = {0:1,1:1,2:2,3:4}[numterms]

    # define parse action for this number of terms,
    # to convert flat list of tokens into nested list
    def pa(s,l,t):
        t = t[0]
        if len(t) > initlen:
            ret = ParseResults(t[:initlen])
            i = initlen
            while i < len(t):
                ret = ParseResults([ret] + t[i:i+incr])
                i += incr
            return ParseResults([ret])
    return pa


ParserElement.setDefaultWhitespaceChars('')

space = Suppress(OneOrMore(Literal(' ') | Literal('\t')))
word = Word(alphas + "_" + "-" + "=" + "+")

decimal = Word(nums)
hex = Combine((Literal('0x') | Literal('0X')) + Word(nums + 'abcdefABCDEF'))
binary = Combine((Literal('0b') | Literal('0B')) + Word('01'))
octal = Combine(Literal('0') + Word('01234567'))
number = (hex | binary | octal | decimal)

name = Combine(Literal('&') + word)
symbol = Combine(Literal(':') + word)
string = QuotedString('"', '\\') | QuotedString("'", '\\')

method = word
bang = Optional(Literal("!") | Literal("?"))
var = word

self = Literal('@')
arg = Literal('$')

code = Forward()

block = Group(Suppress(Literal('{')) + space + code + space + Suppress(Literal('}')))
literal = (name | symbol | string | number | var | self | arg | block)

call = literal + ZeroOrMore(space + ((method + Optional(space + literal)) | (method + bang)))

expr = operatorPrecedence(call, [(method, 2, opAssoc.LEFT, makeLRlike(None))])

stmt = expr # (expr + Suppress(Literal(';') | LineEnd() | StringEnd()))
code << ZeroOrMore(stmt)

raw_input()
print code.parseString("")
raw_input()
print code.parseString("4 factorial!")
raw_input()
print code.parseString("2 plus 2")
raw_input()
print code.parseString("5 times 5 plus 4")
raw_input()
print code.parseString("(&hello = 5) write-to :stdout;\n:test do-something-to-yourself!")
raw_input()
print code.parseString("@ copy-in ('hello' write-to (File open 'test.txt'))")
raw_input()
print code.parseString("{ $ write-to :stdout } call 0xdEaDf00d")
raw_input()
print code.parseString("0755 factorial!")
raw_input()
print code.parseString("""(((4 + 3) == 5) if { \"equal\" write-to :stdout }) else { \"not equal\" write-to :stdout }""")
raw_input()
print code.parseString("""(4 + 3 == 5) if { "equal" write-to :stdout } else { "not equal" write-to :stdout }""")
#print code.parseString("'hello' transform :uppercase")



