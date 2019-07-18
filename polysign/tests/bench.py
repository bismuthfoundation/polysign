import base58
import base64
from time import time

NB = 100000

SIGNATURE_58 = "381yXZ8CZPvDn3WWyfCWYxqpGnbGQVxfRcUdpu6LbjycoTpYckPEoc6aorS5RiEZPh5Z6sm2BDLZPpHQ5FNhmH1SDYDiSZ9j"
SIGNATURE_HEX = base58.b58decode(SIGNATURE_58).hex()
SIGNATURE_64 = base64.b64encode(base58.b58decode(SIGNATURE_58)).decode("utf-8")

print(SIGNATURE_58, SIGNATURE_HEX, SIGNATURE_64)


def decode_58():
    for i in range(NB):
        dec = base58.b58decode(SIGNATURE_58)
    return dec


def decode_64():
    for i in range(NB):
        dec = base64.b64decode(SIGNATURE_64)
    return dec


def decode_hex():
    for i in range(NB):
        dec = bytes.fromhex(SIGNATURE_HEX)
    return dec


def timer(function):
    start = time()
    function()
    print(function, time() - start)


if __name__ == "__main__":
    timer(decode_58)
    timer(decode_64)
    timer(decode_hex)
