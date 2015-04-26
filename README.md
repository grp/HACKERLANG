# HACKERLANG

HACKERLANG is a cool language for HACKERs.

## Syntax

### Comments

Comments are defined using `#`. They continue until the end of the line. Multiline comments are not supported.

### Method Calls

The most basic syntax is the method call. It looks like this:

    object method argument
    
Or, more concretely, to call the method "write-to" on a string:

    "hello world" write-to :stdout
    
Method calls are left-associative. Therefore, `"hello world" transform :uppercase write-to :stdout` is interpreted as `("hello world" transform :uppercase) write-to :stdout`. As you might guess, that writes the uppercase form of `"HELLO WORLD"` to the screen. However, `=` is special-cased to be right associative. Thus:
  
      &variable = "hello" + "world" # works as expected

Methods can also be called without an argument by appending an `!` or an `?` to the method name:

    "hello there" length! # => 11
    [] is_empty? # => true
    
By convention, `?` is used for predicate methods and `!` is used for other methods. Unlike Ruby, `!` does not indicate a destructive method. At an internal level, a `nil` argument is still passed. These methods are generally written with the final character appended.

Method names, for multi-stage methods, are written with spaces between them, such as `make with`, `set to`, or `method with`.

### Core Types
    
There are a bunch of built-in types:

- String: Just your normal string type. They look like this:

      "hello world"
  
  Or like this:
  
      'hello world'
      
  They define a method `+` for concatentation and `*` for repetition, as well as `length`, `replace with`, `find`, `slice to`, and other useful methods.
      
- Symbol. Just like Ruby. They look just like Ruby, too:

       :symbol_name
       
- Number. Not even going to give an example for this one, although the prefixes `0x`, `0b`, and `0` are supported for alternate bases. Numbers have the standard mathematical operations defined as methods. Note that as method calls are left-associative, the order of operations is not supported, and all operations are evaluated left-to-right.
- List. As usual, they are delimited with brackets:
      
       ["hi", "there", "this", "is", "a", "list"] 

- Tuples. Similar to Python, they use parentheses:

        ("hi", "i", "am", "a", "tuple")
        
  Single element tuples still need the awkward Python syntax:
  
        ("tuples are cool",)
        
  The method `at` is used to access a single tuple element by index. They also support the `=` operator, taking a tuple of names (or `nil`) on the left and a tuple of values on the right, which are matched in the local namespace.
        
- Nil. This type has one instance, `nil`, and generally behaves as in Objective-C: it will silently eat all method calls. An alias to `nil` is `_`.

- Block. These are similar to both Ruby and Objective-C blocks, and use curly braces for delimiters. They take one implicit parameter, `$`, when called: 

        { "hello" + $ write-to :stdout }

  As in Ruby, they implicitly return the last expression evalutated. To accept multiple parameters, you can create Smalltalk-like keyword arguments by returning an object accepting a method with the next keyword.
  
  Blocks capture the references to the values of all variables used inside them. However, the current values of a name upon execution can be accessed using the `value!` method of a name.
  
  As there are no functions, blocks cannot be called outside of the context of a method call.
  
- Boolean. There are two booleans, `true` and `false`. Booleans are used for flow control, as in Smalltalk. The flow control methods, such as `if`, take a block as a parameter. The standard construct `else` is also supported, as `if` returns an object that responds to the `else` method. This is best shown by an example:

       (4 + 3 = 5) if {
           "equal" write-to :stdout
       } else {
           "not equal" write-to :stdout
       }

- Name. Names are a way to directly address the name of an object, and are used for variables. Similar to symbols, they are prefixed, but use `&` instead of the colon. When no & is used as the target of a method, the contents of that name in this scope is used instead. Their most commonly used method, `=`, assigns a value to a name:

      &variable = "hello world"
      variable write-to :stdout
       
- Object. Objects are not a distinct core type (all other types inherit from objects at some level), but are used to create your own types. The most common method on the object type is `clone`, used to both create objects and types. It takes a block of code to customize the new object, whose parameter is the object itself. The symbol `@` refers to the current object, when a block is called as a method. This example creates a new template class, using only the fundamental object methods:

      &PlayingCard = Object clone {
          $ set &suit to { @ get &suit_ }
          $ set &suit= to { @ set &suit_ to $ }
          
          $ set &value to { @ get &value_ }
          $ set &value= to { @ set &value_ to $ }
          
          $ set &print to {
              @ value + "of" + @ suit write-to :stdout
          }
          
          $ set &ace to {
              @ value = 1 # equalitytest, not assignment
          }
      }

      &three_of_spades = PlayingCard clone!
      three_of_spades value= 7
      three_of_spades suit= "spades"
      three_of_spades print! # => 7 of spades
      three_of_spades ace? write-to :stdout

  The methods `get`, `set to`, and `remove` modify the object's slots (similar to instance or member variables in other languages). However, as this is somewhat cumbersome, more convenient wrapper syntax is also provided:
  
      &PlayingCard = Object clone {
          $ property &suit
          $ property &value
          
          $ method &print with {
              @ value + "of" + @ suit write-to :stdout
          }
          
          $ method &ace with {
              @ value = 1 # equality test, not assignment
          }
      }
      
  In this case, the `property` method covers creating an easily readable and writeable property, while `method` is a wrapper over the existing `set to` method. In addition, the `propertys` method takes a second, optional keyword argument `access`, which accepts the symbols `:read_only`, `:write_only`, and (the default) `:read_write`.
  
### Other Included Types

- Callable. To make using blocks easier, a method is needed to easily wrap them as an object. Callables are objects with a `call` method. You use them like this:
 
      &print = Callable with { $ write-to :stdout }
      print call "hello world"

  As the Callable object itself is what hosts the `call` method and the block, it can be accessed inside the block with `@`. The Callable object might be implemented as follows:
  
      &Callable = Object clone {
          $ method &with with {
              &block = $
          
              Object clone {
                  $ method &call with block
                  $ method &block with { block }
              }
          }
      }
  
- Keyword. To more easily enable keyword methods to be created without custom objects each time, you can instead return a Keyword object, created with the `make with` method. The Keyword type is defined as follows:

      &Keyword = Object clone {
          $ method &make {
              &name = $
              
              Object clone {
                  $ method &with {
                      &block = $
                      
                      Object clone {
                          $ method name with block
                      }
                  }
              }
          }
      }

  An example of using it, as an example of how you might define Object's `method` method:
  
      Object property &method
      Object set &method to {
          &target = @
          &name = $
      
          Keyword make &with with {
              &block = $
              
              target set name to block
          }
      }

  Note that you must manually save `@` for it to be available in the keyword body, as the current object is never passed to Keyword's `make with` method.

## Speed

How fast is it? It doesn't exist yet, that's how fast.















    
