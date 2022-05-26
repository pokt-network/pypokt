# pypocket

Python Client SDK for Pocket Network

## Installation

```sh
git clone git@github.com:pokt-foundation/pypocket.git
cd pypocket
pip install wheel
pip install -e .
pip install duckdb pyarrow pandas
```

## Requirements

A Pocket RPC URL Can be acquired through either:

1. Access to a Pocket Node with RPC
2. An app endpoint from [the Portal](https://portal.pokt.network/)

## Usage

### Pocket RPC `/query`

All RPC methods that begin with `/query` are currently supported. These are
all exposed under the `PoktRPCDataProvider`.

```python
from pokt import PoktRPCDataProvider

rpc_url = "https://mainnet.pokt.network/v1/lb/<PortalID>"
pokt_rpc = PoktRPCDataProvider(rpc_url)

height = pokt_rpc.get_height()
supported_chains = pokt_rpc.get_supported_chains()
supply = pokt_rpc.get_supply()
```

### Pocket DB

CLI script available as `pokt-index` for pulling in transactions into a format
that can be queried.

```sh
$ pokt-index --help
usage: pokt-index [-h] [-s START] [-e END] [-j N_CORES] [-u URL] [-d INDEX_DIR] [-b BATCH_SIZE]

Index the pocket network blockchain data

optional arguments:
  -h, --help            show this help message and exit
  -s START, --start START
                        The block to start indexing from, defaults to either the first block, or the
                        last indexed block.
  -e END, --end END     The block to index to. Defaults to the latest block.
  -j N_CORES, --n-cores N_CORES
                        The number of cores to use when indexing, defaults to 4 less than the total
                        core count.
  -u URL, --url URL     The rpc url, defaults to http://localhost:8081.
  -d INDEX_DIR, --index-dir INDEX_DIR
                        The directory where the indexed files should be written to. Defaults to
                        'index' of the current working directory.
  -b BATCH_SIZE, --batch-size BATCH_SIZE
                        The number of blocks to write to each parquet file. Defaults to 250.
```

Schema of the available tables defined in `pokt/index/schema.py`

Tables are initially written in batches to parquet files, available at: `${INDEX_DIR}/<table-name>/*.parquet`.

These tables can either be queried directly:

```python
import duckdb

tx_dir = "/path/to/INDEX_DIR/txs/*.parquet"
con = duckdb.connection()
# Get result at python object
res = con.execute("SELECT COUNT(*) FROM read_parquet({})".format(tx_dir)).fetchall()
# Get result in pandas dataframe (needs pandas install)
df = con.execute("SELECT * FROM read_parquet({}) LIMIT 500".format(tx_dir)).df()
con.close()
```

Or ingested into an engine (using `duckdb` as reference):

```python
import duckdb

tx_dir = "/path/to/INDEX_DIR/txs/*.parquet"
# Create a txs table on a new duckdb file.
con_new = duckdb.connection("new.duckdb")
con_new.execute("CREATE TABLE txs AS SELECT * FROM read_parquet({})".format(tx_dir))
con_new.close()
# Insert txs into an existing table on a duckdb file.
con = duckdb.connection("existing.duckdb")
con.execute("INSERT INTO txs SELECT * FROM read_parquet({})".format(tx_dir))
con.close()
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

## Current Functionality

`[x]` -> Complete  
`[~]` -> Partial functionality

**Pocket RPC:**

- [x] Pocket RPC `/query`
- [~] Pocket DB
- [] Pocket RPC `/client`

**Wallet:**

- [x] Create Account (PPK file/Private Key)
- [x] Import Account (from PPK/Private Key)
- [x] Sign message with account
- [x] Verify signed message
- [] Create and sign transactions from account
- [] Create and sign multisig transactions from account

**Portal RPC:**

- [~] pocket RPC provider
- [] web3 providers
- [] figure out other types
