# Paginator for LeadzAI

## Dependencies
No dependencies - decided to skip *pytests* and do a take on *unittest*. Tested on Python **3.9**, however, should work almost with any version.

## Installation
```
git clone https://github.com/holohup/paginator.git && cd paginator
```

## Running

First create an instance with your parameters:
```
p = Paginator(5, 10, 1, 1)
```
Then call the *print_pages()* method to print the pagination:
```
p.print_pages()
```
You can also get the *get_pages()* method to get a pages string without printing and do whatever you please with it.

## Testing

All the tests are inside the *tests.py* file.
```
python -m unittest -v
```
