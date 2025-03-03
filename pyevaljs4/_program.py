NODE_PROGRAM = """
try {{
    var __process = process;  
}} catch (e) {{
    console.log('[[<<exception>>]]' + JSON.stringify(e.stack));
}}
try {{
    globalThis.require = require;
    globalThis.exports = exports;
    globalThis.module = module;
    globalThis.__filename = __filename;
    globalThis.__dirname = __dirname;
}} catch (e) {{}}
try {{
   globalThis.eval({source}); 
}} catch (e) {{
    console.log('[[<<exception>>]]' + JSON.stringify(e.stack));
}}
__process.stdin.setEncoding('utf8');
__process.stdin.on('data', function(data) {{
    let input = data.trim();
    try {{
        if (input.substring(0, 24) === "[[PyEvalJS4_Async_Call]]"){{
            globalThis.eval(input.substring(24))
        }} else {{
            var res = globalThis.eval(input)
            console.log('[[<<result>>]]' + JSON.stringify(res))
        }}
    }} catch (e) {{
        console.log('[[<<exception>>]]' + JSON.stringify(e.stack))
    }}
}});
__process.on('uncaughtException', (err) => {{
    console.log('[[<<exception>>]]' + err);
}});
"""

ASYNC_EVAL = """
(async () => {{
    try {{
        let res = {};
        console.log('[[<<result>>]]' + JSON.stringify(res));
    }} catch (e) {{
        console.log('[[<<exception>>]]' + JSON.stringify(e.stack))
    }}
}})();
"""

ASYNC_CALL = "{flags}{func}.apply(this, {args}).then(res => {{console.log('[[<<result>>]]' + JSON.stringify(res))}}, err => {{console.log('[[<<exception>>]]' + JSON.stringify(err.stack))}})"
SYNC_CALL = "{func}.apply(this, {args})"
