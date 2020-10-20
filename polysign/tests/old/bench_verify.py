
from time import time
from coincurve import verify_signature
import ed25519
from base64 import b64decode
from Cryptodome.Hash import SHA
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import PKCS1_v1_5
import nacl
import nacl.signing

NB = 1000

ECDSA = {
    "buffer": "('1559472321.00', 'Bis1SAk19HCWpDAThwFiaP9xA6zWjzsga7Hog', 'f6c0363ca1c5aa28cc584252e65a63998493ff0a5ec1bb16beda9bac', '0.63000000', '', 'fake_tx_info')",
    "signature": "MEQCIHu5eNOhmebPTxqHWEMsLJcvFa8i+8hMrsGVXt5xI7rmAiAwFbs3HSGnKiujcbbzRAkVmgTlbG2vU3kOyGe9YWTqfA==",
    "public_key": "A0l0a6ARznKt6nWOCSFZYiuqpQCfrKcq1DFnktgot3lq",
}

ED25519 = {
    "buffer": "('1557384490.32', 'Bis13AbAZwMeY1C5GuFuVuVKLSjr3RdKG63g4CEx6epwSbhpuDU3rj', 'f6c0363ca1c5aa28cc584252e65a63998493ff0a5ec1bb16beda9bac', '0.63443243', '', 'fake_tx_info')",
    "signature": "A9xXtvrwGUSM6k50OVJ9zmx7X+yYA8FGVxyNJ9FPvLYjWKYkJwLGT093XO1X2i8kSh92Q/JVpMQK1AlMaqgRBQ==",
    "public_key": "5YsUhytlWuyWCqIYr1PeXBpTOVWH+WEPnwSL7hfbaAo=",
}

RSA_ = {
    "buffer": "('1557384490.32', 'd35d8ddd4ded7074e5bf092cb716dd4d42d44a2c615115113a6f96dc', 'f6c0363ca1c5aa28cc584252e65a63998493ff0a5ec1bb16beda9bac', '0.63443243', '', 'fake_tx_info')",
    "signature": "iSds5K/vWHSjljBexucIiEWqO48nDK1PN27LvkgptKB4cCQ5EVUOLV8n4JoMjmWIDFs+xrJUwyLerVxcgtP0IHxajHPyfZP3WX9B0YT7bymXIPHWwpTBzDM3gT2GMyMr+GrUWKpwhN0T1nzHxvJ5EoEZQ5FvxD66bDFASZtrB7ABggsSaS4BXB27KQQexJWnQphaMWLdEhlFN1JQW+mlLlMijh+iM9ZFO1i0b2e2otzwAmB/rd+qblDymZsqVcIB72bUvMq/ZGLYGPy/2FbnYycOX1GzqYb0xIjBrKopFu2bBGnL1Fcsw84MHOEiu0XC1xx9wZLGIms902qr+SQky1XBU2DVR2oBPdMZcIRRe2WNUFVB7ybh8M7u8i3YLP4KutKpFgyg7uJbC33BzyzeK1KxIuvwjb9gVSRwjjDFg9GNwvtCHnBpff4ROyL+nPrH8/wRfxapRfCndE6w8WMn4eAofh80VjPnmUiGGZaCrH4lLlBEfF87efn/Cw+gOJCkimVHhNi6J+J2K2ynJbIbn4yUK93yXTRuSYeRj48HdbPZ1Ni3hyyvrPmnnec7AcKHA6TlrJOhUpW8DxAGU1hNazU/WYNt/WM37ofpO9M/mfKtpgyh0Dk0HCnFQfXFCQxQg5fCi8gfUNSJsZEaSR/aJQmgyHVRrWSV2Rw90ZjLDKE=",
    "public_key": "LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQ0lqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FnOEFNSUlDQ2dLQ0FnRUFuN2U5dTBIbjZhN3VmdUZDZ2lIcApmem8vWng2amdZb2RLeWZhTm5SS3JhNWsyYm9oVHB2cWRWdVkwRzZGTjNUUVFHbzRXWE5PdFV2c1BRYmQ5REJMCnozd3NyVTY0dWFNVUlNdUZHWnZYYjJuelZKeGlhY3V1S2ZQa01HM1E4RFk4WlhCSWFxNmNibzFBR3RPMy9qcTYKNXNuSm9kR0F5VUFuTGFnK21oSWdTZ3dPOXRqeEs4M3pSQXRTdW1EWnZWTmNzM2liMS9rcm5ydkZjcUFNb0Z6NQpJVlF1Wlh2MUpLYzlvTXRIUCsxak5rWU9rN3BjR0NxVDVXYVJ0LzRWSGI5dmdiQnB3SXVBY09qS0w5b1lVS3dKCkxFZDl3SmFHMWVGSEIrbkxqdmIzbmtVa2phTDdPTGFYMGdBYjNmajFEdUwyeFNSd0hRYVVZOTJlOHlPbXRXN0EKU3FPM2UralJadGtycVVGMkxMWjlucWsvUllTMWV5UWJSWC8xMTJsdnhpK3RVbStjbDNxZER3Y2dzZTA5OVJOZAo0NGlXYkZYaFcwVFRPZ3ptMXhnVmR5SFJib3k4dktoTnhHTFIxUFYwQmMvZm5aZ2RtNSs1YkhkNWZEc2Y4R2kvCmpNYnRreGFwY09MNFB6WW9MZWE4dGcxRmFYZTZSOHhzS1pRakdKNkFZNEg0Y3RzU1M4bkVGQ0pGNjJLWkRyTngKK1hFZ01XS0xvRDJrRVF1aWhqa2t2ZGJDb0t5RE5NbjQ4UExBc2dCQnl6ZHFRVkUxNE5KNklBQWtwdmovSXVwRQpKYnl5cXEzaGZiRUhKWnBXeUtjM2lVa0RibC9tK1BCdEdVYm43UDFEWWxWTGV4VDM4dldiN0tLeFg1TEREVUxkCnZqRnBQb3h4Y1QvcWxFbTQ2cDB4dk04Q0F3RUFBUT09Ci0tLS0tRU5EIFBVQkxJQyBLRVktLS0tLQ==",
}


