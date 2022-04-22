# pokt

- `providers`: All provider interfaces, likely the entry point for most users.
- `rpc`: Defines the http client methods and validation models for communicating over RPC.
- `transactions`: Everything needed for encoding transactions
- `views`: Currently a collection of assorted interfaces and QoL helpers.
- `models`: Largely unused models originally designed for use in stateful applications. Validation models currently live in `rpc`.
- `wallet.py`: Module that defines all functions needed for creating a similar to the current `pocket-js`.
- `assets`: any assets used in other contexts
