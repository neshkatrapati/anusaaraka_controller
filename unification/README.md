# What is this ?

A set of simple decorators that wrap around nltk.featstruct which do function dispatch based on unification.
# How to dispatch ?
``` python
@dispatch("[tense:'present']")
def if_tense_present(fs):
    ...
    ...
```

Then call

``` python
if_tense_present("[tense:'']")
```

# How to inherit.
If we are going to write a specific rule we might as well inherit a more generic rule than writing the whole feature structure

``` python
@inherit(if_tense_present, "[number:'plural']")
def if_tense_present_plural(fs):
  ...
  ...
```
