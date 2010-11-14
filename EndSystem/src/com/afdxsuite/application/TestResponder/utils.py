

def h2i(value):
    if type(value) == str:
        return int(value.encode('hex'), 16)

def i2h(value):

    if type(value) == int:
        if value < 255:
            return "\\x%02X" % value
        else:
            val = "%04X" % value
            return "\\x%s\\x%s" % (val[0:2], val[2:4])
    else:
        value = "%04s" % value
        return "\\x%s\\x%s" % (value[0:2], value[2:4])

def hexarrayTointarray(hex_array):
    response = list()
    for hexval in hex_array:
        response.append(h2i(hexval))
    return response
