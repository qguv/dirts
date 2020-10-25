#!/usr/bin/env python3

import argparse
import itertools
import operator
import pathlib
import sys
import termios
import tty


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def ask(prompt, choices):
    choices_msg = '/'.join(choices)
    choices_msg = f"[{choices_msg}]"

    default = None
    try:
        default = [c for c in choices if c.isupper()][0].lower()
    except IndexError:
        pass
    choices = choices.lower()

    while True:
        print(f"{prompt:<35} {choices_msg:>10} ", file=sys.stderr, end="")
        sys.stderr.flush()

        ch = getch().strip()[0].lower()
        if ch == '\r' and default is not None:
            print(default, file=sys.stderr)
            return default

        if ch in choices:
            print(ch, file=sys.stderr)
            return ch
        elif ch in 'q\x03\x04\x1a\x1b':
            print("\nExiting...", file=sys.stderr)
            sys.exit(1)
        else:
            print(repr(ch), file=sys.stderr)


def subdirs(path):
    return [child for child in path.iterdir() if child.is_dir()]


def dirts(dirs, top=True):
    accept_rest = False
    for d in dirs:

        if accept_rest:
            yield d
            continue

        choices = 'Yn'
        if len(dirs) > 1:
            choices += 'ad'

        children = subdirs(d)
        while len(children) == 1:
            grandchildren = subdirs(children[0])
            if not grandchildren:
                break
            children = grandchildren

        if len(children) > 1:
            choices += 's'

        if top:
            choice = 's'
        else:
            choice = 's' if top else ask(f"{d}/", choices)

        if choice == 'd':
            break
        elif choice == 'a':
            accept_rest = True
            yield d
        elif choice == 'y':
            yield d
        elif choice == 's':
            yield from dirts(children, top=False)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('DIRS', nargs='+')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    roots = map(pathlib.Path, args.DIRS)
    roots = [root for root in roots if root.is_dir()]
    for path in dirts(roots):
        print(f"{path}/")
