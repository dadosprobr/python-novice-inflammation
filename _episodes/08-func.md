---
title: Creating Functions
teaching: 30
exercises: 0
questions:
- "How can I define new functions?"
- "What's the difference between defining and calling a function?"
- "What happens when I call a function?"
objectives:
- "Define a function that takes parameters."
- "Return a value from a function."
- "Test and debug a function."
- "Set default values for function parameters."
- "Explain why we should divide programs into small, single-purpose functions."
keypoints:
- "Define a function using `def function_name(parameter)`."
- "The body of a function must be indented."
- "Call a function using `function_name(value)`."
- "Numbers are stored as integers or floating-point numbers."
- "Variables defined within a function can only be seen and used within the body of the function."
- "If a variable is not defined within the function it is used,
   Python looks for a definition before the function call"
- "Use `help(thing)` to view help for something."
- "Put docstrings in functions to provide help for that function."
- "Specify default values for parameters when defining a function using `name=value`
   in the parameter list."
- "Parameters can be passed by matching based on name, by position,
   or by omitting them (in which case the default value is used)."
- "Put code whose parameters change frequently in a function,
   then call it with different parameter values to customize its behavior."
---

At this point,
we've written code to draw some interesting features in our inflammation data,
loop over all our data files to quickly draw these plots for each of them,
and have Python make decisions based on what it sees in our data.
But, our code is getting pretty long and complicated;
what if we had thousands of datasets,
and didn't want to generate a figure for every single one?
Commenting out the figure-drawing code is a nuisance.
Also, what if we want to use that code again,
on a different dataset or at a different point in our program?
Cutting and pasting it is going to make our code get very long and very repetitive,
very quickly.
We'd like a way to package our code so that it is easier to reuse,
and Python provides for this by letting us define things called 'functions' ---
a shorthand way of re-executing longer pieces of code.
Let's start by defining a function `fahr_to_celsius` that converts temperatures
from Fahrenheit to Celsius:

~~~
def fahr_to_celsius(temp):
    return ((temp - 32) * (5/9))
~~~
{: .language-python}

![Labeled parts of a Python function definition](../fig/python-function.svg)


