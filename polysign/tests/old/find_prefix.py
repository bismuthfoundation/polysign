#!/usr/bin/env python3

from math import log, ceil
import sys


# lookup tables to convert integers in the range [0, 58) to base-58 digits and back
int_to_b58_digit = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
b58_digit_to_int = {b58: i for i, b58 in enumerate(int_to_b58_digit)}


# convert a (long) integer to its base-58 representation string
def int_to_base58_str(int_rep):
    base58_str = ""
    while int_rep:
        int_rep, remainder = divmod(int_rep, 58)
        base58_str = int_to_b58_digit[remainder] + base58_str
    return base58_str


def prepended_bytes(prepended_b58_digits, b256_digit_count):

    # ones are a special case in base58check format;
    # count and remove them, they are added back in later
    ones = 0
    for b58 in prepended_b58_digits:
        if b58 != "1":
            break
        ones += 1
        prepended_b58_digits = prepended_b58_digits[1:]
    if not prepended_b58_digits:  # if they're all 1's
        return ones * b"\0"

    # calc the # of base58 digits required for b256_digit_count bytes of "real" data
    # (not including the prepended base58 digits)
    b58_digit_count = ceil(b256_digit_count * log(256) / log(58))

    do_overflow_check = True
    while True:
        # calc the minimum integral value which starts with the desired digits in base-58
        min_int = 0
        for b58 in prepended_b58_digits:
            min_int *= 58
            min_int += b58_digit_to_int[b58]
        #
        # left-shift (mult. by a power of 58) to be just left of the "real" base-58 data
        min_int *= 58 ** b58_digit_count

        # uncomment to sanity-check that min_int is correct
        # print(" min_int:", ones * '1' + int_to_base58_str(min_int))

        # right-shift by multiples of 8 bits (base-256) to retrieve only the
        # most-significant bytes which are to the left of the "real" base-256 data
        min_int >>= b256_digit_count * 8
        # right-shifing effectively rounds min_int down, but we
        # need it rounded up, so add one to round it up instead
        min_int += 1

        # because min_int has been rounded up above, it's possible that adding it to "real"
        # data could cause an overflow in base-58 making the prepended_b58_digits increment
        # by one; if this could happen, left-shift prepended_b58_digits and repeat
        if do_overflow_check:
            max_real_data_int = (1 << b256_digit_count * 8) - 1
            max_base58_str = int_to_base58_str(
                (min_int << b256_digit_count * 8) + max_real_data_int
            )
            if not max_base58_str.startswith(prepended_b58_digits):
                prepended_b58_digits += "1"
                do_overflow_check = (
                    False
                )  # it doesn't matter if the '1' appended above overflows to '2'

                # uncomment to confirm that the max possible value
                # wouldn't have the desired prepended base-58 digits
                # print("overflow:", ones * '1' + max_base58_str)

                continue

        # prepend any ones according to base58check rules, and convert min_int to a byte string
        return ones * b"\0" + min_int.to_bytes(
            length=(min_int.bit_length() + 7) // 8, byteorder="big"
        )


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(
            "usage: {} <STRING-TO-PREPEND> <DATA-BYTE-LEN (excluding 4-byte checksum)>".format(
                sys.argv[0]
            )
        )

    result = prepended_bytes(
        sys.argv[1], int(sys.argv[2]) + 4
    )  # add 4 for the checksum
    print(", ".join("{:#04x}".format(i) for i in result))

    """
    ECDSA (len 20 bytes + 4)
    Regular add
    Bis1    0x4f, 0x54, 0x5b
    Multisig/script
    Bism    0x4f, 0x54, 0xc8
    
    tesnet
    tBis    0x01, 0x7a, 0xb6, 0x85
    testnet multisig
    mBis    0x01, 0x46, 0xeb, 0xa5
    
    
    ED25519 (len 32 bytes + 4)
    Regular add
    Bis1    0x03, 0xb8, 0x6c, 0xf3 //  0x02, 0x07, 0x1a, 0xb5
    Multisig/script
    Bism    0x03, 0xb8, 0x72, 0x14
    
    tesnet
    tBis    0x11, 0xc2, 0xce, 0x7c
    testnet multisig
    mBis    0x0f, 0x54, 0xfd, 0x2d
        
    """
