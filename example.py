from farah import run


def output_callback(x):
    print("[OUTPUT] " + x)


def error_callback(x):
    print("[ERROR] " + x)


return_code = run("./ticker.py", output_callback, error_callback)
print("Finished with return code:", return_code)
