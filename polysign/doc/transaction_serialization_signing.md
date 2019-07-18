# Bismuth transactions Serialization and signing

This scheme is valid whatever the signing algo is (RSA, ECDSA, ED25519) 

## Global Flow

- get the transaction properties
- assemble the buffer to be signed
- sign the buffer, add pubkey and signature to transaction properties
- send the mempool insert message with signed tx 

## Bismuth transaction properties

All strings are utf-8 encoded.

A Bismuth Transaction (buffer to be signed) is composed of:
   - timestamp : transaction timestamp, float with 2 fixed decimals, encoded as string 
   - address : string, sender address, max 56 chars
   - recipient : string, sender address, max 56 chars
   - amount : BIS amount, float with fixed 8 decimals, encoded as string
   - operation : string, optional, max 30 chars
   - openfield : string, optional, max 100000 chars

## Buffer to sign

The buffer to be signed is a string representation of the transaction above, as a tuple.  
It's format is very precise, spaces and decimals included.

```
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
```

> For a clean Js implementation of that serialization, see https://github.com/gabidi/bismuth-js-crypto/blob/3291997c1bf89f71981624be682e0fa1c0dc9653/src/sign.js#L17
   
ecdsa_txs.json contains several test vectors based upon test private key "e5b42f3c3fe02e161d42ff4707a174a5715b2badc7d4d3aebbea9081bd9123d5" which gives Bis Address Bis1SAk19HCWpDAThwFiaP9xA6zWjzsga7Hog  
with matching buffers 

make_ecdsa_txs.py regenerates a set of vectors from current date.
   
## Full transaction to send

A Full Bismuth Transaction (list to send to network) has extra info, signature and pubkey

   - timestamp : transaction timestamp, float with 2 fixed decimals, encoded as string 
   - address : string, sender address, max 56 chars
   - recipient : string, sender address, max 56 chars
   - amount : BIS amount, float with fixed 8 decimals, encoded as string
   - signature : the transaction signature, base64 encoded (string), max 684 chars
   - pubkey : the sender address pubkey, base64 encoded (string), max 1068 chars
   - operation : string, optional, max 30 chars
   - openfield : string, optional, max 100000 chars
   
ecdsa_txs.json contains the signatures and pubkeys also, as string   
 
## Sending the transaction

Command is sent over websocket, as a json array [command, options]
options begin an array, even if there is one option only.

Javascript: see https://github.com/gabidi/bismuth-js-sdk/blob/master/BismuthWSSdk.ts  
use the insertMemPoolTxn method

https://github.com/gabidi/bismuth-web-wallet can be useful also.
(only the key and signing changes, transaction assembling, signing and sending works the same)

ecdsa_txs.json also contains the matching websocket commands, as string.   

# Sample from ecdsa_txs.json

```
 "tx": {
      "timestamp": "1559472321.00",
      "address": "Bis1SAk19HCWpDAThwFiaP9xA6zWjzsga7Hog",
      "recipient": "f6c0363ca1c5aa28cc584252e65a63998493ff0a5ec1bb16beda9bac",
      "amount": "0.63000000",
      "operation": "",
      "openfield": "fake_tx_info"
    },
    "buffer": "('1559472321.00', 'Bis1SAk19HCWpDAThwFiaP9xA6zWjzsga7Hog', 'f6c0363ca1c5aa28cc584252e65a63998493ff0a5ec1bb16beda9bac', '0.63000000', '', 'fake_tx_info')",
    "signature": "MEQCIHu5eNOhmebPTxqHWEMsLJcvFa8i+8hMrsGVXt5xI7rmAiAwFbs3HSGnKiujcbbzRAkVmgTlbG2vU3kOyGe9YWTqfA==",
    "public_key": "A0l0a6ARznKt6nWOCSFZYiuqpQCfrKcq1DFnktgot3lq",
    "websocket_command": "[\"mpinsert\", [[\"1559472321.00\", \"Bis1SAk19HCWpDAThwFiaP9xA6zWjzsga7Hog\", \"f6c0363ca1c5aa28cc584252e65a63998493ff0a5ec1bb16beda9bac\", \"0.63000000\", \"MEQCIHu5eNOhmebPTxqHWEMsLJcvFa8i+8hMrsGVXt5xI7rmAiAwFbs3HSGnKiujcbbzRAkVmgTlbG2vU3kOyGe9YWTqfA==\", \"A0l0a6ARznKt6nWOCSFZYiuqpQCfrKcq1DFnktgot3lq\", \"\", \"fake_tx_info\"]]]"
```
