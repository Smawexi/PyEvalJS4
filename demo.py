import pyevaljs4

# example 1
rt = pyevaljs4.compile_("function f(a,b){console.log(a,b);return a+b;}")
res = rt.call('f', 'x', 'y')
print(res)
assert res == "xy"
# Another way of passing parameters
res = rt.call('f', arg_list=['x', 'y'])
print(res)
assert res == "xy"
# Other equivalent calling methods
print(rt.f('x',  'y'))
print(rt.f(arg_list=['x', 'y']))
# close runtime
rt.close()

# example 2
with pyevaljs4.compile_("function f(a,b){console.log(a,b);return a+b;}") as rt:
    res = rt.call('f', 'x', 'y')
    print(res)
    assert res == "xy"

# example 3
# empty context
rt = pyevaljs4.compile_()
# Add the function f to this context
rt.eval("function f(a,b){console.log(a,b);return a+b;}")
res = rt.call('f', 'x', 'y')
print(res)
assert res == 'xy'
# Other calling methods
res = rt.eval("f('x', 'y')")
print(res)
assert res == "xy"
rt.close()

# Call JS asynchronous function
rt = pyevaljs4.compile_()
rt.eval("async function f(a,b){console.log(a,b);return a+b;}")
# To call the JS asynchronous function, you need to pass async_js_func=True
res = rt.call('f', 'x', 'y', async_js_func=True)
print(res)
assert res == "xy"
res = rt.f('x', 'y', async_js_func=True)
print(res)
assert res == "xy"
# The shortcut for calling the JS asynchronous function can only be used this way.
# other cases are not supported.
res = rt.eval('await f("x", "y")')
print(res)
assert res == "xy"
rt.close()
