# dirts

_DIRectory Tree Selector_

Takes some paths as arguments. Recurses through subdirectories of these paths (like `find`) and asks whether you want to include them or not (like hunks in `git add --patch`). All included directories are printed to stdout.

## installation

After installing Python 3:

```sh
$ sudo cp dirts.py /usr/local/bin/dirts
```

## example

```sh
$ dirts my_project my_other_project > chosen_dirs.txt
my_project/doc/                      [Y/n/a/d] n
my_project/bin/                      [Y/n/a/d] n
my_project/src/                      [Y/n/a/d] y
my_other_project/doc/                [Y/n/a/d] n
my_other_project/bin/                [Y/n/a/d] n
my_other_project/src/               [Y/n/a/d/s] s
my_other_project/src/boring_stuff/   [Y/n/a/d] n
my_other_project/src/interesting_stuff/  [Y/n/a/d] y
$
```

## prompt

| key | meaning |
| --- | ------- |
| `y` | add this directory |
| `n` | don't add this directory |
| `s` | ask for each sub-directory |
| `a` | add this directory and all remaining siblings |
| `d` | don't add this directory or any remaining siblings |
| `q` | quit immediately with error code 1 |
| `^C` | quit immediately with error code 1 |
| `^D` | quit immediately with error code 1 |
| `^Z` | quit immediately with error code 1 |
| `ESC` | quit immediately with error code 1 |
