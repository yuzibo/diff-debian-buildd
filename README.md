This is a python demo to diff Debian buildd status between two build.

We still need to train it more.


# Basic usage:

## 0

Running `generate_data.py` to get the last buildd status json file and to store in `date/`

```python
python3 generate_data.py
```

## 1

To analyst the result:

````
vimer@dev:~/dev$ python analyst.py --old=data/2023-02-11.json --new=data/2023-02-12.json
Auto-Not-For-Us:
Old disappered packages since previous build(2023-02-11):
No change
New added packages at last build(2023-02-12):
No change


BD-Uninstallable:
Old disappered packages since previous build(2023-02-11):
{'haskell-fold-debounce', 'evolution-ews'}
New added packages at last build(2023-02-12):
No change


Build-Attempted:
Old disappered packages since previous build(2023-02-11):
{'editorconfig-core', 'haskell-stm-delay', 'rust-r2d2', 'ring', 'neovim', 'rust-jemalloc-sys'}
New added packages at last build(2023-02-12):
{'xdp-tools'}


Failed:
Old disappered packages since previous build(2023-02-11):
No change
New added packages at last build(2023-02-12):
{'rust-jemalloc-sys'}

```
