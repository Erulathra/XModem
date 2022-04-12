def algebraic_check_sum(block: bytes):
    result = 0
    for i in block:
        result += i
    result = result % 256
    return result.to_bytes(1, 'big')


# Copied form StackOverflow https://stackoverflow.com/questions/53358646/how-to-calculate-this-crc-using-python
def crc_check_sum(block: bytes):
    lo = hi = 0xff
    mask = 0xff
    for new in block:
        new ^= lo
        new ^= (new << 4) & mask
        tmp = new >> 5
        lo = hi
        hi = new ^ tmp
        lo ^= (new << 3) & mask
        lo ^= new >> 4
    lo ^= mask
    hi ^= mask
    result = hi << 8 | lo
    return result.to_bytes(2, 'big')
