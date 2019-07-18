# Asymetric Crypto schemes comparison


| |RSA 4096 bits|ECDSA Secp256k1|ed25519|
|-|-------------|---------------|-------|
|Used by|Bismuth (pow, legacy)|Bitcoin, alts, Bismuth pos|Nyzo, LSK? XLM, XMR, ADA, XTZ|
|Safety| > 2030 for 3072 bits| = RSA 3248 bits | = RSA 3072 bits, < RSA 4096 bits|
|Maturity| Industry standard, very mature|  |  |
|Privkey len|   |  | 32 bytes |
|Pubkey len|   | 32 bytes | 32 bytes |
|Signature| Yes | Yes | Yes |
|Signature len|   | 64 bytes  | 64 bytes |
|Sig voodoo| ? | Yes | ? |
|Key creation time| High | Low | Very Low |
|Signature time| High | Low | Very Low |
|Verifying time| Low | High | Low (+batch) |
|I P| | | public domain|


https://www.ssl.com/article/comparing-ecdsa-vs-rsa/  
According to public research, RSA 2048-bit keys require 4098 qubits
(and 5.2 trillion Tofolli gates) to be defeated, whereas ECDSA 256-bit keys
require only 2330 qubits (and 126 billion Tofolli gates). Hence, RSA is more
expensive to break, using a theoretical quantum machine.

https://security.stackexchange.com/questions/50878/ecdsa-vs-ecdh-vs-ed25519-vs-curve25519
https://medium.com/risan/upgrade-your-ssh-key-to-ed25519-c6e8d60d3c54
