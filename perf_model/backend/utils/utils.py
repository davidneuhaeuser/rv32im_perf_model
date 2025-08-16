import math
import struct


def set_bits_in_range(n, m):
    # Create a mask with bits set from n to m
    mask = ((1 << (m - n + 1)) - 1) << n

    # Set the bits in the original number
    return mask


def uint32_to_int32(x: int) -> int:
    """
    convert from a uint32 number to the int32 equivalent.
    only affects number > 2**31 - 1 as they represent
    negative values for int32
    """
    assert 0 <= x <= 2**32 - 1

    if x >= 2**31 - 1:
        return -(2**32) + x
    else:
        return x


def int32_to_uint32(x: int) -> int:
    """
    convert integers into their uint32
    equivalent; only affects negative values
    """
    assert (-(2**31)) <= x <= (2**31 - 1)

    return (2**32 + x) if x < 0 else x


def create_float32(sign: int, exp: int, mantissa: int) -> int:
    """
    create a float32 integer representation out of the individual
    bitgroups
    """
    assert sign == 1 or sign == 0, "invalid sign value"
    assert 0 <= math.log2(exp if exp != 0 else 1) < 8, "invalid exponent value"
    assert (
        0 <= math.log2(mantissa if mantissa != 0 else 1) < 23
    ), "invalid mantissa value"

    value = mantissa | exp << 23 | sign << 31

    return value


def degroup_as_float32(value: int) -> tuple[int, int, int]:
    """
    degroup and integer, representing a float32-value into
    its corresponding bitgroups
    """
    sign = (value & (1 << 31)) >> 31
    exp = (value & (0xFF << 23)) >> 23
    mant = value & (0x7FFFFF)

    return sign, exp, mant


def float32_to_int(value: float):
    """
    convert a float number in python to an integer
    which corresponds to the underlying stored bit-value

    does **not** perform a conversion of the same number
    """
    packed_value = struct.pack("f", value)
    int_value = struct.unpack("I", packed_value)[0]
    return int_value


def int_to_float32(value: bin):
    """
    convert an integer-representation of a float32-number
    (the integer with the same bits as the float32-number)
    into the according number in python code

    does **not** perform a conversion of the same number
    """
    packed_value = struct.pack("I", value)
    float_value = struct.unpack("f", packed_value)[0]
    return float_value
