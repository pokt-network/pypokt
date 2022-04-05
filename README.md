# pypocket

Python Client SDK for Pocket Network

## Installation (Development)

```sh
git clone git@github.com:pokt-foundation/pypocket.git
cd pypocket
pip install -e .
```

## Requirements

An Pocket RPC URL Can be acquired through either:

1. Access to a Pocket Node with RPC
2. An app endpoint from [the Portal](https://portal.pokt.network/)

## Usage

**Pocket RPC:**

- [x] Pocket RPC `/query`
- [] Pocket RPC `/client`
- [] Pocket DB

**Wallet:**

- [x] Create Account (PPK file/Private Key)
- [x] Import Account (from PPK/Private Key)
- [x] Sign message with account
- [x] Verify signed message
- [] Create and sign transactions from account
- [] Create and sign multisig transactions from account

**Portal RPC:**

- [] pocket RPC provider
- [] web3 providers
- [] figure out other types

### Pocket RPC `/query`

```python
from pokt import PoktRPCDataProvider

rpc_url = "https://mainnet.pokt.network/v1/lb/<PortalID>"
pokt_rpc = PoktRPCDataProvider(rpc_url)

height = pokt_rpc.get_height()
supported_chains = pokt_rpc.get_supported_chains()
supply = pokt_rpc.get_supply()
```

### Create Account

```python
from pokt import create_new_ppk

ppk = create_new_ppk("super-secret-password")
```

### Import Account

```python
from pokt import PPK

ppk = PPK.from_file("/path/to/keyfile.json")
```

### Sign a Message

```python
from pokt import PPK, unlock_ppk

ppk = PPK.from_file("/path/to/keyfile.json")

unlocked = unlock_ppk(ppk, "super-secret-password")
signed = unlocked.sign("This message is from me!")
```

### Verify a Signature

```python
from pokt import verify_signature

pub_key="public_key" # see PoktRPCDataProvider.get_signing_info("address")
signed_message="signed message"

isValid = verify_signature(pub_key, signed_message)
```