def verify_ecdsa():
    sig = b64decode(ECDSA["signature"])
    buffer = ECDSA["buffer"].encode()
    public_key = b64decode(ECDSA["public_key"])
    for i in range(NB):
        valid = verify_signature(sig, buffer, public_key)
    return valid


def verify_ed25519():
    sig = b64decode(ED25519["signature"])
    buffer = ED25519["buffer"].encode()
    public_key = b64decode(ED25519["public_key"])
    verifying_key = ed25519.VerifyingKey(public_key)
    for i in range(NB):
        verifying_key.verify(sig, buffer)


def verify_ed25519_nacl():
    sig = b64decode(ED25519["signature"])
    buffer = ED25519["buffer"].encode()
    public_key = b64decode(ED25519["public_key"])

    vk = nacl.signing.VerifyKey(public_key)
    for i in range(NB):
        vk.verify(buffer, sig)


def verify_rsa():
    sig = b64decode(RSA_["signature"])
    buffer = RSA_["buffer"].encode()
    public_key = RSA_["public_key"]
    public_key_pem = b64decode(public_key).decode('utf-8')
    public_key_object = RSA.importKey(public_key_pem)
    verifier = PKCS1_v1_5.new(public_key_object)
    sha_hash = SHA.new(buffer)
    for i in range(NB):
        valid = verifier.verify(sha_hash, sig)
    return valid


def timer(func):
    start = time()
    func()
    delay = time() - start
    print(func, delay, f"{NB/delay:0.0f} tx/s")


if __name__ == "__main__":
    timer(verify_rsa)
    timer(verify_ecdsa)
    timer(verify_ed25519)
    timer(verify_ed25519_nacl)

"""
core i7

<function verify_rsa at 0x7fa9f02330d0> 1.3092164993286133 764 tx/s
<function verify_ecdsa at 0x7fa9f851ce18> 0.07944917678833008 12587 tx/s
<function verify_ed25519 at 0x7fa9f13e3620> 3.6701412200927734 272 tx/s
<function verify_ed25519_nacl at 0x7fa9f13e36a8> 0.09578156471252441 10440 tx/s

"""
