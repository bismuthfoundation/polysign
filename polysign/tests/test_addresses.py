"""
Tests address generation from private keys, with very various schemes including other existing cryptos test vectors
"""

import json
import base58
import pytest
import sys

sys.path.append("../")
from polysign.signer import SignerType, SignerSubType
from polysign.signerfactory import SignerFactory


# Never to be used for real addresses - from https://en.bitcoin.it/wiki/BIP_0032_TestVectors
TEST_SEED = "e8f32e723decf4051aefac8e2c93c9c5b214313817cdb01a1494b917c8436b35"

TEST_PK = "e5b42f3c3fe02e161d42ff4707a174a5715b2badc7d4d3aebbea9081bd9123d5"


def test_rsa_address1(verbose: bool=False):
    # RSA Test
    with open("./vectors/rsa_wallet1.json") as f:
        wallet = json.load(f)
    rsa_private_key = wallet["Private Key"]
    signer = SignerFactory.from_private_key(rsa_private_key, SignerType.RSA)
    if verbose:
        print(signer.to_json())
    signer_dict = signer.to_dict()
    assert signer_dict["address"] == wallet["Address"]
    assert signer_dict["public_key"] == "-----BEGIN PUBLIC KEY-----\n" \
                                        "MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAn7e9u0Hn6a7ufuFCgiHp\n" \
                                        "fzo/Zx6jgYodKyfaNnRKra5k2bohTpvqdVuY0G6FN3TQQGo4WXNOtUvsPQbd9DBL\n" \
                                        "z3wsrU64uaMUIMuFGZvXb2nzVJxiacuuKfPkMG3Q8DY8ZXBIaq6cbo1AGtO3/jq6\n" \
                                        "5snJodGAyUAnLag+mhIgSgwO9tjxK83zRAtSumDZvVNcs3ib1/krnrvFcqAMoFz5\n" \
                                        "IVQuZXv1JKc9oMtHP+1jNkYOk7pcGCqT5WaRt/4VHb9vgbBpwIuAcOjKL9oYUKwJ\n" \
                                        "LEd9wJaG1eFHB+nLjvb3nkUkjaL7OLaX0gAb3fj1DuL2xSRwHQaUY92e8yOmtW7A\n" \
                                        "SqO3e+jRZtkrqUF2LLZ9nqk/RYS1eyQbRX/112lvxi+tUm+cl3qdDwcgse099RNd\n" \
                                        "44iWbFXhW0TTOgzm1xgVdyHRboy8vKhNxGLR1PV0Bc/fnZgdm5+5bHd5fDsf8Gi/\n" \
                                        "jMbtkxapcOL4PzYoLea8tg1FaXe6R8xsKZQjGJ6AY4H4ctsSS8nEFCJF62KZDrNx\n" \
                                        "+XEgMWKLoD2kEQuihjkkvdbCoKyDNMn48PLAsgBByzdqQVE14NJ6IAAkpvj/IupE\n" \
                                        "Jbyyqq3hfbEHJZpWyKc3iUkDbl/m+PBtGUbn7P1DYlVLexT38vWb7KKxX5LDDULd\n" \
                                        "vjFpPoxxcT/qlEm46p0xvM8CAwEAAQ==\n" \
                                        "-----END PUBLIC KEY-----"
    assert signer_dict["type"] == "RSA"
    assert signer_dict["sub_type"] == "MAINNET_REGULAR"
    assert signer_dict["private_key"] == rsa_private_key


def test_btc_address(verbose: bool = False):
    # BTC ECDSA Test - seed is in fact a 32 byte privkey (random, no constraint)
    signer = SignerFactory.from_seed(TEST_SEED, SignerType.BTC)
    signer_dict = signer.to_dict()
    if verbose:
        print(signer_dict)
    assert signer.to_dict()["address"] == "15mKKb2eos1hWa6tisdPwwDC1a5J1y9nma"
    assert signer_dict["public_key"] == "0339a36013301597daef41fbe593a02cc513d0b55527ec2df1050e2e8ff49c85c2"
    assert signer_dict["private_key"] == "e8f32e723decf4051aefac8e2c93c9c5b214313817cdb01a1494b917c8436b35"
    assert signer_dict["sub_type"] == "MAINNET_REGULAR"
    assert signer_dict["type"] == "ECDSA"


