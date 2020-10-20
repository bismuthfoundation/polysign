"""
Demoes how to verify a generic tx, no a priori on its type.
"""

import json
import pytest
import sys

sys.path.append("../")
from polysign.signerfactory import SignerFactory


def check_generic_sig(name: str, file: str, verbose: bool=False):
    with open(file) as f:
        tx = json.load(f)
        # Caller is responsible for creating the bin buffer to check the sig against
        buffer = str(
            (
                tx["timestamp"],
                tx["address"],
                tx["recipient"],
                tx["amount"],
                tx["operation"],
                tx["openfield"],
            )
        ).encode("utf-8")
        if verbose:
            print(f"{name} buffer", buffer)

        SignerFactory.verify_bis_signature(
            tx["signature"], tx["public_key"], buffer, tx["address"]
        )
        if verbose:
            print(f"{name}: No Error")


def test_verify_rsa_signature1(verbose: bool=False):
    # Sample real rsa tx
    check_generic_sig("RSA 1", "./vectors/rsa_tx1.json", verbose)


def test_verify_rsa_signature2(verbose: bool=False):
    # Sample real rsa tx
    check_generic_sig("RSA 2", "./vectors/rsa_tx2.json", verbose)


def test_verify_rsa_fail_signature(verbose: bool=False):
    # Sample real rsa tx, with one byte changed, must raise
    with pytest.raises(ValueError) as execinfo:
        check_generic_sig("RSA", "./vectors/rsa_tx_fail.json", verbose)
        # The following may be too strong or need formal specs to make sure the message is right.
        assert str(execinfo.value) == "Bad Signature"


def test_verify_ecdsa_signature2(verbose: bool=False):
    # Sample fake rsa tx
    check_generic_sig("ECDSA 2", "./vectors/ecdsa_tx2.json", verbose)


def test_verify_ecdsa_fail_signature(verbose: bool=False):
    # Sample rsa tx, with one byte changed, must raise
    with pytest.raises(ValueError) as execinfo:
        check_generic_sig("ECDSA", "./vectors/ecdsa_tx_fail.json", verbose)
        assert str(execinfo.value) == "Bad Signature"


def test_verify_ed25519_signature2(verbose: bool=False):
    # Sample fake ed25519 tx
    check_generic_sig("ED25519 2", "./vectors/ed25519_tx2.json", verbose)


def test_verify_ed25519_fail_signature(verbose: bool=False):
    # Sample real ed25519 tx, with one byte changed, must raise
    with pytest.raises(ValueError) as execinfo:
        check_generic_sig("ed25519", "./vectors/ed25519_tx_fail.json", verbose)
        assert str(execinfo.value) == "Bad Signature"


if __name__ == "__main__":
    test_verify_rsa_signature1(True)
    test_verify_rsa_fail_signature(True)
    test_verify_ed25519_fail_signature(True)
