"""
Test 100 random sigs of every scheme
"""

import json
import base64
import sys
import random

sys.path.append("../")
from polysign.signerfactory import SignerFactory
from polysign.signer import SignerType

SEED = "This has to be reproducible"


def generic_test(signer_type: SignerType.ECDSA, verbose: bool=False):
    if verbose:
        print("Type", signer_type)
    random.seed(SEED)
    for i in range(100):
        seed = hex(random.getrandbits(32 * 8))[2:]
        if verbose:
            # We can have leading zeros that get discarded. In that case, the seed will be shorter
            # and the lig will use it as a random seed to regenerate a full 32 bytes seed.
            # left as is, not filling here.
            print("seed", seed, len(seed))
        signer = SignerFactory.from_seed(seed, signer_type)
        signer_dict = signer.to_dict()
        if verbose:
            print(signer_dict)
        public_key_hex = signer.to_dict()["public_key"]
        public_key_net = base64.b64encode(bytes.fromhex(public_key_hex)).decode("utf-8")

        buffer = hex(random.getrandbits(64 * 8)).encode()
        signature = signer.sign_buffer_for_bis(buffer)
        SignerFactory.verify_bis_signature(
            signature, public_key_net, buffer, signer_dict["address"]
        )


def test_100_rsa(verbose: bool=False):
    # This is a complex issue. We could do it, but this is not safe enough for crypto.
    # do it for tests? other tests vectors should be enough for RSA.
    if verbose:
        print("RSA impl by pycryptodome does not support seeded key gen.")
    pass


def test_100_ecdsa(verbose: bool=False):
    generic_test(SignerType.ECDSA, verbose=verbose)


def test_100_ed25519(verbose: bool=False):
    generic_test(SignerType.ED25519, verbose=verbose)


if __name__ == "__main__":
    test_100_ecdsa(True)
    test_100_ed25519(True)
