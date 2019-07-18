"""
Basic tests
"""

import base58
import json
import sys

sys.path.append("../")
from polysign.signer import SignerType, SignerSubType
from polysign.signerfactory import SignerFactory

# Never to be used for real addresses - from https://en.bitcoin.it/wiki/BIP_0032_TestVectors
TEST_SEED = "e8f32e723decf4051aefac8e2c93c9c5b214313817cdb01a1494b917c8436b35"
"""
Identifier
     * (hex):       3442193e1bb70916e914552172cd4e2dbc9df811
     * (fpr):       0x3442193e
     * (main addr): 15mKKb2eos1hWa6tisdPwwDC1a5J1y9nma
   * Secret key
     * (hex):       e8f32e723decf4051aefac8e2c93c9c5b214313817cdb01a1494b917c8436b35
     * (wif):       L52XzL2cMkHxqxBXRyEpnPQZGUs3uKiL3R11XbAdHigRzDozKZeW
   * Public key
     * (hex):       0339a36013301597daef41fbe593a02cc513d0b55527ec2df1050e2e8ff49c85c2
"""

if __name__ == "__main__":
    # RSA Test
    with open("rsa1.json") as f:
        wallet = json.load(f)
    rsa_private_key = wallet["Private Key"]
    signer = SignerFactory.from_private_key(rsa_private_key, SignerType.RSA)
    # print(signer.to_json())
    assert signer.to_dict()["address"] == wallet["Address"]

    # BTC ECDSA Test - seed is in fact a 32 byte privkey (random, no constraint)
    signer = SignerFactory.from_seed(TEST_SEED, SignerType.BTC)
    print(signer)
    print(signer.to_dict())
    assert signer.to_dict()["address"] == "15mKKb2eos1hWa6tisdPwwDC1a5J1y9nma"

    # CRW Test - seed is in fact a 32 byte privkey (random, no constraint)

    # From https://gitlab.crown.tech/crown/crown-core/issues/210
    wif = "5KZT4KD9mFd45h44LkR2ibUdt5EMF15YBtBxuRtomWAFgsAa2wa"
    wifdecode = base58.b58decode(wif).hex()
    print("wifdecode", wifdecode)
    # 80e5b42f3c3fe02e161d42ff4707a174a5715b2badc7d4d3aebbea9081bd9123d566129939
    # 80 e5b42f3c3fe02e161d42ff4707a174a5715b2badc7d4d3aebbea9081bd9123d5 66129939
    # 1 byte network, 32 bytes PK, 4 bytes checksum
    # CRW seems to use the uncompressed pubaddress format, btc uses compressed one.
    # fits with https://crown.tech/paper_wallet/index.html
    pk = wifdecode[2:66]
    print("pk", pk)

    signer = SignerFactory.from_seed(pk, SignerType.CRW)
    print(signer.to_dict())
    assert signer.to_dict()["address"] == "CRWGg6VvaNe6zhQ46wuEBci8VerP4qVTw8qq"

    signer = SignerFactory.from_seed(pk, SignerType.ECDSA)
    print(signer.to_dict())
    assert signer.to_dict()["address"] == "Bis1SAk19HCWpDAThwFiaP9xA6zWjzsga7Hog"

    signer = SignerFactory.from_seed(
        pk, SignerType.ECDSA, subtype=SignerSubType.TESTNET_REGULAR
    )
    print(signer.to_dict())
    assert signer.to_dict()["address"] == "tBisH4YbEridY7Xw2Dv5sP727VA7tV2j5fTk7"
