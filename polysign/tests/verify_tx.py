"""
Demoes how to verify a generic tx, no a priori on its type.
"""

import json
import sys

sys.path.append("../")
from polysign.signerfactory import SignerFactory

if __name__ == "__main__":
    # Sample real rsa tx
    with open("rsa_tx1.json") as f:
        rsa_tx = json.load(f)

    # Caller is responsible for creating the bin buffer to check the sig against
    buffer = str(
        (
            rsa_tx["timestamp"],
            rsa_tx["address"],
            rsa_tx["recipient"],
            rsa_tx["amount"],
            rsa_tx["operation"],
            rsa_tx["openfield"],
        )
    ).encode("utf-8")
    print("buffer", buffer)

    SignerFactory.verify_bis_signature(
        rsa_tx["signature"], rsa_tx["public_key"], buffer, rsa_tx["address"]
    )
    print("RSA: No Error")

    # Sample fake ecdsa tx
    with open("ecdsa_tx2.json") as f:
        ecdsa_tx = json.load(f)

    # Caller is responsible for creating the bin buffer to check the sig against
    buffer = str(
        (
            ecdsa_tx["timestamp"],
            ecdsa_tx["address"],
            ecdsa_tx["recipient"],
            ecdsa_tx["amount"],
            ecdsa_tx["operation"],
            ecdsa_tx["openfield"],
        )
    ).encode("utf-8")
    print("buffer", buffer)

    SignerFactory.verify_bis_signature(
        ecdsa_tx["signature"], ecdsa_tx["public_key"], buffer, ecdsa_tx["address"]
    )
    print("ECDSA: No Error")

    # Sample fake ed25519 tx
    with open("ed25519_tx2.json") as f:
        ecdsa_tx = json.load(f)

    # Caller is responsible for creating the bin buffer to check the sig against
    buffer = str(
        (
            ecdsa_tx["timestamp"],
            ecdsa_tx["address"],
            ecdsa_tx["recipient"],
            ecdsa_tx["amount"],
            ecdsa_tx["operation"],
            ecdsa_tx["openfield"],
        )
    ).encode("utf-8")
    print("buffer", buffer)

    SignerFactory.verify_bis_signature(
        ecdsa_tx["signature"], ecdsa_tx["public_key"], buffer, ecdsa_tx["address"]
    )
    print("ED25519: No Error")
