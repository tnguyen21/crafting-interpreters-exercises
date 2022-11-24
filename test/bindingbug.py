a = "global"
try:
    def showA():
        print(a)

    showA() # prints "global"
    a = "block"
    showA() # prints "block"
except:
    print("fail")

"""
if we're respecting closures then the above code
is weird! buggy!

but this is valid python and behaves how i expect
it too...

what do other languages do?
are closures _that_ important?
"""
