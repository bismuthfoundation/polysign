"""
Generates test vectors for ECDSA signatures, from given timestamp
"""

import json
import base64
import random
import sys
from time import time
from decimal import *

sys.path.append("../")
from polysign.signer import SignerType
from polysign.signerfactory import SignerFactory

TIMESTAMP = 1559472321.17


def quantize_two(value):
    value = Decimal(value)
    value = value.quantize(Decimal("0.00"))
    return value


def quantize_eight(value):
    value = Decimal(value)
    value = value.quantize(Decimal("0.00000000"))
    return value


def get_tx_vector(i: int, a_tx: dict) -> dict:
    tx = dict(a_tx)  # deep copy
    tx["timestamp"] = "%.2f" % quantize_two(tx["timestamp"])
    tx["amount"] = "%.8f" % quantize_eight(tx["amount"])
    vector = {"id": i, "tx": tx}
    # adjust and recreate the buffer
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
    vector["buffer"] = buffer.decode("utf-8")
    print("\nBuffer {}: {}".format(i, vector["buffer"]))
    # Sign the tx
    signature = signer.sign_buffer_for_bis(buffer)
    print("ECDSA Signature", signature)
    vector["signature"] = signature

    public_key_hex = signer.to_dict()["public_key"]
    public_key_net = base64.b64encode(bytes.fromhex(public_key_hex)).decode("utf-8")
    vector["public_key"] = public_key_net

    full_tx = [
        tx["timestamp"],
        tx["address"],
        tx["recipient"],
        tx["amount"],
        signature,
        public_key_net,
        tx["operation"],
        tx["openfield"],
    ]
    vector["websocket_command"] = '["mpinsert", [{}]]'.format(json.dumps(full_tx))
    print("websocket : {}".format(vector["websocket_command"]))
    SignerFactory.verify_bis_signature(
        signature, public_key_net, buffer, "Bis1SAk19HCWpDAThwFiaP9xA6zWjzsga7Hog"
    )
    return vector


if __name__ == "__main__":

    # sign the TX data with our ecdsa test address
    signer = SignerFactory.from_private_key(
        "e5b42f3c3fe02e161d42ff4707a174a5715b2badc7d4d3aebbea9081bd9123d5",
        SignerType.ECDSA,
    )
    print(signer.to_dict())
    assert signer.to_dict()["address"] == "Bis1SAk19HCWpDAThwFiaP9xA6zWjzsga7Hog"

    current_time = TIMESTAMP
    vectors = []
    tx = {
        "timestamp": int(current_time),  # 2 decimals will be added to conform.
        "address": "Bis1SAk19HCWpDAThwFiaP9xA6zWjzsga7Hog",
        "recipient": "f6c0363ca1c5aa28cc584252e65a63998493ff0a5ec1bb16beda9bac",
        "amount": "0.63",  # Decimal will be added
        "operation": "",
        "openfield": "fake_tx_info",
    }
    vectors.append(get_tx_vector(0, tx))

    random.seed(555)  # reproducible results
    tx["openfield"] = ""
    for i in range(10):
        tx["timestamp"] = current_time + i / 100
        tx["amount"] = random.randint(0, 1000) / 1000
        vectors.append(get_tx_vector(i + 1, tx))
    # print(vectors)
    with open("ecdsa_txs.json", "w") as f:
        json.dump(vectors, f, indent=2)
