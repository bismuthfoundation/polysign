"""
Test - Generate vanity ecdsa address
"""

import sys
from os import urandom
from time import time
from secrets import token_hex
from multiprocessing import Process

sys.path.append("../")
from polysign.signer import SignerType, SignerSubType
from polysign.signerfactory import SignerFactory

# TODO: click would be a better choice than tornado. I'm lazy.
from tornado.options import define, options


define("processes", default=4, help="Process count to start (default 4)", type=int)
define("string", help="String to find in the address", type=str)
define("case", default=False, help="be case sensitive (default false)", type=bool)
define("max", default=100, help="max hit per process (default 100)", type=int)

alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def find_it(string: str):
    found = 0
    while True:
        # pk = urandom(32).hex()
        pk = token_hex(32)  # +50% time, but supposed to be cryptographically secure
        signer = SignerFactory.from_seed(pk, signer_type, subtype=subtype)
        address = signer._address
        if not options.case:
            address = address.lower()
        if string in address:
            print(signer._address, pk)
            found += 1
            if found > options.max:
                return


if __name__ == "__main__":
    options.parse_command_line()
    # TODO: could be given on command line
    signer_type = SignerType.ECDSA
    subtype = SignerSubType.MAINNET_REGULAR

    print("Looking for '{}'".format(options.string))
    if not options.case:
        options.string = options.string.lower()
        print("Case InsEnsITivE")
    else:
        print("Case sensitive")
    # Check charset is ok ? not easy with case insensitive...

    processes = []
    for i in range(options.processes):
        p = Process(target=find_it, args=(options.string,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
    # find_it(options.string)
    """
    start = time()
    for i in range(100):
        # pk = urandom(32).hex()
        pk = token_hex(32)  # +50% time, but supposed to be cryptographically secure
        signer = SignerFactory.from_seed(pk, signer_type, subtype=subtype)
        # print("  ", signer.to_dict())
        print(signer.to_dict()["address"], pk)
    print()
    print(time() - start)
    """
