#!/usr/bin/env python

import os

import sys


def error(x):
    os.write(2, str(x).encode(sys.stdout.encoding))
    sys.stderr.flush()


print("Hello, world...")
error("lol")
print("done?")
error("lol2")
print("now I'm done")