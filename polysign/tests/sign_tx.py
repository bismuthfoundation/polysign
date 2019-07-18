"""
Demoes how to sign a generic tx
"""

import json
import base64
import sys

sys.path.append("../")
from polysign.signer import SignerType
from polysign.signerfactory import SignerFactory


if __name__ == "__main__":
    # Load privkey from our test rsa1.json (do not use IRL!)
    with open("rsa1.json") as f:
        wallet = json.load(f)
    rsa_private_key = wallet["Private Key"]

    # Create a signer. Safer if we can force the Type, but should be ok in the end with just key
    signer = SignerFactory.from_private_key(rsa_private_key, SignerType.RSA)

    # Load our fake tx params
    with open("rsa_tx2.json") as f:
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

    # Sign the tx
    signature = signer.sign_buffer_for_bis(buffer)
    print("RSA Signature", signature)

    # Extra: recheck (useless, for test only) - Raises if Error
    SignerFactory.verify_bis_signature(
        rsa_tx["signature"], rsa_tx["public_key"], buffer, rsa_tx["address"]
    )
    print("No Error")

    # =================================================================================

    # Now sign the same TX data with our ecdsa test address
    # Could as well be loaded from a wallet, no matter.
    signer = SignerFactory.from_private_key(
        "e5b42f3c3fe02e161d42ff4707a174a5715b2badc7d4d3aebbea9081bd9123d5",
        SignerType.ECDSA,
    )
    print(signer.to_dict())
    assert signer.to_dict()["address"] == "Bis1SAk19HCWpDAThwFiaP9xA6zWjzsga7Hog"

    # adjust and recreate the buffer
    rsa_tx["address"] = "Bis1SAk19HCWpDAThwFiaP9xA6zWjzsga7Hog"
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
    # Sign the tx
    signature = signer.sign_buffer_for_bis(buffer)
    print("ECDSA Signature", signature)

    public_key_hex = signer.to_dict()["public_key"]
    public_key_net = base64.b64encode(bytes.fromhex(public_key_hex)).decode("utf-8")
    print(public_key_hex, public_key_net)

    SignerFactory.verify_bis_signature(
        signature, public_key_net, buffer, "Bis1SAk19HCWpDAThwFiaP9xA6zWjzsga7Hog"
    )
    print("No Error")

    # =================================================================================

    # Now sign the same TX data with our ed25519 test address
    # Could as well be loaded from a wallet, no matter.
    signer = SignerFactory.from_private_key(
        "e5b42f3c3fe02e161d42ff4707a174a5715b2badc7d4d3aebbea9081bd9123d5",
        SignerType.ED25519,
    )
    print(signer.to_dict())
    assert (
        signer.to_dict()["address"]
        == "Bis13AbAZwMeY1C5GuFuVuVKLSjr3RdKG63g4CEx6epwSbhpuDU3rj"
    )

    # adjust and recreate the buffer
    rsa_tx["address"] = "Bis13AbAZwMeY1C5GuFuVuVKLSjr3RdKG63g4CEx6epwSbhpuDU3rj"
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
    # Sign the tx
    signature = signer.sign_buffer_for_bis(buffer)
    print("ED25519 Signature", signature)

    public_key_hex = signer.to_dict()["public_key"]
    public_key_net = base64.b64encode(bytes.fromhex(public_key_hex)).decode("utf-8")
    print(public_key_hex, public_key_net)

    SignerFactory.verify_bis_signature(
        signature,
        public_key_net,
        buffer,
        "Bis13AbAZwMeY1C5GuFuVuVKLSjr3RdKG63g4CEx6epwSbhpuDU3rj",
    )
    print("No Error")
