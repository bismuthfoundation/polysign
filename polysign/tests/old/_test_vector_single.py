"""
Creates Bis pubkey and address from pk
"""

import base58
import base64
import json
import sys

sys.path.append("../")
from polysign.signer import SignerType, SignerSubType
from polysign.signerfactory import SignerFactory

# Never to be used for real addresses - from https://en.bitcoin.it/wiki/BIP_0032_TestVectors

PK = "e5b42f3c3fe02e161d42ff4707a174a5715b2badc7d4d3aebbea9081bd9123d5"
PK = "C775E7B757EDE630CD0AA1113BD102661AB38829CA52A6422AB782862F268646"

if __name__ == "__main__":
    # Test vector 1
    print("Test vector {}\n".format(PK))
    signer = SignerFactory.from_private_key(
        PK,
        SignerType.ECDSA,
    )
    print(signer.to_dict())
    print(base64.b64encode(bytes.fromhex(signer.to_dict()["public_key"])).decode('utf-8'))
    # assert signer.to_dict()["address"] == "Bis1SAk19HCWpDAThwFiaP9xA6zWjzsga7Hog"

    # print(signer.public_key_to_address(signer.to_dict()["public_key"]))

    """
    Test vector e5b42f3c3fe02e161d42ff4707a174a5715b2badc7d4d3aebbea9081bd9123d5

    {'address': 'Bis1SAk19HCWpDAThwFiaP9xA6zWjzsga7Hog', 
    'private_key': 'e5b42f3c3fe02e161d42ff4707a174a5715b2badc7d4d3aebbea9081bd9123d5', 
    'public_key': '0349746ba011ce72adea758e092159622baaa5009faca72ad4316792d828b7796a', 
    'compressed': True, 'type': 'ECDSA', 'sub_type': 'MAINNET_REGULAR'}
    pubkey b64: A0l0a6ARznKt6nWOCSFZYiuqpQCfrKcq1DFnktgot3lq
    
    prefix, id, checksum for address
    b'OT[' b']|\x8c\xc1\x1e/_\x00\xaf\x86o=G\xe0i\xe6H\xc4J\xc3' b'\x06\xb0\xe0F'
    4f545b 5d7c8cc11e2f5f00af866f3d47e069e648c44ac3 06b0e046

    """
