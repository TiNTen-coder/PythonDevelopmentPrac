import shlex

while s := input(">> "):
    try:
        print(shlex.join(shlex.split(s)))
    except Exception as E:
        print(E)
