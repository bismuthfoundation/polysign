"""
Test - Generate several random ECDSA Bis addresses of different types
"""

import sys
from os import urandom

sys.path.append("../")
from polysign.signer import SignerType, SignerSubType
from polysign.signerfactory import SignerFactory


if __name__ == "__main__":
    for signer_type in [SignerType.ECDSA, SignerType.ED25519]:
        print(signer_type.name)
        for subtype in SignerSubType:
            print(" -", subtype.name)
            for i in range(10):
                pk = urandom(32).hex()
                signer = SignerFactory.from_seed(pk, signer_type, subtype=subtype)
                print("  ", signer.to_dict())
                print(len(signer.to_dict()["address"]))
