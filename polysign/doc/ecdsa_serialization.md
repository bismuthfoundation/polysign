# Bismuth ECDSA Addresses serialization

Follows bitcoin format.  
The individual steps are described here only for fine debug if needed. 


## Identifier

To get the identifier, you RIPEMD-160(SHA256()) hash a ECDSA public key derived from your 256-bit ECDSA private key.

## Version bytes

Add a address version bytes in front of the Identifier.  
The version bytes used by Bismuth are:

- MAINNET_REGULAR: 0x4f545b
- MAINNET_MULTISIG: 0x4f54c8
- TESTNET_REGULAR: 0x017ab685
- TESTNET_MULTISIG: 0x0146eba5

> Only MAINNET_REGULAR is supported atm, both on mainnnet and testnet.

## Checksum

Version is concatenated with Identifier, then sha256 hashed twice.
 
SHA256(SHA256(version . hash))

The first four bytes are the checksum

## Address as string

The address string to be used is the base58 encoded version of

Version . Identifier . Checksum 

## Reference

https://bitcoin.org/en/developer-reference#address-conversion
