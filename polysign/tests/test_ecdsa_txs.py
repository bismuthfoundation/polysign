"""
Test precalc vector of ecdsa sigs
"""

import json
import base64
import pytest
import sys

sys.path.append("../")
from polysign.signerfactory import SignerFactory
from polysign.signer import SignerType


def test_ecdsa_txs(verbose: bool=False):
    signer = SignerFactory.from_private_key(
        "e5b42f3c3fe02e161d42ff4707a174a5715b2badc7d4d3aebbea9081bd9123d5",
        SignerType.ECDSA,
    )
    if verbose:
        print(signer.to_dict())
    assert signer.to_dict()["address"] == "Bis1SAk19HCWpDAThwFiaP9xA6zWjzsga7Hog"

    public_key_hex = signer.to_dict()["public_key"]
    public_key_net = base64.b64encode(bytes.fromhex(public_key_hex)).decode("utf-8")

    with open("./vectors/ecdsa_txs.json", "r") as f:
        txs = json.load(f)
        assert txs[0]["public_key"] == public_key_net
        for tx in txs:
            if verbose:
                print(f"Testing tx #{tx['id']}")
            buffer = tx['buffer'].encode()
            # Recalc sig from buffer
            signature = signer.sign_buffer_for_bis(buffer)
            # Make sure sig is same as before
            assert signature == tx["signature"]
            # Make sure it still verifies as well
            SignerFactory.verify_bis_signature(
                signature, public_key_net, buffer, "Bis1SAk19HCWpDAThwFiaP9xA6zWjzsga7Hog"
            )


if __name__ == "__main__":
    test_ecdsa_txs(True)
