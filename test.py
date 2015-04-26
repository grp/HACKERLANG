
import sys

from lexer import Lexer, Token
from parser import Parser, Block, Value, Expression

def fmt(v, level=0):
    indent = level * '  '
    if isinstance(v, Value):
        return str(v.token)
    elif isinstance(v, Expression):
        if v.param is not None:
            return '(%s %s %s)' % (fmt(v.target, level), fmt(v.action, level), fmt(v.param, level))
        else:
            return '(%s %s)' % (fmt(v.target, level), fmt(v.action, level))
    elif isinstance(v, Block):
        return '{\n' + fmt(v.expressions, level + 1) + '\n' + indent + '}'
    elif isinstance(v, list):
        return '\n'.join(indent + fmt(x, level) for x in v)  
    else:
        return ''

def test(text):
    print
    print text
    lexer = Lexer()
    tokens = lexer.tokenize(text)
    print tokens
    parser = Parser()
    ast = parser.parse(tokens)
    print ast

    print fmt(ast)



if __name__ == '__main__':
    test('hello')
    test('"Hello World"')
    test('"Hello World"')
    test('2 + 2')
    test('"str" transform :uppercase write-to :stdout')
    test('("str" uppercase!) write-to :stdout')
    test('("str" uppercase!) write-to :stdout; "hello" write-to :stderr')
    test('(2 + 4) factorial! factorial!')
    test('''(a = b) if {
            "yes" write-to :stdout
        } else {
            "no" write-to :stderr
        }''')
    test('''&Callable = Object clone {
            ("str" transform :uppercase) write-to :stdout
            (("world" prepend "hello") transform :lowercase)
        }''')
    test("""
          &Callable = (Object clone {
              $ method &with with {
                  &block = $
              
                  Object clone {
                      $ method &call with block
                      $ method &block with { block }
                  }
              }
          }
    """)
    test("""
      &Keyword = Object clone {
          $ method &make = {
              &name = $
              
              Object clone {
                  $ method &with = {
                      &block = $
                      
                      Object clone {
                          $ method name with block
                      }
                  }
              }
          }
      }
    """)


