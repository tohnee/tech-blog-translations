---
title: "Python 2 vs 3 Key Differences"
source: https://sebastianraschka.com/Articles/2014_python_2_3_key_diff.html
crawled: 2026-09-06
---

# Python 2 vs 3 Key Differences

Many beginning Python users are wondering with which version of Python they should start. My answer to this question is usually something along the lines “just go with the version your favorite tutorial was written in, and check out the differences later on.”

But what if you are starting a new project and have the choice to pick? I would say there is currently no “right” or “wrong” as long as both Python 2.7.x and Python 3.x support the libraries that you are planning to use. However, it is worthwhile to have a look at the major differences between those two most popular versions of Python to avoid common pitfalls when writing the code for either one of them, or if you are planning to port your project.

## Sections

## The `__future__` module

Python 3.x introduced some Python 2-incompatible keywords and features that can be imported via the in-built `__future__` module in Python 2. It is recommended to use `__future__` imports it if you are planning Python 3.x support for your code. For example, if we want Python 3.x’s integer division behavior in Python 2, we can import it via

```python
from __future__ import division
```

More features that can be imported from the `__future__` module are listed in the table below:

| feature | optional in | mandatory in | effect |
| --- | --- | --- | --- |
| nested\_scopes | 2.1.0b1 | 2.2 | [**PEP 227**](https://www.python.org/dev/peps/pep-0227): *Statically Nested Scopes* |
| generators | 2.2.0a1 | 2.3 | [**PEP 255**](https://www.python.org/dev/peps/pep-0255): *Simple Generators* |
| division | 2.2.0a2 | 3.0 | [**PEP 238**](https://www.python.org/dev/peps/pep-0238): *Changing the Division Operator* |
| absolute\_import | 2.5.0a1 | 3.0 | [**PEP 328**](https://www.python.org/dev/peps/pep-0328): *Imports: Multi-Line and Absolute/Relative* |
| with\_statement | 2.5.0a1 | 2.6 | [**PEP 343**](https://www.python.org/dev/peps/pep-0343): *The “with” Statement* |
| print\_function | 2.6.0a2 | 3.0 | [**PEP 3105**](https://www.python.org/dev/peps/pep-3105): *Make print a function* |
| unicode\_literals | 2.6.0a2 | 3.0 | [**PEP 3112**](https://www.python.org/dev/peps/pep-3112): *Bytes literals in Python 3000* |

(Source: [https://docs.python.org/2/library/\_\_future\_\_.html](https://docs.python.org/2/library/\_\_future\_\_.html#module-\_\_future\_\_))

```python
from platform import python_version
```

## The print function

Very trivial, and the change in the print-syntax is probably the most widely known change, but still it is worth mentioning: Python 2’s print statement has been replaced by the `print()` function, meaning that we have to wrap the object that we want to print in parantheses.

Python 2 doesn’t have a problem with additional parantheses, but in contrast, Python 3 would raise a `SyntaxError` if we called the print function the Python 2-way without the parentheses.

### Python 2

```python
print 'Python', python_version()
print 'Hello, World!'
print('Hello, World!')
print "text", ; print 'print more text on the same line'
```

```python
Python 2.7.6
Hello, World!
Hello, World!
text print more text on the same line
```

### Python 3

```python
print('Python', python_version())
print('Hello, World!')

print("some text,", end="")
print(' print more text on the same line')
```

```python
Python 3.4.1
Hello, World!
some text, print more text on the same line
```

```python
print 'Hello, World!'
```

```python
  File "<ipython-input-3-139a7c5835bd>", line 1
    print 'Hello, World!'
                        ^
SyntaxError: invalid syntax
```

**Note:**

Printing “Hello, World” above via Python 2 looked quite “normal”. However, if we have multiple objects inside the parantheses, we will create a tuple, since `print` is a “statement” in Python 2, not a function call.

```python
print 'Python', python_version()
print('a', 'b')
print 'a', 'b'
```

```python
Python 2.7.7
('a', 'b')
a b
```

## Integer division

This change is particularly dangerous if you are porting code, or if you are executing Python 3 code in Python 2, since the change in integer-division behavior can often go unnoticed (it doesn’t raise a `SyntaxError`).  
So, I still tend to use a `float(3)/2` or `3/2.0` instead of a `3/2` in my Python 3 scripts to save the Python 2 guys some trouble (and vice versa, I recommend a `from __future__ import division` in your Python 2 scripts).

### Python 2

```python
print 'Python', python_version()
print '3 / 2 =', 3 / 2
print '3 // 2 =', 3 // 2
print '3 / 2.0 =', 3 / 2.0
print '3 // 2.0 =', 3 // 2.0
```

```python
Python 2.7.6
3 / 2 = 1
3 // 2 = 1
3 / 2.0 = 1.5
3 // 2.0 = 1.0
```

### Python 3

```python
print('Python', python_version())
print('3 / 2 =', 3 / 2)
print('3 // 2 =', 3 // 2)
print('3 / 2.0 =', 3 / 2.0)
print('3 // 2.0 =', 3 // 2.0)
```

```python
Python 3.4.1
3 / 2 = 1.5
3 // 2 = 1
3 / 2.0 = 1.5
3 // 2.0 = 1.0
```

## Unicode

Python 2 has ASCII `str()` types, separate `unicode()`, but no `byte` type.

Now, in Python 3, we finally have Unicode (utf-8) `str`ings, and 2 byte classes: `byte` and `bytearray`s.

### Python 2

```python
print 'Python', python_version()
```

```python
Python 2.7.6
```

```python
print type(unicode('this is like a python3 str type'))
```

```python
<type 'unicode'>
```

```python
print type(b'byte type does not exist')
```

```python
<type 'str'>
```

```python
print 'they are really' + b' the same'
```

```python
they are really the same
```

```python
print type(bytearray(b'bytearray oddly does exist though'))
```

```python
<type 'bytearray'>
```

### Python 3

```python
print('Python', python_version())
print('strings are now utf-8 \u03BCnico\u0394é!')
```

```python
Python 3.4.1
strings are now utf-8 μnicoΔé!
```

```python
print('Python', python_version(), end="")
print(' has', type(b' bytes for storing data'))
```

```python
Python 3.4.1 has <class 'bytes'>
```

```python
print('and Python', python_version(), end="")
print(' also has', type(bytearray(b'bytearrays')))
```

```python
and Python 3.4.1 also has <class 'bytearray'>
```

```python
'note that we cannot add a string' + b'bytes for data'
```

```python
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)

<ipython-input-13-d3e8942ccf81> in <module>()
----> 1 'note that we cannot add a string' + b'bytes for data'

TypeError: Can't convert 'bytes' object to str implicitly
```

## xrange

The usage of `xrange()` is very popular in Python 2.x for creating an iterable object, e.g., in a for-loop or list/set-dictionary-comprehension.  
The behavior was quite similar to a generator (i.e., “lazy evaluation”), but here the xrange-iterable is not exhaustible - meaning, you could iterate over it infinitely.

Thanks to its “lazy-evaluation”, the advantage of the regular `range()` is that `xrange()` is generally faster if you have to iterate over it only once (e.g., in a for-loop). However, in contrast to 1-time iterations, it is not recommended if you repeat the iteration multiple times, since the generation happens every time from scratch!

In Python 3, the `range()` was implemented like the `xrange()` function so that a dedicated `xrange()` function does not exist anymore (`xrange()` raises a `NameError` in Python 3).

```python
import timeit

n = 10000
def test_range(n):
    return for i in range(n):
        pass

def test_xrange(n):
    for i in xrange(n):
        pass
```

### Python 2

```python
print 'Python', python_version()

print '\ntiming range()'
%timeit test_range(n)

print '\n\ntiming xrange()'
%timeit test_xrange(n)
```

```python
Python 2.7.6

timing range()
1000 loops, best of 3: 433 µs per loop

timing xrange()
1000 loops, best of 3: 350 µs per loop
```

### Python 3

```python
print('Python', python_version())

print('\ntiming range()')
%timeit test_range(n)
```

```python
Python 3.4.1

timing range()
1000 loops, best of 3: 520 µs per loop
```

```python
print(xrange(10))
```

```python
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)

<ipython-input-5-5d8f9b79ea70> in <module>()
----> 1 print(xrange(10))

NameError: name 'xrange' is not defined
```

### The `__contains__` method for `range` objects in Python 3

Another thing worth mentioning is that `range` got a “new” `__contains__` method in Python 3.x (thanks to [Yuchen Ying](https://github.com/yegle), who pointed this out). The `__contains__` method can speedup “look-ups” in Python 3.x `range` significantly for integer and Boolean types.

```python
x = 10000000
```

```python
def val_in_range(x, val):
    return val in range(x)
```

```python
def val_in_xrange(x, val):
    return val in xrange(x)
```

```python
print('Python', python_version())
assert(val_in_range(x, x/2) == True)
assert(val_in_range(x, x//2) == True)
%timeit val_in_range(x, x/2)
%timeit val_in_range(x, x//2)
```

```python
Python 3.4.1
1 loops, best of 3: 742 ms per loop
1000000 loops, best of 3: 1.19 µs per loop
```

Based on the `timeit` results above, you see that the execution for the “look up” was about 60,000 faster when it was of an integer type rather than a float. However, since Python 2.x’s `range` or `xrange` doesn’t have a `__contains__` method, the “look-up speed” wouldn’t be that much different for integers or floats:

```python
print 'Python', python_version()
assert(val_in_xrange(x, x/2.0) == True)
assert(val_in_xrange(x, x/2) == True)
assert(val_in_range(x, x/2) == True)
assert(val_in_range(x, x//2) == True)
%timeit val_in_xrange(x, x/2.0)
%timeit val_in_xrange(x, x/2)
%timeit val_in_range(x, x/2.0)
%timeit val_in_range(x, x/2)
```

```python
Python 2.7.7
1 loops, best of 3: 285 ms per loop
1 loops, best of 3: 179 ms per loop
1 loops, best of 3: 658 ms per loop
1 loops, best of 3: 556 ms per loop
```

Below the “proofs” that the `__contain__` method wasn’t added to Python 2.x yet:

```python
print('Python', python_version())
range.__contains__
```

```python
Python 3.4.1

<slot wrapper '__contains__' of 'range' objects>
```

```python
print 'Python', python_version()
range.__contains__
```

```python
Python 2.7.7

---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)

<ipython-input-7-05327350dafb> in <module>()
      1 print 'Python', python_version()
----> 2 range.__contains__

AttributeError: 'builtin_function_or_method' object has no attribute '__contains__'
```

```python
print 'Python', python_version()
xrange.__contains__
```

```python
Python 2.7.7

---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)

<ipython-input-8-7d1a71bfee8e> in <module>()
      1 print 'Python', python_version()
----> 2 xrange.__contains__

AttributeError: type object 'xrange' has no attribute '__contains__'
```

#### Note about the speed differences in Python 2 and 3

Some people pointed out the speed difference between Python 3’s `range()` and Python2’s `xrange()`. Since they are implemented the same way one would expect the same speed. However the difference here just comes from the fact that Python 3 generally tends to run slower than Python 2.

```python
def test_while():
    i = 0
    while i < 20000:
        i += 1
    return
```

```python
print('Python', python_version())
%timeit test_while()
```

```python
Python 3.4.1
100 loops, best of 3: 2.68 ms per loop
```

```python
print 'Python', python_version()
%timeit test_while()
```

```python
Python 2.7.6
1000 loops, best of 3: 1.72 ms per loop
```

## Raising exceptions

Where Python 2 accepts both notations, the ‘old’ and the ‘new’ syntax, Python 3 chokes (and raises a `SyntaxError` in turn) if we don’t enclose the exception argument in parentheses:

### Python 2

```python
print 'Python', python_version()
```

```python
Python 2.7.6
```

```python
raise IOError, "file error"
```

```python
---------------------------------------------------------------------------
IOError                                   Traceback (most recent call last)

<ipython-input-8-25f049caebb0> in <module>()
----> 1 raise IOError, "file error"

IOError: file error
```

```python
raise IOError("file error")
```

```python
---------------------------------------------------------------------------
IOError                                   Traceback (most recent call last)

<ipython-input-9-6f1c43f525b2> in <module>()
----> 1 raise IOError("file error")

IOError: file error
```

### Python 3

```python
print('Python', python_version())
```

```python
Python 3.4.1
```

```python
raise IOError, "file error"
```

```python
  File "<ipython-input-10-25f049caebb0>", line 1
    raise IOError, "file error"
                 ^
SyntaxError: invalid syntax
```

The proper way to raise an exception in Python 3:

```python
print('Python', python_version())
raise IOError("file error")
```

```python
Python 3.4.1

---------------------------------------------------------------------------
OSError                                   Traceback (most recent call last)

<ipython-input-11-c350544d15da> in <module>()
      1 print('Python', python_version())
----> 2 raise IOError("file error")

OSError: file error
```

## Handling exceptions

Also the handling of exceptions has slightly changed in Python 3. In Python 3 we have to use the “`as`” keyword now

### Python 2

```python
print 'Python', python_version()
try:
    let_us_cause_a_NameError
except NameError, err:
    print err, '--> our error message'
```

```python
Python 2.7.6
name 'let_us_cause_a_NameError' is not defined --> our error message
```

### Python 3

```python
print('Python', python_version())
try:
    let_us_cause_a_NameError
except NameError as err:
    print(err, '--> our error message')
```

```python
Python 3.4.1
name 'let_us_cause_a_NameError' is not defined --> our error message
```

## The next() function and .next() method

Since `next()` (`.next()`) is such a commonly used function (method), this is another syntax change (or rather change in implementation) that is worth mentioning: where you can use both the function and method syntax in Python 2.7.5, the `next()` function is all that remains in Python 3 (calling the `.next()` method raises an `AttributeError`).

### Python 2

```python
print 'Python', python_version()

my_generator = (letter for letter in 'abcdefg')

next(my_generator)
my_generator.next()
```

```python
Python 2.7.6

'b'
```

### Python 3

```python
print('Python', python_version())

my_generator = (letter for letter in 'abcdefg')

next(my_generator)
```

```python
Python 3.4.1

'a'
```

```python
my_generator.next()
```

```python
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)

<ipython-input-14-125f388bb61b> in <module>()
----> 1 my_generator.next()

AttributeError: 'generator' object has no attribute 'next'
```

## For-loop variables and the global namespace leak

Good news is: In Python 3.x for-loop variables don’t leak into the global namespace anymore!

This goes back to a change that was made in Python 3.x and is described in [What’s New In Python 3.0](https://docs.python.org/3/whatsnew/3.0.html) as follows:

“List comprehensions no longer support the syntactic form `[... for var in item1, item2, ...]`. Use `[... for var in (item1, item2, ...)]` instead. Also note that list comprehensions have different semantics: they are closer to syntactic sugar for a generator expression inside a `list()` constructor, and in particular the loop control variables are no longer leaked into the surrounding scope.”

### Python 2

```python
print 'Python', python_version()

i = 1
print 'before: i =', i

print 'comprehension: ', [i for i in range(5)]

print 'after: i =', i
```

```python
Python 2.7.6
before: i = 1
comprehension:  [0, 1, 2, 3, 4]
after: i = 4
```

### Python 3

```python
print('Python', python_version())

i = 1
print('before: i =', i)

print('comprehension:', [i for i in range(5)])

print('after: i =', i)
```

```python
Python 3.4.1
before: i = 1
comprehension: [0, 1, 2, 3, 4]
after: i = 1
```

## Comparing unorderable types

Another nice change in Python 3 is that a `TypeError` is raised as warning if we try to compare unorderable types.

### Python 2

```python
print 'Python', python_version()
print "[1, 2] > 'foo' = ", [1, 2] > 'foo'
print "(1, 2) > 'foo' = ", (1, 2) > 'foo'
print "[1, 2] > (1, 2) = ", [1, 2] > (1, 2)
```

```python
Python 2.7.6
[1, 2] > 'foo' =  False
(1, 2) > 'foo' =  True
[1, 2] > (1, 2) =  False
```

### Python 3

```python
print('Python', python_version())
print("[1, 2] > 'foo' = ", [1, 2] > 'foo')
print("(1, 2) > 'foo' = ", (1, 2) > 'foo')
print("[1, 2] > (1, 2) = ", [1, 2] > (1, 2))
```

```python
Python 3.4.1

---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)

<ipython-input-16-a9031729f4a0> in <module>()
      1 print('Python', python_version())
----> 2 print("[1, 2] > 'foo' = ", [1, 2] > 'foo')
      3 print("(1, 2) > 'foo' = ", (1, 2) > 'foo')
      4 print("[1, 2] > (1, 2) = ", [1, 2] > (1, 2))

TypeError: unorderable types: list() > str()
```

## Parsing user inputs via input()

Fortunately, the `input()` function was fixed in Python 3 so that it always stores the user inputs as `str` objects. In order to avoid the dangerous behavior in Python 2 to read in other types than `strings`, we have to use `raw_input()` instead.

### Python 2

```python
Python 2.7.6
[GCC 4.0.1 (Apple Inc. build 5493)] on darwin
Type "help", "copyright", "credits" or "license" for more information.

>>> my_input = input('enter a number: ')

enter a number: 123

>>> type(my_input)
<type 'int'>

>>> my_input = raw_input('enter a number: ')

enter a number: 123

>>> type(my_input)
<type 'str'>
```

### Python 3

```python
Python 3.4.1
[GCC 4.2.1 (Apple Inc. build 5577)] on darwin
Type "help", "copyright", "credits" or "license" for more information.

>>> my_input = input('enter a number: ')

enter a number: 123

>>> type(my_input)
<class 'str'>
```

## Returning iterable objects instead of lists

As we have already seen in the [`xrange`](#xrange) section, some functions and methods return iterable objects in Python 3 now - instead of lists in Python 2.

Since we usually iterate over those only once anyway, I think this change makes a lot of sense to save memory. However, it is also possible - in contrast to generators - to iterate over those multiple times if needed, it is only not so efficient.

And for those cases where we really need the `list`-objects, we can simply convert the iterable object into a `list` via the `list()` function.

### Python 2

```python
print 'Python', python_version()

print range(3)
print type(range(3))
```

```python
Python 2.7.6
[0, 1, 2]
<type 'list'>
```

### Python 3

```python
print('Python', python_version())

print(range(3))
print(type(range(3)))
print(list(range(3)))
```

```python
Python 3.4.1
range(0, 3)
<class 'range'>
[0, 1, 2]
```

**Some more commonly used functions and methods that don’t return lists anymore in Python 3:**

- `zip()`
- `map()`
- `filter()`
- dictionary’s `.keys()` method
- dictionary’s `.values()` method
- dictionary’s `.items()` method

## Banker’s Rounding

Python 3 adopted the now standard way of rounding decimals when it results in a tie (.5) at the last significant digits. Now, in Python 3, decimals are rounded to the nearest even number. Although it’s an inconvenience for code portability, it’s supposedly a better way of rounding compared to rounding up as it avoids the bias towards large numbers. For more information, see the excellent Wikipedia articles and paragraphs:

- <https://en.wikipedia.org/wiki/Rounding#Round_half_to_even>
- <https://en.wikipedia.org/wiki/IEEE_floating_point#Roundings_to_nearest>

### Python 2

```python
print 'Python', python_version()
```

```python
Python 2.7.12
```

```python
round(15.5)
```

```python
16.0
```

```python
round(16.5)
```

```python
17.0
```

### Python 3

```python
print('Python', python_version())
```

```python
Python 3.5.1
```

```python
round(15.5)
```

```python
16
```

```python
round(16.5)
```

```python
16
```

## More articles about Python 2 and Python 3

Here is a list of some good articles concerning Python 2 and 3 that I would recommend as a follow-up.

**// Porting to Python 3**

- [Should I use Python 2 or Python 3 for my development activity?](https://wiki.python.org/moin/Python2orPython3)
- [What’s New In Python 3.0](https://docs.python.org/3.0/whatsnew/3.0.html)
- [Porting to Python 3](http://python3porting.com/differences.html)
- [Porting Python 2 Code to Python 3](https://docs.python.org/3/howto/pyporting.html)
- [How keep Python 3 moving forward](http://nothingbutsnark.svbtle.com/my-view-on-the-current-state-of-python-3)

**// Pro and anti Python 3**

- [10 awesome features of Python that you can’t use because you refuse to upgrade to Python 3](http://asmeurer.github.io/python3-presentation/slides.html#1)
- [Everything you did not want to know about Unicode in Python 3](http://lucumr.pocoo.org/2014/5/12/everything-about-unicode/)
- [Python 3 is killing Python](https://medium.com/@deliciousrobots/5d2ad703365d/)
- [Python 3 can revive Python](https://medium.com/p/2a7af4788b10)
- [Python 3 is fine](https://web.archive.org/web/20140530010014/http://sealedabstract.com:80/rants/python-3-is-fine/)
