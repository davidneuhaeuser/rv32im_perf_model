def int_to_int32(i: int):
    # out = 0
    i = i & ((1 << 32) - 1)
    # while i:
    #     if i % 2:
    #         out += 1
    #     out = out << 1
    #     i >> 1
    # return out
    return i


def int32_to_int(i: int):
    out = 0
    b31 = (i & (1 << 31)) >> 31
    i = i & ((1 << 31) - 1)
    out += i - b31 * (1 << 31)
    return out