The function definition opens with the keyword `def` followed by the
name of the function (`fahr_to_celsius`) and a parenthesized list of parameter names (`temp`). The
[body]({{ page.root }}/reference/#body) of the function --- the
statements that are executed when it runs --- is indented below the
definition line.  The body concludes with a `return` keyword followed by the return value.

When we call the function,
the values we pass to it are assigned to those variables
so that we can use them inside the function.
Inside the function,
we use a [return statement]({{ page.root }}/reference/#return-statement) to send a result
back to whoever asked for it.

Let's try running our function.

~~~
fahr_to_celsius(32)
~~~
{: .language-python}

This command should call our function, using "32" as the input and return the function value.

In fact, calling our own function is no different from calling any other function:
~~~
print('freezing point of water:', fahr_to_celsius(32), 'C')
print('boiling point of water:', fahr_to_celsius(212), 'C')
~~~
{: .language-python}

~~~
freezing point of water: 0.0 C
boiling point of water: 100.0 C
~~~
{: .output}

We've successfully called the function that we defined,
and we have access to the value that we returned.


## Composing Functions

Now that we've seen how to turn Fahrenheit into Celsius,
we can also write the function to turn Celsius into Kelvin:

~~~
def celsius_to_kelvin(temp_c):
    return temp_c + 273.15

print('freezing point of water in Kelvin:', celsius_to_kelvin(0.))
~~~
{: .language-python}

~~~
freezing point of water in Kelvin: 273.15
~~~
{: .output}

What about converting Fahrenheit to Kelvin?
We could write out the formula,
but we don't need to.
Instead,
we can [compose]({{ page.root }}/reference/#compose) the two functions we have already created:

~~~
def fahr_to_kelvin(temp_f):
    temp_c = fahr_to_celsius(temp_f)
    temp_k = celsius_to_kelvin(temp_c)
    return temp_k

print('boiling point of water in Kelvin:', fahr_to_kelvin(212.0))
~~~
{: .language-python}

~~~
boiling point of water in Kelvin: 373.15
~~~
{: .output}

This is our first taste of how larger programs are built:
we define basic operations,
then combine them in ever-larger chunks to get the effect we want.
Real-life functions will usually be larger than the ones shown here --- typically half a dozen
to a few dozen lines --- but they shouldn't ever be much longer than that,
or the next person who reads it won't be able to understand what's going on.

## Tidying up

Now that we know how to wrap bits of code up in functions,
we can make our inflammation analysis easier to read and easier to reuse.
First, let's make a `visualize` function that generates our plots:

~~~
def visualize(filename):

    data = numpy.loadtxt(fname=filename, delimiter=',')

    fig = matplotlib.pyplot.figure(figsize=(10.0, 3.0))

    axes1 = fig.add_subplot(1, 3, 1)
    axes2 = fig.add_subplot(1, 3, 2)
    axes3 = fig.add_subplot(1, 3, 3)

    axes1.set_ylabel('average')
    axes1.plot(numpy.mean(data, axis=0))

    axes2.set_ylabel('max')
    axes2.plot(numpy.max(data, axis=0))

    axes3.set_ylabel('min')
    axes3.plot(numpy.min(data, axis=0))

    fig.tight_layout()
    matplotlib.pyplot.show()
~~~
{: .language-python}

and another function called `detect_problems` that checks for those systematics
we noticed:

~~~
def detect_problems(filename):

    data = numpy.loadtxt(fname=filename, delimiter=',')

    if numpy.max(data, axis=0)[0] == 0 and numpy.max(data, axis=0)[20] == 20:
        print('Suspicious looking maxima!')
    elif numpy.sum(numpy.min(data, axis=0)) == 0:
        print('Minima add up to zero!')
    else:
        print('Seems OK!')
~~~
{: .language-python}

Wait! Didn't we forget to specify what both of these functions should return? Well, we didn't.
In Python, functions are not required to include a `return` statement and can be used for
the sole purpose of grouping together pieces of code that conceptually do one thing. In such cases,
function names usually describe what they do, _e.g._ `visualize`, `detect_problems`.

Notice that rather than jumbling this code together in one giant `for` loop,
we can now read and reuse both ideas separately.
We can reproduce the previous analysis with a much simpler `for` loop:

~~~
filenames = sorted(glob.glob('inflammation*.csv'))

for filename in filenames[:3]:
    print(filename)
    visualize(filename)
    detect_problems(filename)
~~~
{: .language-python}

By giving our functions human-readable names,
we can more easily read and understand what is happening in the `for` loop.
Even better, if at some later date we want to use either of those pieces of code again,
we can do so in a single line.

## Testing and Documenting

Once we start putting things in functions so that we can re-use them,
we need to start testing that those functions are working correctly.
To see how to do this,
let's write a function to offset a dataset so that it's mean value
shifts to a user-defined value:

~~~
def offset_mean(data, target_mean_value):
    return (data - numpy.mean(data)) + target_mean_value
~~~
{: .language-python}

We could test this on our actual data,
but since we don't know what the values ought to be,
it will be hard to tell if the result was correct.
Instead,
let's use NumPy to create a matrix of 0's
and then offset its values to have a mean value of 3:

~~~
z = numpy.zeros((2,2))
print(offset_mean(z, 3))
~~~
{: .language-python}

~~~
[[ 3.  3.]
 [ 3.  3.]]
~~~
{: .output}

That looks right,
so let's try `offset_mean` on our real data:

~~~
data = numpy.loadtxt(fname='inflammation-01.csv', delimiter=',')
print(offset_mean(data, 0))
~~~
{: .language-python}

~~~
[[-6.14875 -6.14875 -5.14875 ... -3.14875 -6.14875 -6.14875]
 [-6.14875 -5.14875 -4.14875 ... -5.14875 -6.14875 -5.14875]
 [-6.14875 -5.14875 -5.14875 ... -4.14875 -5.14875 -5.14875]
 ...
 [-6.14875 -5.14875 -5.14875 ... -5.14875 -5.14875 -5.14875]
 [-6.14875 -6.14875 -6.14875 ... -6.14875 -4.14875 -6.14875]
 [-6.14875 -6.14875 -5.14875 ... -5.14875 -5.14875 -6.14875]]
~~~
{: .output}

It's hard to tell from the default output whether the result is correct,
but there are a few tests that we can run to reassure us:

~~~
print('original min, mean, and max are:', numpy.min(data), numpy.mean(data), numpy.max(data))
offset_data = offset_mean(data, 0)
print('min, mean, and max of offset data are:',
      numpy.min(offset_data),
      numpy.mean(offset_data),
      numpy.max(offset_data))
~~~
{: .language-python}

~~~
original min, mean, and max are: 0.0 6.14875 20.0
min, mean, and and max of offset data are: -6.14875 2.84217094304e-16 13.85125
~~~
{: .output}

That seems almost right:
the original mean was about 6.1,
so the lower bound from zero is now about -6.1.
The mean of the offset data isn't quite zero --- we'll explore why not in the challenges --- but
it's pretty close.
We can even go further and check that the standard deviation hasn't changed:

~~~
print('std dev before and after:', numpy.std(data), numpy.std(offset_data))
~~~
{: .language-python}

~~~
std dev before and after: 4.61383319712 4.61383319712
~~~
{: .output}

Those values look the same,
but we probably wouldn't notice if they were different in the sixth decimal place.
Let's do this instead:

~~~
print('difference in standard deviations before and after:',
      numpy.std(data) - numpy.std(offset_data))
~~~
{: .language-python}

~~~
difference in standard deviations before and after: -3.5527136788e-15
~~~
{: .output}

Again,
the difference is very small.
It's still possible that our function is wrong,
but it seems unlikely enough that we should probably get back to doing our analysis.
We have one more task first, though:
we should write some [documentation]({{ page.root }}/reference/#documentation) for our function
to remind ourselves later what it's for and how to use it.

The usual way to put documentation in software is
to add [comments]({{ page.root }}/reference/#comment) like this:

~~~
# offset_mean(data, target_mean_value):
# return a new array containing the original data with its mean offset to match the desired value.
def offset_mean(data, target_mean_value):
    return (data - numpy.mean(data)) + target_mean_value
~~~
{: .language-python}

There's a better way, though.
If the first thing in a function is a string that isn't assigned to a variable,
that string is attached to the function as its documentation:

~~~
def offset_mean(data, target_mean_value):
    '''Return a new array containing the original data
       with its mean offset to match the desired value.'''
    return (data - numpy.mean(data)) + target_mean_value
~~~
{: .language-python}

This is better because we can now ask Python's built-in help system to show us
the documentation for the function:

~~~
help(offset_mean)
~~~
{: .language-python}

~~~
Help on function offset_mean in module __main__:

offset_mean(data, target_mean_value)
    Return a new array containing the original data with its mean offset to match the desired value.
~~~
{: .output}

A string like this is called a [docstring]({{ page.root }}/reference/#docstring).
We don't need to use triple quotes when we write one,
but if we do,
we can break the string across multiple lines:

~~~
def offset_mean(data, target_mean_value):
    '''Return a new array containing the original data
       with its mean offset to match the desired value.

    Examples
    --------
    >>> offset_mean([1, 2, 3], 0)
    array([-1.,  0.,  1.])
    '''
    return (data - numpy.mean(data)) + target_mean_value

help(offset_mean)
~~~
{: .language-python}

~~~
Help on function offset_mean in module __main__:

offset_mean(data, target_mean_value)
    Return a new array containing the original data
       with its mean offset to match the desired value.

    Examples
    --------
    >>> offset_mean([1, 2, 3], 0)
    array([-1.,  0.,  1.])
~~~
{: .output}

## Defining Defaults

We have passed parameters to functions in two ways:
directly, as in `type(data)`,
and by name, as in `numpy.loadtxt(fname='something.csv', delimiter=',')`.
In fact,
we can pass the filename to `loadtxt` without the `fname=`:

~~~
numpy.loadtxt('inflammation-01.csv', delimiter=',')
~~~
{: .language-python}

~~~
array([[ 0.,  0.,  1., ...,  3.,  0.,  0.],
       [ 0.,  1.,  2., ...,  1.,  0.,  1.],
       [ 0.,  1.,  1., ...,  2.,  1.,  1.],
       ...,
       [ 0.,  1.,  1., ...,  1.,  1.,  1.],
       [ 0.,  0.,  0., ...,  0.,  2.,  0.],
       [ 0.,  0.,  1., ...,  1.,  1.,  0.]])
~~~
{: .output}

but we still need to say `delimiter=`:

~~~
numpy.loadtxt('inflammation-01.csv', ',')
~~~
{: .language-python}

~~~
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/username/anaconda3/lib/python3.6/site-packages/numpy/lib/npyio.py", line 1041, in loa
dtxt
    dtype = np.dtype(dtype)
  File "/Users/username/anaconda3/lib/python3.6/site-packages/numpy/core/_internal.py", line 199, in
_commastring
    newitem = (dtype, eval(repeats))
  File "<string>", line 1
    ,
    ^
SyntaxError: unexpected EOF while parsing
~~~
{: .error}

To understand what's going on,
and make our own functions easier to use,
let's re-define our `offset_mean` function like this:

~~~
def offset_mean(data, target_mean_value=0.0):
    '''Return a new array containing the original data
       with its mean offset to match the desired value, (0 by default).

    Examples
    --------
    >>> offset_mean([1, 2, 3])
    array([-1.,  0.,  1.])
    '''
    return (data - numpy.mean(data)) + target_mean_value
~~~
{: .language-python}

The key change is that the second parameter is now written `target_mean_value=0.0`
instead of just `target_mean_value`.
If we call the function with two arguments,
it works as it did before:

~~~
test_data = numpy.zeros((2, 2))
print(offset_mean(test_data, 3))
~~~
{: .language-python}

~~~
[[ 3.  3.]
 [ 3.  3.]]
~~~
{: .output}

But we can also now call it with just one parameter,
in which case `target_mean_value` is automatically assigned
the [default value]({{ page.root }}/reference/#default-value) of 0.0:

~~~
more_data = 5 + numpy.zeros((2, 2))
print('data before mean offset:')
print(more_data)
print('offset data:')
print(offset_mean(more_data))
~~~
{: .language-python}

~~~
data before mean offset:
[[ 5.  5.]
 [ 5.  5.]]
offset data:
[[ 0.  0.]
 [ 0.  0.]]
~~~
{: .output}

This is handy:
if we usually want a function to work one way,
but occasionally need it to do something else,
we can allow people to pass a parameter when they need to
but provide a default to make the normal case easier.
The example below shows how Python matches values to parameters:

~~~
def display(a=1, b=2, c=3):
    print('a:', a, 'b:', b, 'c:', c)

print('no parameters:')
display()
print('one parameter:')
display(55)
print('two parameters:')
display(55, 66)
~~~
{: .language-python}

~~~
no parameters:
a: 1 b: 2 c: 3
one parameter:
a: 55 b: 2 c: 3
two parameters:
a: 55 b: 66 c: 3
~~~
{: .output}

As this example shows,
parameters are matched up from left to right,
and any that haven't been given a value explicitly get their default value.
We can override this behavior by naming the value as we pass it in:

~~~
print('only setting the value of c')
display(c=77)
~~~
{: .language-python}

~~~
only setting the value of c
a: 1 b: 2 c: 77
~~~
{: .output}

With that in hand,
let's look at the help for `numpy.loadtxt`:

~~~
help(numpy.loadtxt)
~~~
{: .language-python}

~~~
Help on function loadtxt in module numpy.lib.npyio:

loadtxt(fname, dtype=<class 'float'>, comments='#', delimiter=None, converters=None, skiprows=0, use
cols=None, unpack=False, ndmin=0, encoding='bytes')
    Load data from a text file.

    Each row in the text file must have the same number of values.

    Parameters
    ----------
...
~~~
{: .output}

There's a lot of information here,
but the most important part is the first couple of lines:

~~~
loadtxt(fname, dtype=<class 'float'>, comments='#', delimiter=None, converters=None, skiprows=0, use
cols=None, unpack=False, ndmin=0, encoding='bytes')
~~~
{: .output}

This tells us that `loadtxt` has one parameter called `fname` that doesn't have a default value,
and eight others that do.
If we call the function like this:

~~~
numpy.loadtxt('inflammation-01.csv', ',')
~~~
{: .language-python}

then the filename is assigned to `fname` (which is what we want),
but the delimiter string `','` is assigned to `dtype` rather than `delimiter`,
because `dtype` is the second parameter in the list. However `','` isn't a known `dtype` so
our code produced an error message when we tried to run it.
When we call `loadtxt` we don't have to provide `fname=` for the filename because it's the
first item in the list, but if we want the `','` to be assigned to the variable `delimiter`,
we *do* have to provide `delimiter=` for the second parameter since `delimiter` is not
the second parameter in the list.

## Readable functions

Consider these two functions:

~~~
def s(p):
    a = 0
    for v in p:
        a += v
    m = a / len(p)
    d = 0
    for v in p:
        d += (v - m) * (v - m)
    return numpy.sqrt(d / (len(p) - 1))

def std_dev(sample):
    sample_sum = 0
    for value in sample:
        sample_sum += value

    sample_mean = sample_sum / len(sample)

    sum_squared_devs = 0
    for value in sample:
        sum_squared_devs += (value - sample_mean) * (value - sample_mean)

    return numpy.sqrt(sum_squared_devs / (len(sample) - 1))
~~~
{: .language-python}

The functions `s` and `std_dev` are computationally equivalent (they
both calculate the sample standard deviation), but to a human reader,
they look very different. You probably found `std_dev` much easier to
read and understand than `s`.

As this example illustrates, both documentation and a programmer's
_coding style_ combine to determine how easy it is for others to read
and understand the programmer's code. Choosing meaningful variable
names and using blank spaces to break the code into logical "chunks"
are helpful techniques for producing _readable code_. This is useful
not only for sharing code with others, but also for the original
programmer. If you need to revisit code that you wrote months ago and
haven't thought about since then, you will appreciate the value of
readable code!

> ## Combinando Strings
>
> "Adicionar" duas strings produz sua concatenação:
> `'a' + 'b'` é `'ab'`.
> Escreva uma função chamada `fence` que use dois parâmetros chamados `original` e `wrapper`
> e retorne uma nova string que contenha os caracteres de wrapper no início e no fim do original.
> A chamada da sua função deve ser assim:
>
> ~~~
> print(fence('name', '*'))
> ~~~
> {: .language-python}
>
> ~~~
> *name*
> ~~~
> {: .output}
>
> > ## Solução
> > ~~~
> > def fence(original, wrapper):
> >     return wrapper + original + wrapper
> > ~~~
> > {: .language-python}
> {: .solution}
{: .challenge}

> ## Return versus print
>
> Note que `return` e `print` não são intercambiáveis.
> `print` é uma função Python que *exibe* dados na tela.
> Permite que nós, *usuários*, vejamos os dados.
> A instrução `return`, por outro lado, torna os dados visíveis ao programa.
> Vamos dar uma olhada na seguinte função:
>
> ~~~
> def add(a, b):
>     print(a + b)
> ~~~
> {: .language-python}
>
> **Pergunta**: O que veremos se executarmos os seguintes comandos??
> ~~~
> A = add(7, 3)
> print(A)
> ~~~
> {: .language-python}
>
> > ## Solução
> > O Python executará primeiro a função `add` com `a = 7` e `b = 3`,
> > e então, exibirá `10`. No entanto, como a função `add` não tem uma
> > linha que se inicia com `return` (sem "instrução" `return`), ela irá, por padrão, retornar
> > nada, que, no mundo Python, é chamado `None`. Portanto, `A` será atribuído a `None`
> > e a última linha (`print(A)`) exibirá `None`. Como resultado, veremos:
> > ~~~
> > 10
> > None
> > ~~~
> > {: .output}
> {: .solution}
{: .challenge}

> ## Selecionando Caracteres de Strings
>
> Se a variável `s` se referir a uma string,
> então `s[0]` é o primeiro caractere da string
> e `s[-1]` é o último.
> Escreva uma função chamada `outer`
> que retorne uma string composta apenas pelo primeiro e último caractere de sua entrada.
> A chamada da sua função deve ser assim:
>
> ~~~
> print(outer('helium'))
> ~~~
> {: .language-python}
>
> ~~~
> hm
> ~~~
> {: .output}
>
> > ## Solução
> > ~~~
> > def outer(input_string):
> >     return input_string[0] + input_string[-1]
> > ~~~
> > {: .language-python}
> {: .solution}
{: .challenge}

> ## Normalizando um Array
>
> Escreva uma função chamada `rescale` que receba um array de entrada
> e retorne um array correspondente de valores dimensionados dentro do intervalo 0.0 e 1.0.
> (Dica: Se `L` e `H` são os valores mais baixo e mais alto no array original,
> então a substituição por um valor `v` deve ser `(v-L) / (H-L)`.)
>
> > ## Solução
> > ~~~
> > def rescale(input_array):
> >     L = numpy.min(input_array)
> >     H = numpy.max(input_array)
> >     output_array = (input_array - L) / (H - L)
> >     return output_array
> > ~~~
> > {: .language-python}
> {: .solution}
{: .challenge}

> ## Testando e Documentando Sua Função
>
> Execute os comandos `help(numpy.arange)` e `help(numpy.linspace)`
> para ver como usar essas funções para gerar valores regularmente espaçados,
> então use esses valores para testar sua função `rescale`.
> Quando você tiver testado com êxito sua função,
> adicione uma docstring que explique o que ela faz.
>
> > ## Solução
> > ~~~
> > '''Recebe um array como entrada e retorna um array correspondente
> > dimensionado para que 0 corresponda ao valor mínimo e 1 ao
> > valor máximo do array de entrada.
> >
> > Exemplo:
> > >>> rescale(numpy.arange(10.0))
> > array([ 0.        ,  0.11111111,  0.22222222,  0.33333333,  0.44444444,
> >        0.55555556,  0.66666667,  0.77777778,  0.88888889,  1.        ])
> > >>> rescale(numpy.linspace(0, 100, 5))
> > array([ 0.  ,  0.25,  0.5 ,  0.75,  1.  ])
> > '''
> > ~~~
> > {: .language-python}
> {: .solution}
{: .challenge}

> ## Definindo Padrões
>
> Reescreva a função `rescale` para que ela dimensione os dados para ficar entre `0.0` e `1.0` por
> padrão, mas que permita que o chamador especifique o limite inferior e superior, se desejar.
> Compare sua implementação com a de seu vizinho:
> As duas funções sempre se comportam da mesma maneira?
>
> > ## Solução
> > ~~~
> > def rescale(input_array, low_val=0.0, high_val=1.0):
> >     '''rescales input array values to lie between low_val and high_val'''
> >     L = numpy.min(input_array)
> >     H = numpy.max(input_array)
> >     intermed_array = (input_array - L) / (H - L)
> >     output_array = intermed_array * (high_val - low_val) + low_val
> >     return output_array
> > ~~~
> > {: .language-python}
> {: .solution}
{: .challenge}

> ## Variáveis Internas e Externas da Função
>
> O que o seguinte trecho de código exibe quanto executado --- e por quê?
>
> ~~~
> f = 0
> k = 0
>
> def f2k(f):
>     k = ((f-32)*(5.0/9.0)) + 273.15
>     return k
>
> f2k(8)
> f2k(41)
> f2k(32)
>
> print(k)
> ~~~
> {: .language-python}
>
> > ## Solução
> >
> > ~~~
> > 259.81666666666666
> > 287.15
> > 273.15
> > 0
> > ~~~
> > {: .output}
> > `k` é 0 porque o `k` interno da função `f2k` não conhece
> > o valor de `k` definido fora da função.
> {: .solution}
{: .challenge}

> ## Mesclando parâmetros Padrão e Não-Padrão
>
> Dado o seguinte código:
>
> ~~~
> def numbers(one, two=2, three, four=4):
>     n = str(one) + str(two) + str(three) + str(four)
>     return n
>
> print(numbers(1, three=3))
> ~~~
> {: .language-python}
>
> O que você espera que seja exibido? O que é realmente exibido?
> Que regra você pensa que o Python está seguindo?
>
> 1.  `1234`
> 2.  `one2three4`
> 3.  `1239`
> 4.  `SyntaxError`
>
> Dado isso, o que o seguinte trecho de código exibe quando executado?
>
> ~~~
> def func(a, b=3, c=6):
>     print('a: ', a, 'b: ', b, 'c:', c)
>
> func(-1, 2)
> ~~~
> {: .language-python}
>
> 1. `a: b: 3 c: 6`
> 2. `a: -1 b: 3 c: 6`
> 3. `a: -1 b: 2 c: 6`
> 4. `a: b: -1 c: 2`
>
> > ## Solução
> > Tentar definir a função `numbers` resulta em `4. SyntaxError`.
> > Os parâmetros definidos `two` e `four` recebem valor padrão. Como
> > `one` e `three` não recebem valor padrão, eles precisam ser incluídos como
> > argumentos quando a função é chamada e devem ser colocados
> > antes de quaisquer parâmetros que tenham valores padrão na definição da função.
> >
> > A chamada da função `func` exibe `a: -1 b: 2 c: 6`. -1 é atribuído ao
> > primeiro parâmetro `a`, 2 é atribuído ao próximo parâmetro `b`, e nenhum
> > valor é atribuído ao parâmetro `c`, então ele usa seu valor padrão 6.
> {: .solution}
{: .challenge}

> ## O Velho Troca Troca
>
> Considere o código:
>
> ~~~
> a = 3
> b = 7
>
> def swap(a, b):
>     temp = a
>     a = b
>     b = temp
>
> swap(a, b)
>
> print(a, b)
> ~~~
> {: .language-python}
>
> Qual das opções a seguir seria exibida se você executasse esse código?
> Por que você escolheu esta resposta?
>
> 1. `7 3`
> 2. `3 7`
> 3. `3 3`
> 4. `7 7`
>
> > ## Solução
> > `3 7` é a resposta correta. Inicialmente, `a` tem o valor 3 e `b` tem o valor 7.
> > Quando a função `swap` é chamada, ela cria variáveis locais (também chamadas de
> > `a` e `b` neste caso) e negocia seus valores. A função não retorna
> > valor algum e não altera `a` ou `b` de fora da sua cópia local.
> > Portanto os valores originais de `a` e `b` permanecem inalterados.
> {: .solution}
{: .challenge}

> ## Código Legível
>
> Revise uma função que você escreveu em um dos exercícios anteriores para tentar
> criar um código mais legível. Em seguida, colabore com um de seus vizinhos
> para criticar as funções uns dos outros e discutir como suas implementações de
> funções poderiam ser melhoradas para se tornarem mais legíveis.
{: .challenge}

{% include links.md %}
