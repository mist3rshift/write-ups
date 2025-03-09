def decode_jsfuck(jsfuck_code):
    js_code = ""
    exec(jsfuck_code, {"js_code": js_code})
    return js_code

with open("./de-jsfuck/encoded.js", "r") as f:
    print("file open")
    jsfuck_code = f.read()

decoded_code = decode_jsfuck(jsfuck_code)
print(decoded_code)
