---
title: "Diving deep into Python"
source: https://sebastianraschka.com/Articles/2014_deep_python.html
crawled: 2026-09-06
---

# Diving deep into Python

## Sections

### The C3 class resolution algorithm for multiple class inheritance

If we are dealing with multiple inheritance, according to the newer C3 class resolution algorithm, the following applies:  
Assuming that child class C inherits from two parent classes A and B, “class A should be checked before class B”.

If you want to learn more, please read the [original blog](http://python-history.blogspot.ru/2010/06/method-resolution-order.html) post by Guido van Rossum.

(Original source: <http://gistroll.com/rolls/21/horizontal_assessments/new>)

```python
class A(object):
    def foo(self):
        print("class A")

class B(object):
    def foo(self):
        print("class B")

class C(A, B):
    pass

C().foo()
```

```python
class A
```

So what actually happened above was that class `C` looked in the scope of the parent class `A` for the method `.foo()` first (and found it)!

I received an email containing a suggestion which uses a more nested example to illustrate Guido van Rossum’s point a little bit better:

```python
class A(object):
   def foo(self):
      print("class A")

class B(A):
   pass

class C(A):
   def foo(self):
      print("class C")

class D(B,C):
   pass

D().foo()
```

```python
class C
```

Here, class `D` searches in `B` first, which in turn inherits from `A` (note that class `C` also inherits from `A`, but has its own `.foo()` method) so that we come up with the search order: `D, B, C, A`.

### Assignment operators and lists - simple-add vs. add-AND operators

Python `list`s are mutable objects as we all know. So, if we are using the `+=` operator on `list`s, we extend the `list` by directly modifying the object.

However, if we use the assignment via `my_list = my_list + ...`, we create a new list object, which can be demonstrated by the following code:

```python
a_list = []
print('ID:', id(a_list))

a_list += [1]
print('ID (+=):', id(a_list))

a_list = a_list + [2]
print('ID (list = list + ...):', id(a_list))
```

```python
ID: 4366496544
ID (+=): 4366496544
ID (list = list + ...): 4366495472
```

Just for reference, the `.append()` and `.extends()` methods are modifying the `list` object in place, just as expected.

```python
a_list = []
print(a_list, '\nID (initial):',id(a_list), '\n')

a_list.append(1)
print(a_list, '\nID (append):',id(a_list), '\n')

a_list.extend([2])
print(a_list, '\nID (extend):',id(a_list))
```

```python
[]
ID (initial): 140704077653128

[1]
ID (append): 140704077653128

[1, 2]
ID (extend): 140704077653128
```

### `True` and `False` in the datetime module

“It often comes as a big surprise for programmers to find (sometimes by way of a hard-to-reproduce bug) that, unlike any other time value, midnight (i.e. `datetime.time(0,0,0)`) is False. A long discussion on the python-ideas mailing list shows that, while surprising, that behavior is desirable—at least in some quarters.”

(Original source: <http://lwn.net/SubscriberLink/590299/bf73fe823974acea/>)

```python
import datetime

print('"datetime.time(0,0,0)" (Midnight) ->', bool(datetime.time(0,0,0)))

print('"datetime.time(1,0,0)" (1 am) ->', bool(datetime.time(1,0,0)))
```

```python
"datetime.time(0,0,0)" (Midnight) -> False
"datetime.time(1,0,0)" (1 am) -> True
```

### Python reuses objects for small integers - use “==” for equality, “is” for identity

This oddity occurs, because Python keeps an array of small integer objects (i.e., integers between -5 and 256, [see the doc](https://docs.python.org/2/c-api/int.html#PyInt_FromLong)).

```python
a = 1
b = 1
print('a is b', bool(a is b))
True

c = 999
d = 999
print('c is d', bool(c is d))
```

```python
a is b True
c is d False
```

(*I received a comment that this is in fact a CPython artefact and* **must not necessarily be true** *in all implementations of Python!*)

So the take home message is: always use “==” for equality, “is” for identity!

Here is a [nice article](http://python.net/%7Egoodger/projects/pycon/2007/idiomatic/handout.html#other-languages-have-variables) explaining it by comparing “boxes” (C language) with “name tags” (Python).

This example demonstrates that this applies indeed for integers in the range in -5 to 256:

```python
print('256 is 257-1', 256 is 257-1)
print('257 is 258-1', 257 is 258 - 1)
print('-5 is -6+1', -5 is -6+1)
print('-7 is -6-1', -7 is -6-1)
```

```python
256 is 257-1 True
257 is 258-1 False
-5 is -6+1 True
-7 is -6-1 False
```

#### And to illustrate the test for equality (`==`) vs. identity (`is`):

```python
a = 'hello world!'
b = 'hello world!'
print('a is b,', a is b)
print('a == b,', a == b)
```

```python
a is b, False
a == b, True
```

We would think that identity would always imply equality, but this is not always true, as we can see in the next example:

```python
a = float('nan')
print('a is a,', a is a)
print('a == a,', a == a)
```

```python
a is a, True
a == a, False
```

### Shallow vs. deep copies if list contains other structures and objects

**Shallow copy**:  
If we use the assignment operator to assign one list to another list, we just create a new name reference to the original list. If we want to create a new list object, we have to make a copy of the original list. This can be done via `a_list[:]` or `a_list.copy()`.

```python
list1 = [1,2]
list2 = list1        # reference
list3 = list1[:]     # shallow copy
list4 = list1.copy() # shallow copy

print('IDs:\nlist1: {}\nlist2: {}\nlist3: {}\nlist4: {}\n'
      .format(id(list1), id(list2), id(list3), id(list4)))

list2[0] = 3
print('list1:', list1)

list3[0] = 4
list4[1] = 4
print('list1:', list1)
```

```python
IDs:
list1: 4346366472
list2: 4346366472
list3: 4346366408
list4: 4346366536

list1: [3, 2]
list1: [3, 2]
```

**Deep copy**  
As we have seen above, a shallow copy works fine if we want to create a new list with contents of the original list which we want to modify independently.

However, if we are dealing with compound objects (e.g., lists that contain other lists, [read here](https://docs.python.org/2/library/copy.html) for more information) it becomes a little trickier.

In the case of compound objects, a shallow copy would create a new compound object, but it would just insert the references to the contained objects into the new compound object. In contrast, a deep copy would go “deeper” and create also new objects   
for the objects found in the original compound object.
If you follow the code, the concept should become more clear:

```python
from copy import deepcopy

list1 = [[1],[2]]
list2 = list1.copy()    # shallow copy
list3 = deepcopy(list1) # deep copy

print('IDs:\nlist1: {}\nlist2: {}\nlist3: {}\n'
      .format(id(list1), id(list2), id(list3)))

list2[0][0] = 3
print('list1:', list1)

list3[0][0] = 5
print('list1:', list1)
```

```python
IDs:
list1: 4377956296
list2: 4377961752
list3: 4377954928

list1: [[3], [2]]
list1: [[3], [2]]
```

### Picking `True` values from logical `and`s and `or`s

**Logical `or`:**

`a or b == a if a else b`

- If both values in `or` expressions are `True`, Python will select the first value (e.g., select `"a"` in `"a" or "b"`), and the second one in `and` expressions.  
  This is also called **short-circuiting** - we already know that the logical `or` must be `True` if the first value is `True` and therefore can omit the evaluation of the second value.

**Logical `and`:**

`a and b == b if a else a`

- If both values in `and` expressions are `True`, Python will select the second value, since for a logical `and`, both values must be true.

```python
result = (2 or 3) * (5 and 7)
print('2 * 7 =', result)
```

```python
2 * 7 = 14
```

### Don’t use mutable objects as default arguments for functions!

Don’t use mutable objects (e.g., dictionaries, lists, sets, etc.) as default arguments for functions! You might expect that a new list is created every time when we call the function without providing an argument for the default parameter, but this is not the case: **Python will create the mutable object (default parameter) the first time the function is defined - not when it is called**, see the following code:

(Original source: <http://docs.python-guide.org/en/latest/writing/gotchas/>

```python
def append_to_list(value, def_list=[]):
    def_list.append(value)
    return def_list

my_list = append_to_list(1)
print(my_list)

my_other_list = append_to_list(2)
print(my_other_list)
```

```python
[1]
[1, 2]
```

Another good example showing that demonstrates that default arguments are created when the function is created (**and not when it is called!**):

```python
import time
def report_arg(my_default=time.time()):
    print(my_default)

report_arg()

time.sleep(5)

report_arg()
```

```python
1397764090.456688
1397764090.456688
```

### Be aware of the consuming generator

Be aware of what is happening when combining “`in`” checks with generators, since they won’t evaluate from the beginning once a position is “consumed”.

```python
gen = (i for i in range(5))
print('2 in gen,', 2 in gen)
print('3 in gen,', 3 in gen)
print('1 in gen,', 1 in gen)
```

```python
2 in gen, True
3 in gen, True
1 in gen, False
```

Although this defeats the purpose of a generator (in most cases), we can convert a generator into a list to circumvent the problem.

```python
gen = (i for i in range(5))
a_list = list(gen)
print('2 in l,', 2 in a_list)
print('3 in l,', 3 in a_list)
print('1 in l,', 1 in a_list)
```

```python
2 in l, True
3 in l, True
1 in l, True
```

### `bool` is a subclass of `int`

Chicken or egg? In the history of Python (Python 2.2 to be specific) truth values were implemented via 1 and 0 (similar to the old C). In order to avoid syntax errors in old (but perfectly working) Python code, `bool` was added as a subclass of `int` in Python 2.3.

Original source: <http://www.peterbe.com/plog/bool-is-int>

```python
print('isinstance(True, int):', isinstance(True, int))
print('True + True:', True + True)
print('3*True + True:', 3*True + True)
print('3*True - False:', 3*True - False)
```

```python
isinstance(True, int): True
True + True: 2
3*True + True: 4
3*True - False: 3
```

### About lambda-in-closures-and-a-loop pitfall

Remember the section about the [“consuming generators”](#be-aware-of-the-consuming-generator)? This example is somewhat related, but the result might still come unexpected.

(Original source: <http://openhome.cc/eGossip/Blog/UnderstandingLambdaClosure3.html>)

In the first example below, we call a `lambda` function in a list comprehension, and the value `i` will be dereferenced every time we call `lambda`. Since the list comprehension has already been constructed and evaluated when we for-loop through the list, the closure-variable will be set to the last value 4.

```python
my_list = [lambda: i for i in range(5)]
for l in my_list:
    print(l())
```

```python
4
4
4
4
4
```

However, by using a generator expression, we can make use of its stepwise evaluation (note that the returned variable still stems from the same closure, but the value changes as we iterate over the generator).

```python
my_gen = (lambda: n for n in range(5))
for l in my_gen:
    print(l())
```

```python
0
1
2
3
4
```

And if you are really keen on using lists, there is a nifty trick that circumvents this problem as a reader nicely pointed out in the comments: We can simply pass the loop variable `i` as a default argument to the lambdas.

```python
my_list = [lambda x=i: x for i in range(5)]
for l in my_list:
    print(l())
```

```python
0
1
2
3
4
```

### Python’s LEGB scope resolution and the keywords `global` and `nonlocal`

There is nothing particularly surprising about Python’s LEGB scope resolution (Local -> Enclosed -> Global -> Built-in), but it is still useful to take a look at some examples!

#### `global` vs. `local`

According to the LEGB rule, Python will first look for a variable in the local scope. So if we set the variable `x = 1` `local`ly in the function’s scope, it won’t have an effect on the `global` `x`.

```python
x = 0
def in_func():
    x = 1
    print('in_func:', x)

in_func()
print('global:', x)
```

```python
in_func: 1
global: 0
```

If we want to modify the `global` x via a function, we can simply use the `global` keyword to import the variable into the function’s scope:

```python
x = 0
def in_func():
    global x
    x = 1
    print('in_func:', x)

in_func()
print('global:', x)
```

```python
in_func: 1
global: 1
```

#### `local` vs. `enclosed`

Now, let us take a look at `local` vs. `enclosed`. Here, we set the variable `x = 1` in the `outer` function and set `x = 1` in the enclosed function `inner`. Since `inner` looks in the local scope first, it won’t modify `outer`’s `x`.

```python
def outer():
       x = 1
       print('outer before:', x)
       def inner():
           x = 2
           print("inner:", x)
       inner()
       print("outer after:", x)
outer()
```

```python
outer before: 1
inner: 2
outer after: 1
```

Here is where the `nonlocal` keyword comes in handy - it allows us to modify the `x` variable in the `enclosed` scope:

```python
def outer():
       x = 1
       print('outer before:', x)
       def inner():
           nonlocal x
           x = 2
           print("inner:", x)
       inner()
       print("outer after:", x)
outer()
```

```python
outer before: 1
inner: 2
outer after: 2
```

### When mutable contents of immutable tuples aren’t so mutable

As we all know, tuples are immutable objects in Python, right!? But what happens if they contain mutable objects?

First, let us have a look at the expected behavior: a `TypeError` is raised if we try to modify immutable types in a tuple:

```python
tup = (1,)
tup[0] += 1
```

```python
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)

<ipython-input-41-c3bec6c3fe6f> in <module>()
      1 tup = (1,)
----> 2 tup[0] += 1

TypeError: 'tuple' object does not support item assignment
```

#### But what if we put a mutable object into the immutable tuple? Well, modification works, but we **also** get a `TypeError` at the same time.

```python
tup = ([],)
print('tup before: ', tup)
tup[0] += [1]
```

```python
tup before:  ([],)

---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)

<ipython-input-42-aebe9a31dbeb> in <module>()
      1 tup = ([],)
      2 print('tup before: ', tup)
----> 3 tup[0] += [1]

TypeError: 'tuple' object does not support item assignment
```

```python
print('tup after: ', tup)
```

```python
tup after:  ([1],)
```

However, **there are ways** to modify the mutable contents of the tuple without raising the `TypeError`, the solution is the `.extend()` method, or alternatively `.append()` (for lists):

```python
tup = ([],)
print('tup before: ', tup)
tup[0].extend([1])
print('tup after: ', tup)
```

```python
tup before:  ([],)
tup after:  ([1],)
```

```python
tup = ([],)
print('tup before: ', tup)
tup[0].append(1)
print('tup after: ', tup)
```

```python
tup before:  ([],)
tup after:  ([1],)
```

#### Explanation

**A. Jesse Jiryu Davis** has a nice explanation for this phenomenon (Original source: <http://emptysqua.re/blog/python-increment-is-weird-part-ii/>)

If we try to extend the list via `+=` *“then the statement executes `STORE_SUBSCR`, which calls the C function `PyObject_SetItem`, which checks if the object supports item assignment. In our case the object is a tuple, so `PyObject_SetItem` throws the `TypeError`. Mystery solved.”*

##### One more note about the `immutable` status of tuples. Tuples are famous for being immutable. However, how comes that this code works?

```python
my_tup = (1,)
my_tup += (4,)
my_tup = my_tup + (5,)
print(my_tup)
```

```python
(1, 4, 5)
```

What happens “behind” the curtains is that the tuple is not modified, but a new object is generated every time, which will inherit the old “name tag”:

```python
my_tup = (1,)
print(id(my_tup))
my_tup += (4,)
print(id(my_tup))
my_tup = my_tup + (5,)
print(id(my_tup))
```

```python
4337381840
4357415496
4357289952
```

### List comprehensions are fast, but generators are faster!?

“List comprehensions are fast, but generators are faster!?” - No, not really (or significantly, see the benchmarks below). So what’s the reason to prefer one over the other?

- use lists if you want to use the plethora of list methods
- use generators when you are dealing with huge collections to avoid memory issues

```python
import timeit

def plainlist(n=100000):
    my_list = []
    for i in range(n):
        if i % 5 == 0:
            my_list.append(i)
    return my_list

def listcompr(n=100000):
    my_list = [i for i in range(n) if i % 5 == 0]
    return my_list

def generator(n=100000):
    my_gen = (i for i in range(n) if i % 5 == 0)
    return my_gen

def generator_yield(n=100000):
    for i in range(n):
        if i % 5 == 0:
            yield i
```

#### To be fair to the list, let us exhaust the generators:

```python
def test_plainlist(plain_list):
    for i in plain_list():
        pass

def test_listcompr(listcompr):
    for i in listcompr():
        pass

def test_generator(generator):
    for i in generator():
        pass

def test_generator_yield(generator_yield):
    for i in generator_yield():
        pass

print('plain_list:     ', end = '')
%timeit test_plainlist(plainlist)
print('\nlistcompr:     ', end = '')
%timeit test_listcompr(listcompr)
print('\ngenerator:     ', end = '')
%timeit test_generator(generator)
print('\ngenerator_yield:     ', end = '')
%timeit test_generator_yield(generator_yield)
```

```python
plain_list:     10 loops, best of 3: 22.4 ms per loop

listcompr:     10 loops, best of 3: 20.8 ms per loop

generator:     10 loops, best of 3: 22 ms per loop

generator_yield:     10 loops, best of 3: 21.9 ms per loop
```

### Public vs. private class methods and name mangling

Who has not stumbled across this quote “we are all consenting adults here” in the Python community, yet? Unlike in other languages like C++ (sorry, there are many more, but that’s one I am most familiar with), we can’t really protect class methods from being used outside the class (i.e., by the API user).  
All we can do is indicate methods as private to make clear that they are not to be used outside the class, but it is really up to the class user, since “we are all consenting adults here”!  
So, when we want to mark a class method as private, we can put a single underscore in front of it.  
If we additionally want to avoid name clashes with other classes that might use the same method names, we can prefix the name with a double-underscore to invoke the name mangling.

This doesn’t prevent the class users to access this class member though, but they have to know the trick and also know that it is at their own risk…

Let the following example illustrate what I mean:

```python
class my_class():
    def public_method(self):
        print('Hello public world!')
    def __private_method(self):
        print('Hello private world!')
    def call_private_method_in_class(self):
        self.__private_method()

my_instance = my_class()

my_instance.public_method()
my_instance._my_class__private_method()
my_instance.call_private_method_in_class()
```

```python
Hello public world!
Hello private world!
Hello private world!
```

### The consequences of modifying a list when looping through it

It can be really dangerous to modify a list when iterating through it - this is a very common pitfall that can cause unintended behavior!  
Look at the following examples, and for a fun exercise: try to figure out what is going on before you skip to the solution!

```python
a = [1, 2, 3, 4, 5]
for i in a:
    if not i % 2:
        a.remove(i)
print(a)
```

```python
[1, 3, 5]
```

```python
b = [2, 4, 5, 6]
for i in b:
     if not i % 2:
         b.remove(i)
print(b)
```

```python
[4, 5]
```

**The solution** is that we are iterating through the list index by index, and if we remove one of the items in-between, we inevitably mess around with the indexing. Look at the following example and it will become clear:

```python
b = [2, 4, 5, 6]
for index, item in enumerate(b):
    print(index, item)
    if not item % 2:
        b.remove(item)
print(b)
```

```python
0 2
1 5
2 6
[4, 5]
```

### Dynamic binding and typos in variable names

Be careful, dynamic binding is convenient, but can also quickly become dangerous!

```python
print('first list:')
for i in range(3):
    print(i)

print('\nsecond list:')
for j in range(3):
    print(i) # I (intentionally) made typo here!
```

```python
first list:
0
1
2

second list:
2
2
2
```

### List slicing using indexes that are “out of range”

As we have all encountered it 1 (x10000) time(s) in our life, the infamous `IndexError`:

```python
my_list = [1, 2, 3, 4, 5]
print(my_list[5])
```

```python
---------------------------------------------------------------------------
IndexError                                Traceback (most recent call last)

<ipython-input-15-eb273dc36fdc> in <module>()
      1 my_list = [1, 2, 3, 4, 5]
----> 2 print(my_list[5])

IndexError: list index out of range
```

But suprisingly, it is not raised when we are doing list slicing, which can be a real pain when debugging:

```python
my_list = [1, 2, 3, 4, 5]
print(my_list[5:])
```

```python
[]
```

### Reusing global variable names and `UnboundLocalErrors`

Usually, it is no problem to access global variables in the local scope of a function:

```python
def my_func():
    print(var)

var = 'global'
my_func()
```

```python
global
```

And is also no problem to use the same variable name in the local scope without affecting the local counterpart:

```python
def my_func():
    var = 'locally changed'

var = 'global'
my_func()
print(var)
```

```python
global
```

But we have to be careful if we use a variable name that occurs in the global scope, and we want to access it in the local function scope if we want to reuse this name:

```python
def my_func():
    print(var) # want to access global variable
    var = 'locally changed' # but Python thinks we forgot to define the local variable!

var = 'global'
my_func()
```

```python
---------------------------------------------------------------------------
UnboundLocalError                         Traceback (most recent call last)

<ipython-input-40-3afd870b7c35> in <module>()
      4
      5 var = 'global'
----> 6 my_func()

<ipython-input-40-3afd870b7c35> in my_func()
      1 def my_func():
----> 2     print(var) # want to access global variable
      3     var = 'locally changed'
      4
      5 var = 'global'

UnboundLocalError: local variable 'var' referenced before assignment
```

In this case, we have to use the `global` keyword!

```python
def my_func():
    global var
    print(var) # want to access global variable
    var = 'locally changed' # changes the gobal variable

var = 'global'

my_func()
print(var)
```

```python
global
locally changed
```

### Creating copies of mutable objects

Let’s assume a scenario where we want to duplicate sub`list`s of values stored in another list. If we want to create an independent sub`list` object, using the arithmetic multiplication operator could lead to rather unexpected (or undesired) results:

```python
my_list1 = [[1, 2, 3]] * 2

print('initially ---> ', my_list1)

# modify the 1st element of the 2nd sublist
my_list1[1][0] = 'a'
print("after my_list1[1][0] = 'a' ---> ", my_list1)
```

```python
initially --->  [[1, 2, 3], [1, 2, 3]]
after my_list1[1][0] = 'a' --->  [['a', 2, 3], ['a', 2, 3]]
```

In this case, we should better create “new” objects:

```python
my_list2 = [[1, 2, 3] for i in range(2)]

print('initially:  ---> ', my_list2)

# modify the 1st element of the 2nd sublist
my_list2[1][0] = 'a'
print("after my_list2[1][0] = 'a':  ---> ", my_list2)
```

```python
initially:  --->  [[1, 2, 3], [1, 2, 3]]
after my_list2[1][0] = 'a':  --->  [[1, 2, 3], ['a', 2, 3]]
```

And here is the proof:

```python
for a,b in zip(my_list1, my_list2):
    print('id my_list1: {}, id my_list2: {}'.format(id(a), id(b)))
```

```python
id my_list1: 4350764680, id my_list2: 4350766472
id my_list1: 4350764680, id my_list2: 4350766664
```

### Key differences between Python 2 and 3

There are some good articles already that are summarizing the differences between Python 2 and 3, e.g.,

- <https://wiki.python.org/moin/Python2orPython3>
- <https://docs.python.org/3.0/whatsnew/3.0.html>
- <http://python3porting.com/differences.html>
- <https://docs.python.org/3/howto/pyporting.html>  
  etc.

But it might be still worthwhile, especially for Python newcomers, to take a look at some of those!
(Note: the the code was executed in Python 3.4.0 and Python 2.7.5 and copied from interactive shell sessions.)

#### Overview - Key differences between Python 2 and 3

- [Unicode](#unicode)
- [The print statement](#print)
- [Integer division](#integer_div)
- [xrange()](#xrange)
- [Raising exceptions](#raising_exceptions)
- [Handling exceptions](#handling_exceptions)
- [next() function and .next() method](#next_next)
- [Loop variables and leaking into the global scope](#loop_leak)
- [Comparing unorderable types](#compare_unorder)

#### Unicode…

[[back to Python 2.x vs 3.x overview](#py23_overview)]

##### - Python 2:

We have ASCII `str()` types, separate `unicode()`, but no `byte` type

##### - Python 3:

Now, we finally have Unicode (utf-8) `str`ings, and 2 byte classes: `byte` and `bytearray`s

```python
#############
# Python 2
#############

>>> type(unicode('is like a python3 str()'))
<type 'unicode'>

>>> type(b'byte type does not exist')
<type 'str'>

>>> 'they are really' + b' the same'
'they are really the same'

>>> type(bytearray(b'bytearray oddly does exist though'))
<type 'bytearray'>

#############
# Python 3
#############

>>> print('strings are now utf-8 \u03BCnico\u0394é!')
strings are now utf-8 μnicoΔé!

>>> type(b' and we have byte types for storing data')
<class 'bytes'>

>>> type(bytearray(b'but also bytearrays for those who prefer them over strings'))
<class 'bytearray'>

>>> 'string' + b'bytes for data'
Traceback (most recent call last):s
  File "<stdin>", line 1, in <module>
TypeError: Can't convert 'bytes' object to str implicitly
```

#### The print statement

Very trivial, but this change makes sense, Python 3 now only accepts `print`s with proper parentheses - just like the other function calls …

```python
# Python 2
>>> print 'Hello, World!'
Hello, World!
>>> print('Hello, World!')
Hello, World!

# Python 3
>>> print('Hello, World!')
Hello, World!
>>> print 'Hello, World!'
  File "<stdin>", line 1
    print 'Hello, World!'
                        ^
SyntaxError: invalid syntax
```

And if we want to print the output of 2 consecutive print functions on the same line, you would use a comma in Python 2, and a `end=""` in Python 3:

```python
# Python 2
>>> print "line 1", ; print 'same line'
line 1 same line

# Python 3
>>> print("line 1", end="") ; print (" same line")
line 1 same line
```

#### Integer division

This is a pretty dangerous thing if you are porting code, or executing Python 3 code in Python 2 since the change in integer-division behavior can often go unnoticed.  
So, I still tend to use a `float(3)/2` or `3/2.0` instead of a `3/2` in my Python 3 scripts to save the Python 2 guys some trouble … (PS: and vice versa, you can `from __future__ import division` in your Python 2 scripts).

```python
# Python 2
>>> 3 / 2
1
>>> 3 // 2
1
>>> 3 / 2.0
1.5
>>> 3 // 2.0
1.0

# Python 3
>>> 3 / 2
1.5
>>> 3 // 2
1
>>> 3 / 2.0
1.5
>>> 3 // 2.0
1.0
```

###`xrange()`

`xrange()` was pretty popular in Python 2.x if you wanted to create an iterable object. The behavior was quite similar to a generator (‘lazy evaluation’), but you could iterate over it infinitely. The advantage was that it was generally faster than `range()` (e.g., in a for-loop) - not if you had to iterate over the list multiple times, since the generation happens every time from scratch!  
In Python 3, the `range()` was implemented like the `xrange()` function so that a dedicated `xrange()` function does not exist anymore.

```python
# Python 2
> python -m timeit 'for i in range(1000000):' ' pass'
10 loops, best of 3: 66 msec per loop

    > python -m timeit 'for i in xrange(1000000):' ' pass'
10 loops, best of 3: 27.8 msec per loop

# Python 3
> python3 -m timeit 'for i in range(1000000):' ' pass'
10 loops, best of 3: 51.1 msec per loop

> python3 -m timeit 'for i in xrange(1000000):' ' pass'
Traceback (most recent call last):
  File "/Library/Frameworks/Python.framework/Versions/3.4/lib/python3.4/timeit.py", line 292, in main
    x = t.timeit(number)
  File "/Library/Frameworks/Python.framework/Versions/3.4/lib/python3.4/timeit.py", line 178, in timeit
    timing = self.inner(it, self.timer)
  File "<timeit-src>", line 6, in inner
    for i in xrange(1000000):
NameError: name 'xrange' is not defined
```

#### Raising exceptions

Where Python 2 accepts both notations, the ‘old’ and the ‘new’ way, Python 3 chokes (and raises a `SyntaxError` in turn) if we don’t enclose the exception argument in parentheses:

```python
# Python 2
>>> raise IOError, "file error"
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IOError: file error
>>> raise IOError("file error")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IOError: file error

# Python 3    
>>> raise IOError, "file error"
  File "<stdin>", line 1
    raise IOError, "file error"
                 ^
SyntaxError: invalid syntax
>>> raise IOError("file error")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
OSError: file error
```

#### Handling exceptions

Also the handling of exceptions has slightly changed in Python 3. Now, we have to use the `as` keyword!

```python
# Python 2
>>> try:
...     blabla
... except NameError, err:
...     print err, '--> our error msg'
...
name 'blabla' is not defined --> our error msg

# Python 3
>>> try:
...     blabla
... except NameError as err:
...     print(err, '--> our error msg')
...
name 'blabla' is not defined --> our error msg
```

#### The `next()` function and `.next()` method

Where you can use both function and method in Python 2.7.5, the `next()` function is all that remains in Python 3!

```python
# Python 2
>>> my_generator = (letter for letter in 'abcdefg')
>>> my_generator.next()
'a'
>>> next(my_generator)
'b'

# Python 3
>>> my_generator = (letter for letter in 'abcdefg')
>>> next(my_generator)
'a'
>>> my_generator.next()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'generator' object has no attribute 'next'
```

#### In Python 3.x for-loop variables don’t leak into the global namespace anymore

This goes back to a change that was made in Python 3.x and is described in [What’s New In Python 3.0](https://docs.python.org/3/whatsnew/3.0.html) as follows:

“List comprehensions no longer support the syntactic form `[... for var in item1, item2, ...]`. Use `[... for var in (item1, item2, ...)]` instead. Also note that list comprehensions have different semantics: they are closer to syntactic sugar for a generator expression inside a `list()` constructor, and in particular the loop control variables are no longer leaked into the surrounding scope.”

```python
from platform import python_version
print('This code cell was executed in Python', python_version())

i = 1
print([i for i in range(5)])
print(i, '-> i in global')
```

```python
This code cell was executed in Python 3.3.5
[0, 1, 2, 3, 4]
1 -> i in global
```

```python
from platform import python_version
print 'This code cell was executed in Python', python_version()

i = 1
print [i for i in range(5)]
print i, '-> i in global'
```

```python
This code cell was executed in Python 2.7.6
[0, 1, 2, 3, 4]
4 -> i in global
```

##### Python 3.x prevents us from comparing unorderable types

```python
from platform import python_version
print 'This code cell was executed in Python', python_version()

print [1, 2] > 'foo'
print (1, 2) > 'foo'
print [1, 2] > (1, 2)
```

```python
This code cell was executed in Python 2.7.6
False
True
False
```

```python
from platform import python_version
print('This code cell was executed in Python', python_version())

print([1, 2] > 'foo')
print((1, 2) > 'foo')
print([1, 2] > (1, 2))
```

```python
This code cell was executed in Python 3.3.5

---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)

<ipython-input-3-1d774c677f73> in <module>()
      2 print('This code cell was executed in Python', python_version())
      3
----> 4 [1, 2] > 'foo'
      5 (1, 2) > 'foo'
      6 [1, 2] > (1, 2)

TypeError: unorderable types: list() > str()
```

### Function annotations - What are those `->`’s in my Python code?

Have you ever seen any Python code that used colons inside the parantheses of a function definition?

```python
def foo1(x: 'insert x here', y: 'insert x^2 here'):
    print('Hello, World')
    return
```

And what about the fancy arrow here?

```python
def foo2(x, y) -> 'Hi!':
    print('Hello, World')
    return
```

Q: Is this valid Python syntax?  
A: Yes!

Q: So, what happens if I *just call* the function?  
A: Nothing!

Here is the proof!

```python
foo1(1,2)
```

```python
Hello, World
```

```python
foo2(1,2)
```

```python
Hello, World
```

\*\*So, those are function annotations … \*\*

- the colon for the function parameters
- the arrow for the return value

You probably will never make use of them (or at least very rarely). Usually, we write good function documentations below the function as a docstring - or at least this is how I would do it (okay this case is a little bit extreme, I have to admit):

```python
def is_palindrome(a):
    """
    Case-and punctuation insensitive check if a string is a palindrom.

    Keyword arguments:
        a (str): The string to be checked if it is a palindrome.

    Returns `True` if input string is a palindrome, else False.

    """
    stripped_str = [l for l in my_str.lower() if l.isalpha()]
    return stripped_str == stripped_str[::-1]
```

However, function annotations can be useful to indicate that work is still in progress in some cases. But they are optional and I see them very very rarely.

As it is stated in [PEP3107](http://legacy.python.org/dev/peps/pep-3107/#fundamentals-of-function-annotations):

1. Function annotations, both for parameters and return values, are completely optional.
2. Function annotations are nothing more than a way of associating arbitrary Python expressions with various parts of a function at compile-time.

The nice thing about function annotations is their `__annotations__` attribute, which is a dictionary of all the parameters and/or the `return` value you annotated.

```python
foo1.__annotations__
```

```python
{'y': 'insert x^2 here', 'x': 'insert x here'}
```

```python
foo2.__annotations__
```

```python
{'return': 'Hi!'}
```

**When are they useful?**

Function annotations can be useful for a couple of things

- Documentation in general
- pre-condition testing
- [type checking](http://legacy.python.org/dev/peps/pep-0362/#annotation-checker)

…

### Abortive statements in `finally` blocks

Python’s `try-except-finally` blocks are very handy for catching and handling errors. The `finally` block is always executed whether an `exception` has been raised or not as illustrated in the following example.

```python
def try_finally1():
    try:
        print('in try:')
        print('do some stuff')
        float('abc')
    except ValueError:
        print('an error occurred')
    else:
        print('no error occurred')
    finally:
        print('always execute finally')

try_finally1()
```

```python
in try:
do some stuff
an error occurred
always execute finally
```

But can you also guess what will be printed in the next code cell?

```python
def try_finally2():
    try:
        print("do some stuff in try block")
        return "return from try block"
    finally:
        print("do some stuff in finally block")
        return "always execute finally"

print(try_finally2())
```

```python
do some stuff in try block
do some stuff in finally block
always execute finally
```

Here, the abortive `return` statement in the `finally` block simply overrules the `return` in the `try` block, since **`finally` is guaranteed to always be executed.** So, be careful using abortive statements in `finally` blocks!

## Assigning types to variables as values

I am not yet sure in which context this can be useful, but it is a nice fun fact to know that we can assign types as values to variables.

```python
a_var = str
a_var(123)
```

```python
'123'
```

```python
from random import choice

a, b, c = float, int, str
for i in range(5):
    j = choice([a,b,c])(i)
    print(j, type(j))
```

```python
0 <class 'int'>
1 <class 'int'>
2.0 <class 'float'>
3 <class 'str'>
4 <class 'int'>
```

## Only the first clause of generators is evaluated immediately

The main reason why we love to use generators in certain cases (i.e., when we are dealing with large numbers of computations) is that it only computes the next value when it is needed, which is also known as “lazy” evaluation.
However, the first clause of an generator is already checked upon it’s creation, as the following example demonstrates:

```python
gen_fails = (i for i in 1/0)
```

```python
---------------------------------------------------------------------------
ZeroDivisionError                         Traceback (most recent call last)

<ipython-input-18-29312e1ece8d> in <module>()
----> 1 gen_fails = (i for i in 1/0)

ZeroDivisionError: division by zero
```

Certainly, this is a nice feature, since it notifies us about syntax erros immediately. However, this is (unfortunately) not the case if we have multiple cases in our generator.

```python
gen_succeeds = (i for i in range(5) for j in 1/0)
```

```python
print('But obviously fails when we iterate ...')
for i in gen_succeeds:
    print(i)
```

```python
---------------------------------------------------------------------------
ZeroDivisionError                         Traceback (most recent call last)

<ipython-input-20-8a83a1022971> in <module>()
      1 print('But obviously fails when we iterate ...')
----> 2 for i in gen_succeeds:
      3     print(i)

<ipython-input-19-c54c53f2218a> in <genexpr>(.0)
----> 1 gen_succeeds = (i for i in range(5) for j in 1/0)

ZeroDivisionError: division by zero

But obviously fails when we iterate ...
```

##Keyword argument unpacking syntax - `*args` and `**kwargs`

Python has a very convenient “keyword argument unpacking syntax” (often referred to as “splat”-operators). This is particularly useful, if we want to define a function that can take a arbitrary number of input arguments.

### Single-asterisk (\*args)

```python
def a_func(*args):
    print('type of args:', type(args))
    print('args contents:', args)
    print('1st argument:', args[0])

a_func(0, 1, 'a', 'b', 'c')
```

```python
type of args: <class 'tuple'>
args contents: (0, 1, 'a', 'b', 'c')
1st argument: 0
```

### Double-asterisk (\*\*kwargs)

```python
def b_func(**kwargs):
    print('type of kwargs:', type(kwargs))
    print('kwargs contents: ', kwargs)
    print('value of argument a:', kwargs['a'])

b_func(a=1, b=2, c=3, d=4)
```

```python
type of kwargs: <class 'dict'>
kwargs contents:  {'d': 4, 'a': 1, 'c': 3, 'b': 2}
value of argument a: 1
```

### (Partially) unpacking of iterables

Another useful application of the “unpacking”-operator is the unpacking of lists and other other iterables.

```python
val1, *vals = [1, 2, 3, 4, 5]
print('val1:', val1)
print('vals:', vals)
```

```python
val1: 1
vals: [2, 3, 4, 5]
```

### Metaclasses - What creates a new instance of a class?

Usually, it is the `__init__` method when we think of instanciating a new object from a class. However, it is the static method `__new__` (it is not a class method!) that creates and returns a new instance before `__init__()` is called.
More specifically, this is what is returned:  
`return super(<currentclass>, cls).__new__(subcls, *args, **kwargs)`

For more information about the `__new__` method, please see the [documentation](https://www.python.org/download/releases/2.2/descrintro/#__new__).

As a little experiment, let us screw with `__new__` so that it returns `None` and see if `__init__` will be executed:

```python
class a_class(object):
    def __new__(clss, *args, **kwargs):
        print('excecuted __new__')
        return None
    def __init__(self, an_arg):
        print('excecuted __init__')
        self.an_arg = an_arg

a_object = a_class(1)
print('Type of a_object:', type(a_object))
```

```python
excecuted __new__
Type of a_object: <class 'NoneType'>
```

As we can see in the code above, `__init__` requires the returned instance from `__new__` in order to called. So, here we just created a `NoneType` object.  
Let us override the `__new__`, now and let us confirm that `__init__` is called now to instantiate the new object”:

```python
class a_class(object):
    def __new__(cls, *args, **kwargs):
        print('excecuted __new__')
        inst = super(a_class, cls).__new__(cls)
        return inst
    def __init__(self, an_arg):
        print('excecuted __init__')
        self.an_arg = an_arg

a_object = a_class(1)
print('Type of a_object:', type(a_object))
print('a_object.an_arg: ', a_object.an_arg)
```

```python
excecuted __new__
excecuted __init__
Type of a_object: <class '__main__.a_class'>
a_object.an_arg:  1
```

```python
for i in range(5):
    if i == 1:
        print('in for')
else:
    print('in else')
print('after for-loop')
```

```python
in for
in else
after for-loop
```

```python
for i in range(5):
    if i == 1:
        break
else:
    print('in else')
print('after for-loop')
```

```python
after for-loop
```

### Else-clauses: “conditional else” and “completion else”

I would claim that the conditional “else” is every programmer’s daily bread and butter. However, there is a second flavor of “else”-clauses in Python, which I will call “completion else” (for reason that will become clear later).  
But first, let us take a look at our “traditional” conditional else that we all are familiar with.

#### Conditional else:

```python
# conditional else

a_list = [1,2]
if a_list[0] == 1:
    print('Hello, World!')
else:
    print('Bye, World!')
```

```python
Hello, World!
```

```python
# conditional else

a_list = [1,2]
if a_list[0] == 2:
    print('Hello, World!')
else:
    print('Bye, World!')
```

```python
Bye, World!
```

Why am I showing those simple examples? I think they are good to highlight some of the key points: It is **either** the code under the `if` clause that is executed, **or** the code under the `else` block, but not both.  
If the condition of the `if` clause evaluates to `True`, the `if`-block is exectured, and if it evaluated to `False`, it is the `else` block.

#### Completion else

**In contrast** to the **either…or**\* situation that we know from the conditional `else`, the completion `else` is executed if a code block finished.  
To show you an example, let us use `else` for error-handling:

##### Completion else (try-except)

```python
try:
    print('first element:', a_list[0])
except IndexError:
    print('raised IndexError')
else:
    print('no error in try-block')
```

```python
first element: 1
no error in try-block
```

```python
try:
    print('third element:', a_list[2])
except IndexError:
    print('raised IndexError')
else:
    print('no error in try-block')
```

```python
raised IndexError
```

In the code above, we can see that the code under the **`else`-clause is only executed if the `try-block` was executed without encountering an error, i.e., if the `try`-block is “complete”.**  
The same rule applies to the “completion” `else` in while- and for-loops, which you can confirm in the following samples below.

##### Completion else (while-loop)

```python
i = 0
while i < 2:
    print(i)
    i += 1
else:
    print('in else')
```

```python
0
1
in else
```

```python
i = 0
while i < 2:
    print(i)
    i += 1
    break
else:
    print('completed while-loop')
```

```python
0
```

##### Completion else (for-loop)

```python
for i in range(2):
    print(i)
else:
    print('completed for-loop')
```

```python
0
1
completed for-loop
```

```python
for i in range(2):
    print(i)
    break
else:
    print('completed for-loop')
```

```python
0
```

### Interning of compile-time constants vs. run-time expressions

This might not be particularly useful, but it is nonetheless interesting: Python’s interpreter is interning compile-time constants but not run-time expressions (note that this is implementation-specific).

(Original source: [Stackoverflow](http://stackoverflow.com/questions/15541404/python-string-interning))

Let us have a look at the simple example below. Here we are creating 3 variables and assign the value “Hello” to them in different ways before we test them for identity.

```python
hello1 = 'Hello'

hello2 = 'Hell' + 'o'

hello3 = 'Hell'
hello3 = hello3 + 'o'

print('hello1 is hello2:', hello1 is hello2)
print('hello1 is hello3:', hello1 is hello3)
```

```python
hello1 is hello2: True
hello1 is hello3: False
```

Now, how does it come that the first expression evaluates to true, but the second does not? To answer this question, we need to take a closer look at the underlying byte codes:

```python
import dis
def hello1_func():
    s = 'Hello'
    return s
dis.dis(hello1_func)
```

```python
  3           0 LOAD_CONST               1 ('Hello')
              3 STORE_FAST               0 (s)

  4           6 LOAD_FAST                0 (s)
              9 RETURN_VALUE
```

```python
def hello2_func():
    s = 'Hell' + 'o'
    return s
dis.dis(hello2_func)
```

```python
  2           0 LOAD_CONST               3 ('Hello')
              3 STORE_FAST               0 (s)

  3           6 LOAD_FAST                0 (s)
              9 RETURN_VALUE
```

```python
def hello3_func():
    s = 'Hell'
    s = s + 'o'
    return s
dis.dis(hello3_func)
```

```python
  2           0 LOAD_CONST               1 ('Hell')
              3 STORE_FAST               0 (s)

  3           6 LOAD_FAST                0 (s)
              9 LOAD_CONST               2 ('o')
             12 BINARY_ADD
             13 STORE_FAST               0 (s)

  4          16 LOAD_FAST                0 (s)
             19 RETURN_VALUE
```

It looks like that `'Hello'` and `'Hell'` + `'o'` are both evaluated and stored as `'Hello'` at compile-time, whereas the third version   
`s = 'Hell'`  
`s = s + 'o'` seems to not be interned. Let us quickly confirm the behavior with the following code:

```python
print(hello1_func() is hello2_func())
print(hello1_func() is hello3_func())
```

```python
True
False
```

Finally, to show that this hypothesis is the answer to this rather unexpected observation, let us `intern` the value manually:

```python
import sys

print(hello1_func() is sys.intern(hello3_func()))
```

```python
True
```
