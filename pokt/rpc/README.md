# rpc

Routes are mapped as follows below:

## client => `rpc.relays`

- [] dispatch
- [] relay
- [] sim
- [] rawtx
- [] challenge

## query => rpc.data

### `rpc.data.account`

- [x] account
- [x] accounts
- [x] balance
- [x] accounttxs

### `rpc.data.network`

- [x] allParams
- [x] height
- [x] param
- [x] supportedChains
- [x] state
- [x] supply
- [x] version
- [x] upgrade

### `rpc.data.block`

- [x] block
- [x] blockTxs

### `rpc.data.transaction`

- [x] tx

### `rpc.data.service`

- [x] app
- [x] apps
- [x] node
- [x] nodes
- [x] nodeclaim
- [x] nodeclaims
- [x] signinginfo

## `models`

This is where all the validation models that come from the OpenAPI spec reside.

Initially all models were built from the OpenAPI `spec.yaml`. The `spec` directory
in the root of the project contains what was used, and the build script is in the
`scripts/rpc_build.sh`. These built models live in `models/valdation/_generated.py`.

It turned out that there were some discrepancies in the spec, so any adaptions
that were made to better support the actual expected validation live in
`models/validation/_overrides.py`.

`model/validation/__init__.py`, will first import everything from
`_generated.py`, and then anything that needs to be specifically overidden is
imported from `models/validation/_overrides.py` as needed.

## `utils.py`/`async_utls.py`

These define utility functions for constructing get/posts/ingesting incoming errors.
