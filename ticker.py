#!/usr/bin/env python

import sys

import time


def error(x):
    sys.stderr.write(x + "\n")


print("Hello, world...")
time.sleep(0.1)
error("lol")
time.sleep(0.1)
print("done?")
time.sleep(0.1)
error("lol2")
time.sleep(0.1)
print("now I'm done")