def test_crw_address(verbose: bool = False):
    # From https://gitlab.crown.tech/crown/crown-core/issues/210
    wif = "5KZT4KD9mFd45h44LkR2ibUdt5EMF15YBtBxuRtomWAFgsAa2wa"
    wifdecode = base58.b58decode(wif).hex()
    if verbose:
        print("wifdecode", wifdecode)
    # 80e5b42f3c3fe02e161d42ff4707a174a5715b2badc7d4d3aebbea9081bd9123d566129939
    # 80 e5b42f3c3fe02e161d42ff4707a174a5715b2badc7d4d3aebbea9081bd9123d5 66129939
    # 1 byte network, 32 bytes PK, 4 bytes checksum
    # CRW seems to use the uncompressed pubaddress format, btc uses compressed one.
    # fits with https://crown.tech/paper_wallet/index.html
    pk = wifdecode[2:66]
    if verbose:
        print("pk", pk)
    signer = SignerFactory.from_seed(pk, SignerType.CRW)
    signer_dict = signer.to_dict()
    if verbose:
        print(signer_dict)
    assert signer.to_dict()["address"] == "CRWGg6VvaNe6zhQ46wuEBci8VerP4qVTw8qq"
    assert signer_dict["public_key"] == "0449746ba011ce72adea758e092159622baaa5009faca72ad4316792d828b7796a738dbf2ce8386d9b5aa1275c70d160e774dc175f41e005311616bf13942f57ad"
    assert signer_dict["private_key"] == "e5b42f3c3fe02e161d42ff4707a174a5715b2badc7d4d3aebbea9081bd9123d5"
    assert signer_dict["sub_type"] == "MAINNET_REGULAR"
    assert signer_dict["type"] == "ECDSA"
    assert signer_dict["compressed"] == False


def test_bis_mainnet(verbose: bool = False):
    signer = SignerFactory.from_seed(TEST_PK, SignerType.ECDSA)
    signer_dict = signer.to_dict()
    if verbose:
        print(signer_dict)
    assert signer.to_dict()["address"] == "Bis1SAk19HCWpDAThwFiaP9xA6zWjzsga7Hog"
    assert signer_dict["public_key"] == "0349746ba011ce72adea758e092159622baaa5009faca72ad4316792d828b7796a"
    assert signer_dict["private_key"] == "e5b42f3c3fe02e161d42ff4707a174a5715b2badc7d4d3aebbea9081bd9123d5"
    assert signer_dict["sub_type"] == "MAINNET_REGULAR"
    assert signer_dict["type"] == "ECDSA"
    assert signer_dict["compressed"] == True


def test_bis_testnet(verbose: bool = False):
    signer = SignerFactory.from_seed(TEST_PK, SignerType.ECDSA, subtype=SignerSubType.TESTNET_REGULAR)
    signer_dict = signer.to_dict()
    if verbose:
        print(signer_dict)
    assert signer.to_dict()["address"] == "tBisH4YbEridY7Xw2Dv5sP727VA7tV2j5fTk7"
    assert signer_dict["public_key"] == "0349746ba011ce72adea758e092159622baaa5009faca72ad4316792d828b7796a"
    assert signer_dict["private_key"] == "e5b42f3c3fe02e161d42ff4707a174a5715b2badc7d4d3aebbea9081bd9123d5"
    assert signer_dict["sub_type"] == "TESTNET_REGULAR"
    assert signer_dict["type"] == "ECDSA"
    assert signer_dict["compressed"] == True


if __name__ == "__main__":
    test_rsa_address1(True)
    test_btc_address(True)
    test_crw_address(True)
    test_bis_mainnet(True)
    test_bis_testnet(True)
