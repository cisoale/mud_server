from lupa import LuaRuntime

lua = LuaRuntime(unpack_returned_tuples=True)

def run_script(path, context={}):
    with open(path) as f:
        code = f.read()

    lua_func = lua.execute(code)
    return lua_func(context)