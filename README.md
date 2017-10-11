Farah
======

#### Subprocesses for Humans™

Dealing with running external commands in Python can be a *nightmare*. Especially when you care about the output.

Farah tries hard to give you easier access to the outputs—both stdout and stderr—of a running subprocess.

At its heart, the API is deliberately simple:

```python
from farah import run

result = run("echo 'hello, world'")
```

But this does no more than a simple `os.system` call. Let's capture the output of that call, by specifying the `output_callback` argument.

```python
def log(msg):
    print("Got output:", msg)

result = run("echo 'hello, world'", log)
```

We can also capture anything sent to stderr, like so:

```python
def error(msg):
    print("Got error:", msg)

result = run("./error.sh", log, error)
```

