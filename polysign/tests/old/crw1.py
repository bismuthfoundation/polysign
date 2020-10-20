import base58
from hashlib import sha256

ADDRESS_VERSION = b"\x01\x75\x07"

old_addr = "15bj2HB2UbmjEZgXyEW4M8MhUL5TXGCN8L"
decoded = base58.b58decode(old_addr).hex()
print("decoded", decoded)
# 00 3271b95d0a3af5b1095502895a422a907b3084129e808f85
# 80 3271b95d0a3af5b1095502895a422a907b308412 9e808f85
# 1 byte network, 20 bytes PubK, 4 bytes checksum
pubk = decoded[2:42]
print("pubk", pubk)

vh160 = ADDRESS_VERSION + bytes.fromhex(pubk)
chk = sha256(sha256(vh160).digest()).digest()[:4]
print("chk", chk)
new = base58.b58encode(vh160 + chk).decode("utf-8")
print("new", new)
assert new == "CRWGZiLqSUbCTWkm3ABp5qpXdun2h8DJCKYF"
