# index

Everything that is used to pull the on-chain data into a format more fit for queries.

- `ingest.py`: Defines how to pull block/block ranges from the RPC and write them out to parquets.
- `db.py`: The convenience interface for the database.
- `main.py`: Defines the `pokt-index` cli script functionality for ingesting in block ranges multicore.
- `schema.py`: Defines the schema used when flattening the RPC response models in `ingest.py`.
- `query`: Subpackage for breaking up any repeated queries, could possibly exist as a module.
