import pyarrow as pa

from ..rpc.models.validation import BlockHeader, Transaction


def flatten_header(
    block_header: BlockHeader,
) -> dict:  # TODO dataclass/typedict the flat models
    return {
        "chain_id": block_header.chain_id,
        "height": block_header.height,
        "time": block_header.time,
        "num_txs": block_header.num_txs,
        "total_txs": block_header.total_txs,
        "proposer_address": block_header.proposer_address,
    }


def flatten_tx(tx: Transaction) -> dict:  # TODO dataclass/typedict the flat models
    return {
        "height": tx.height,
        "hash_": tx.hash_,
        "index": tx.index,
        "result_code": tx.tx_result.code,
        "codespace": tx.tx_result.codespace,
        "signer": tx.tx_result.signer,
        "recipient": tx.tx_result.recipient,
        "msg_type": tx.tx_result.message_type,
    }


block_header_schema = pa.schema(
    [
        pa.field("chain_id", pa.string()),
        pa.field("height", pa.int64()),
        pa.field("time", pa.string()),
        pa.field("num_txs", pa.int64()),
        pa.field("total_txs", pa.int64()),
        pa.field("proposer_address", pa.string()),
    ]
)
tx_schema = pa.schema(
    [
        pa.field("height", pa.int64()),
        pa.field("hash_", pa.string()),
        pa.field("index", pa.int64()),
        pa.field("result_code", pa.int32()),
        pa.field("codespace", pa.string()),
        pa.field("signer", pa.string()),
        pa.field("recipient", pa.string()),
        pa.field("msg_type", pa.string()),
    ]
)
