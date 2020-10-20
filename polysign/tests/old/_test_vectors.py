"""
Creates Bis and test addresses from BIP32 test vectors.
"""

import base58
import json
import sys

sys.path.append("../")
from polysign.signer import SignerType, SignerSubType
from polysign.signerfactory import SignerFactory

# Never to be used for real addresses - from https://en.bitcoin.it/wiki/BIP_0032_TestVectors

if __name__ == "__main__":
    # Test vector 1
    print("Test vector 1\n")
    with open("ecdsa_test1.json") as f:
        private_keys = json.load(f)
    for private_key in private_keys:
        print("Private Key  \n{}  ".format(private_key))
        signer = SignerFactory.from_seed(private_key, SignerType.BTC)
        print("BTC Address  \n{}  ".format(signer.to_dict()["address"]))
        signer = SignerFactory.from_seed(private_key, SignerType.ECDSA)
        print("BIS Address  \n{}  ".format(signer.to_dict()["address"]))
    # Test vector 2
    print("\nTest vector 2\n")
    with open("ecdsa_test2.json") as f:
        private_keys = json.load(f)
    for private_key in private_keys:
        print("Private Key  \n{}  ".format(private_key))
        signer = SignerFactory.from_seed(private_key, SignerType.BTC)
        print("BTC Address  \n{}  ".format(signer.to_dict()["address"]))
        signer = SignerFactory.from_seed(private_key, SignerType.ECDSA)
        print("BIS Address  \n{}  ".format(signer.to_dict()["address"]))
