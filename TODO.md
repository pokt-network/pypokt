## RPC

- All of the client routes need to be implemented.
- `aiohttp` for async support
- Error handling for the occasional 502/504
- Built in logging to capture what we need to identify errors on our end.

## Account/Transactions

- Allow for seed phrase generation of wallet.
- Integrate in `pokt/views/qr_code.py`
- All transactions.

## Indexer/DB

- Improve `pokt/index/main.py` to look for missing chunks instead of starting from highest indexed.
- Make `pokt/index/main.py` check an existing database for missing chunks.
- Migrate `pokt/index/main.py` and `pokt/index/ingest.py` to asyncio
- `stdTx` types for full transaction level detail.
- `block -> header -> evidence` validation model for non string evidence.
- A DB convenience interface.
  - Sweep new parquets into a database instance.
  - Same command for create/insert, handle the nuance behind the scenes

## QoL

- Nicer base `__repr__/__str__`s
- Collective Table `__repr__/__str__`s via `tabulate`
- REPL/Notebook/Qt Console `__repr__`s:
  - `_repr_pretty_`
  - `_repr_html_`
  - `_repr_markdown_`
  - `_repr_latex_`

## Test Coverage

- `pokt/rpc/data/account.py`
- `pokt/rpc/data/block.py`
- `pokt/rpc/data/service.py`
- `pokt/rpc/data/transaction.py`

## Docs

- Inline coverage
