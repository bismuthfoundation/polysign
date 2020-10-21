"""
Check test vectors with all bis addresses schemes
"""

import json
import pytest
import sys

sys.path.append("../")
from polysign.signerfactory import SignerFactory
from polysign.signer import SignerType, SignerSubType


def test_bis_vectors(verbose: bool=False):
    with open("./vectors/bis_vectors.json") as f:
        wallets = json.load(f)
    for wallet in wallets:
        private_key = wallet["private_key"]
        signer_type = SignerType.RSA
        if wallet["type"] == "ECDSA":
            signer_type = SignerType.ECDSA
        if wallet["type"] == "ED25519":
            signer_type = SignerType.ED25519
        signer_subtype = SignerSubType.MAINNET_REGULAR
        if wallet["sub_type"] == "TESTNET_REGULAR":
            signer_subtype = SignerSubType.TESTNET_REGULAR
        signer = SignerFactory.from_private_key(private_key, signer_type=signer_type, subtype=signer_subtype)
        signer_dict = signer.to_dict()
        if verbose:
            print(signer_dict)
        assert signer_dict["address"] == wallet["address"]
        assert signer_dict["public_key"] == wallet["public_key"]
        assert signer_dict["type"] == wallet["type"]
        assert signer_dict["sub_type"] == wallet["sub_type"]
        # In case privkey was submitted as uppercase
        assert signer_dict["private_key"].lower() == wallet["private_key"].lower()


if __name__ == "__main__":
    test_bis_vectors(True)
