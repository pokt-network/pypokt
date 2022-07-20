from dataclasses import dataclass
import os
from typing import TypedDict, Optional, Union
import pyarrow as pa

from ..rpc.models.validation import BlockHeader, Transaction, HashRange


def camel_to_snake(s):
    return "".join(["_" + c.lower() if c.isupper() else c for c in s]).lstrip("_")


def table_dir_map(index_dir):
    dir_map = {
        "headers": os.path.join(index_dir, "headers", "*.parquet"),
        "txs": os.path.join(index_dir, "txs", "*.parquet"),
    }
    for module in ("apps", "gov", "pocketcore", "pos"):
        mod_dir = os.path.join(index_dir, "tx_msgs", module)
        for msg_dir in [f.name for f in os.scandir(mod_dir) if f.is_dir()]:
            table_name = camel_to_snake(msg_dir).replace("msg", "").lstrip("_")
            dir_map[table_name] = os.path.join(mod_dir, msg_dir, "*.parquet")
    return dir_map


class HeaderRecord(TypedDict):
    chain_id: Optional[str]
    height: Optional[int]
    time: Optional[str]
    num_txs: Optional[int]
    total_txs: Optional[int]
    proposer_address: Optional[str]


def flatten_header(
    block_header: BlockHeader,
) -> HeaderRecord:
    return {
        "chain_id": block_header.chain_id,
        "height": block_header.height,
        "time": block_header.time,
        "num_txs": block_header.num_txs,
        "total_txs": block_header.total_txs,
        "proposer_address": block_header.proposer_address,
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


class TxRecord(TypedDict):
    height: Optional[int]
    hash_: Optional[str]
    index: Optional[int]
    result_code: Optional[int]
    codespace: Optional[str]
    signer: Optional[str]
    recipient: Optional[str]
    msg_type: Optional[str]
    entropy: Optional[int]
    fee_amount: Optional[str]
    fee_denom: Optional[str]
    signer_pubkey: Optional[str]
    empty_msg: bool


def flatten_tx(tx: Transaction) -> TxRecord:
    fee = tx.stdTx.fee
    fee_amount = fee[0].amount if fee else None
    fee_denom = fee[0].denom if fee else None
    return {
        "height": tx.height,
        "hash_": tx.hash_,
        "index": tx.index,
        "result_code": tx.tx_result.code,
        "codespace": tx.tx_result.codespace,
        "signer": tx.tx_result.signer,
        "recipient": tx.tx_result.recipient,
        "msg_type": tx.tx_result.message_type,
        "entropy": tx.stdTx.entropy,
        "fee_amount": fee_amount,
        "fee_denom": fee_denom,
        "signer_pubkey": tx.stdTx.signature.pub_key,
        "empty_msg": tx.stdTx.msg is None,
    }


tx_schema = pa.schema(
    [
        pa.field("height", pa.int64()),
        pa.field("hash_", pa.string()),
        pa.field("index", pa.int64()),
        pa.field("result_code", pa.int64()),
        pa.field("codespace", pa.string()),
        pa.field("signer", pa.string()),
        pa.field("recipient", pa.string()),
        pa.field("msg_type", pa.string()),
        pa.field("entropy", pa.int64()),
        pa.field("fee_amount", pa.string()),
        pa.field("fee_denom", pa.string()),
        pa.field("signer_pubkey", pa.string()),
        pa.field("empty_msg", pa.bool_()),
    ]
)


dao_change_param_msg_schema = pa.schema(
    [
        pa.field("height", pa.int64()),
        pa.field("hash_", pa.string()),
        pa.field("index", pa.int64()),
        pa.field("address", pa.string()),
        pa.field("param_key", pa.string()),
        pa.field("param_value", pa.string()),
    ]
)


class ChangeParamMsgRecord(TypedDict):
    height: Optional[int]
    hash_: Optional[str]
    index: Optional[int]


def _flatten_change_param_msg(tx: Transaction) -> dict:
    return {
        "height": tx.height,
        "hash_": tx.hash_,
        "index": tx.index,
        "address": tx.stdTx.msg.value.address,
        "param_key": tx.stdTx.msg.value.param_key,
        "param_value": str(tx.stdTx.msg.value.param_value),
    }


dao_transfer_msg_schema = pa.schema(
    [
        pa.field("height", pa.int64()),
        pa.field("hash_", pa.string()),
        pa.field("index", pa.int64()),
        pa.field("from_address", pa.string()),
        pa.field("to_address", pa.string()),
        pa.field("amount", pa.int64()),
        pa.field("action", pa.string()),
    ]
)


class DAOTransferMsgRecord(TypedDict):
    height: Optional[int]
    hash_: Optional[str]
    index: Optional[int]
    from_address: Optional[str]
    to_address: Optional[str]
    amount: Optional[int]
    action: Optional[str]


def _flatten_dao_transfer_msg(tx: Transaction) -> DAOTransferMsgRecord:
    return {
        "height": tx.height,
        "hash_": tx.hash_,
        "index": tx.index,
        "from_address": tx.stdTx.msg.value.from_address,
        "to_address": tx.stdTx.msg.value.to_address,
        "amount": tx.stdTx.msg.value.amount,
        "action": tx.stdTx.msg.value.action,
    }


dao_upgrade_msg_schema = pa.schema(
    [
        pa.field("height", pa.int64()),
        pa.field("hash_", pa.string()),
        pa.field("index", pa.int64()),
        pa.field("address", pa.string()),
        pa.field("upgrade_height", pa.int64()),
        pa.field("version", pa.string()),
        pa.field("old_upgrade_height", pa.int64()),
    ]
)


class UpgradeMsgRecord(TypedDict):
    height: Optional[int]
    hash_: Optional[str]
    index: Optional[int]
    address: Optional[str]
    upgrade_height: Optional[int]
    version: Optional[str]
    old_upgrade_height: Optional[int]


def _flatten_upgrade_msg(tx: Transaction) -> UpgradeMsgRecord:
    return {
        "height": tx.height,
        "hash_": tx.hash_,
        "index": tx.index,
        "address": tx.stdTx.msg.value.address,
        "upgrade_height": tx.stdTx.msg.value.upgrade.height,
        "version": tx.stdTx.msg.value.upgrade.version,
        "old_upgrade_height": tx.stdTx.msg.value.upgrade.old_upgrade_height,
    }


app_stake_msg_schema = pa.schema(
    [
        pa.field("height", pa.int64()),
        pa.field("hash_", pa.string()),
        pa.field("index", pa.int64()),
        pa.field("pubkey", pa.string()),
        pa.field("pubkey_type", pa.string()),
        pa.field("chains", pa.list_(pa.string())),
        pa.field("value", pa.int64()),
    ]
)


class AppStakeMsgRecord(TypedDict):
    height: Optional[int]
    hash_: Optional[str]
    index: Optional[int]
    pubkey: Optional[str]
    pubkey_type: Optional[str]
    chains: Optional[list[str]]
    value: Optional[int]


def _flatten_app_stake_msg(tx: Transaction) -> AppStakeMsgRecord:
    return {
        "height": tx.height,
        "hash_": tx.hash_,
        "index": tx.index,
        "pubkey": tx.stdTx.msg.value.pubkey.value,
        "pubkey_type": tx.stdTx.msg.value.pubkey.type_,
        "chains": tx.stdTx.msg.value.chains,
        "value": tx.stdTx.msg.value.value,
    }


app_begin_unstake_msg_schema = pa.schema(
    [
        pa.field("height", pa.int64()),
        pa.field("hash_", pa.string()),
        pa.field("index", pa.int64()),
        pa.field("application_address", pa.string()),
    ]
)


class AppBeginUnstakeMsgRecord(TypedDict):
    height: Optional[int]
    hash_: Optional[str]
    index: Optional[int]
    application_address: Optional[str]


def _flatten_app_begin_unstake_msg(tx: Transaction) -> AppBeginUnstakeMsgRecord:
    return {
        "height": tx.height,
        "hash_": tx.hash_,
        "index": tx.index,
        "application_address": tx.stdTx.msg.value.application_address,
    }


app_unjail_msg_schema = pa.schema(
    [
        pa.field("height", pa.int64()),
        pa.field("hash_", pa.string()),
        pa.field("index", pa.int64()),
        pa.field("address", pa.string()),
    ]
)


class AppUnjailMsgRecord(TypedDict):
    height: Optional[int]
    hash_: Optional[str]
    index: Optional[int]
    address: Optional[str]


def _flatten_app_unjail_msg(tx: Transaction) -> AppUnjailMsgRecord:
    return {
        "height": tx.height,
        "hash_": tx.hash_,
        "index": tx.index,
        "address": tx.stdTx.msg.value.address,
    }


node_stake_msg_schema = pa.schema(
    [
        pa.field("height", pa.int64()),
        pa.field("hash_", pa.string()),
        pa.field("index", pa.int64()),
        pa.field("public_key", pa.string()),
        pa.field("public_key_type", pa.string()),
        pa.field("chains", pa.list_(pa.string())),
        pa.field("value", pa.int64()),
        pa.field("service_url", pa.string()),
        pa.field("output_address", pa.string()),
    ]
)


class NodeStakeMsgRecord(TypedDict):
    height: Optional[int]
    hash_: Optional[str]
    index: Optional[int]
    public_key: Optional[str]
    public_key_type: Optional[str]
    chains: Optional[list[str]]
    value: Optional[int]
    service_url: Optional[str]
    output_address: Optional[str]


def _flatten_node_stake_msg(tx: Transaction) -> NodeStakeMsgRecord:
    return {
        "height": tx.height,
        "hash_": tx.hash_,
        "index": tx.index,
        "public_key": tx.stdTx.msg.value.public_key.value,
        "public_key_type": tx.stdTx.msg.value.public_key.type_,
        "chains": tx.stdTx.msg.value.chains,
        "value": tx.stdTx.msg.value.value,
        "service_url": tx.stdTx.msg.value.service_url,
        "output_address": tx.stdTx.msg.value.output_address,
    }


node_begin_unstake_msg_schema = pa.schema(
    [
        pa.field("height", pa.int64()),
        pa.field("hash_", pa.string()),
        pa.field("index", pa.int64()),
        pa.field("validator_address", pa.string()),
        pa.field("signer_address", pa.string()),
    ]
)


class NodeBeginUnstakeMsgRecord(TypedDict):
    height: Optional[int]
    hash_: Optional[str]
    index: Optional[int]
    validator_address: Optional[str]
    signer_address: Optional[str]


def _flatten_node_begin_unstake_msg(tx: Transaction) -> NodeBeginUnstakeMsgRecord:
    return {
        "height": tx.height,
        "hash_": tx.hash_,
        "index": tx.index,
        "validator_address": tx.stdTx.msg.value.validator_address,
        "signer_address": tx.stdTx.msg.value.signer_address,
    }


node_unjail_msg_schema = pa.schema(
    [
        pa.field("height", pa.int64()),
        pa.field("hash_", pa.string()),
        pa.field("index", pa.int64()),
        pa.field("address", pa.string()),
        pa.field("signer_address", pa.string()),
    ]
)


class NodeUnjailMsgRecord(TypedDict):
    height: Optional[int]
    hash_: Optional[str]
    index: Optional[int]
    address: Optional[str]
    signer_address: Optional[str]


def _flatten_node_unjail_msg(tx: Transaction) -> NodeUnjailMsgRecord:
    return {
        "height": tx.height,
        "hash_": tx.hash_,
        "index": tx.index,
        "address": tx.stdTx.msg.value.address,
        "signer_address": tx.stdTx.msg.value.signer_address,
    }


send_msg_schema = pa.schema(
    [
        pa.field("height", pa.int64()),
        pa.field("hash_", pa.string()),
        pa.field("index", pa.int64()),
        pa.field("from_address", pa.string()),
        pa.field("to_address", pa.string()),
        pa.field("amount", pa.int64()),
    ]
)


class SendMsgRecord(TypedDict):
    height: Optional[int]
    hash_: Optional[str]
    index: Optional[int]
    from_address: Optional[str]
    to_address: Optional[str]
    amount: Optional[int]


def _flatten_send_msg(tx: Transaction) -> SendMsgRecord:
    return {
        "height": tx.height,
        "hash_": tx.hash_,
        "index": tx.index,
        "from_address": tx.stdTx.msg.value.from_address,
        "to_address": tx.stdTx.msg.value.to_address,
        "amount": tx.stdTx.msg.value.amount,
    }


claim_msg_schema = pa.schema(
    [
        pa.field("height", pa.int64()),
        pa.field("hash_", pa.string()),
        pa.field("index", pa.int64()),
        pa.field("from_address", pa.string()),
        pa.field("total_proofs", pa.int64()),
        pa.field("expiration_height", pa.int64()),
        pa.field("evidence_type", pa.int64()),
        pa.field("app_pub_key", pa.string()),
        pa.field("chain", pa.string()),
        pa.field("session_height", pa.int64()),
        pa.field("merkle_hash", pa.string()),
        pa.field("merkle_root_lower", pa.string()),
        pa.field("merkle_root_upper", pa.string()),
    ]
)


class ClaimMsgRecord(TypedDict):
    height: Optional[int]
    hash_: Optional[str]
    index: Optional[int]
    from_address: Optional[str]
    total_proofs: Optional[int]
    expiration_height: Optional[int]
    evidence_type: Optional[int]
    app_pub_key: Optional[str]
    chain: Optional[str]
    session_height: Optional[int]
    merkle_hash: Optional[str]
    merkle_root_lower: Optional[str]
    merkle_root_upper: Optional[str]


def _flatten_claim_msg(tx: Transaction) -> ClaimMsgRecord:
    return {
        "height": tx.height,
        "hash_": tx.hash_,
        "index": tx.index,
        "from_address": tx.stdTx.msg.value.from_address,
        "total_proofs": tx.stdTx.msg.value.total_proofs,
        "expiration_height": tx.stdTx.msg.value.expiration_height,
        "evidence_type": tx.stdTx.msg.value.evidence_type,
        "app_pub_key": tx.stdTx.msg.value.header.app_public_key,
        "chain": tx.stdTx.msg.value.header.chain,
        "session_height": tx.stdTx.msg.value.header.session_height,
        "merkle_hash": tx.stdTx.msg.value.merkle_root.merkleHash,
        "merkle_root_lower": tx.stdTx.msg.value.merkle_root.range_.lower,
        "merkle_root_upper": tx.stdTx.msg.value.merkle_root.range_.upper,
    }


HashRangeStruct = pa.struct(
    [
        pa.field("merkle_hash", pa.string()),
        pa.field("range_lower", pa.string()),
        pa.field("range_upper", pa.string()),
    ]
)

proof_msg_schema = pa.schema(
    [
        pa.field("height", pa.int64()),
        pa.field("hash_", pa.string()),
        pa.field("index", pa.int64()),
        pa.field("merkle_proof_index", pa.int64()),
        pa.field("target_merkle_hash", pa.string()),
        pa.field("target_merkle_lower", pa.string()),
        pa.field("target_merkle_upper", pa.string()),
        pa.field("hash_ranges", pa.list_(HashRangeStruct)),
        pa.field("request_hash", pa.string()),
        pa.field("entropy", pa.int64()),
        pa.field("session_block_height", pa.int64()),
        pa.field("servicer_pub_key", pa.string()),
        pa.field("blockchain", pa.string()),
        pa.field("aat_version", pa.string()),
        pa.field("aat_app_pub_key", pa.string()),
        pa.field("aat_client_pub_key", pa.string()),
        pa.field("aat_signature", pa.string()),
        pa.field("signature", pa.string()),
        pa.field("evidence_type", pa.int64()),
    ]
)


class HashRangeItem(TypedDict):
    merkle_hash: Optional[str]
    range_lower: Optional[str]
    range_upper: Optional[str]


class RelayProofMsgRecord(TypedDict):
    height: Optional[int]
    hash_: Optional[str]
    index: Optional[int]
    merkle_proof_index: Optional[int]
    target_merkle_hash: Optional[str]
    target_merkle_lower: Optional[str]
    target_merkle_upper: Optional[str]
    hash_ranges: Optional[list[HashRangeItem]]
    request_hash: Optional[str]
    entropy: Optional[int]
    session_block_height: Optional[int]
    servicer_pub_key: Optional[str]
    blockchain: Optional[str]
    aat_version: Optional[str]
    aat_app_pub_key: Optional[str]
    aat_client_pub_key: Optional[str]
    aat_signature: Optional[str]
    signature: Optional[str]
    evidence_type: Optional[int]


def _flatten_relay_proof_msg(tx: Transaction) -> RelayProofMsgRecord:
    return {
        "height": tx.height,
        "hash_": tx.hash_,
        "index": tx.index,
        "merkle_proof_index": tx.stdTx.msg.value.merkle_proofs.index,
        "target_merkle_hash": tx.stdTx.msg.value.merkle_proofs.target_range.merkleHash,
        "target_merkle_lower": tx.stdTx.msg.value.merkle_proofs.target_range.range_.lower,
        "target_merkle_upper": tx.stdTx.msg.value.merkle_proofs.target_range.range_.upper,
        "hash_ranges": [
            {
                "merkle_hash": hr.merkleHash,
                "range_lower": hr.range_.lower,
                "range_upper": hr.range_.upper,
            }
            for hr in tx.stdTx.msg.value.merkle_proofs.hash_ranges
        ],
        "request_hash": tx.stdTx.msg.value.leaf.value.request_hash,
        "entropy": tx.stdTx.msg.value.leaf.value.entropy,
        "session_block_height": tx.stdTx.msg.value.leaf.value.session_block_height,
        "servicer_pub_key": tx.stdTx.msg.value.leaf.value.servicer_pub_key,
        "blockchain": tx.stdTx.msg.value.leaf.value.blockchain,
        "aat_version": "Empty"
        if tx.stdTx.msg.value.leaf.value.aat is None
        else tx.stdTx.msg.value.leaf.value.aat.version,
        "aat_app_pub_key": "Empty"
        if tx.stdTx.msg.value.leaf.value.aat is None
        else tx.stdTx.msg.value.leaf.value.aat.app_pub_key,
        "aat_client_pub_key": "Empty"
        if tx.stdTx.msg.value.leaf.value.aat is None
        else tx.stdTx.msg.value.leaf.value.aat.client_pub_key,
        "aat_signature": "Empty"
        if tx.stdTx.msg.value.leaf.value.aat is None
        else tx.stdTx.msg.value.leaf.value.aat.signature,
        "signature": tx.stdTx.msg.value.leaf.value.signature,
        "evidence_type": tx.stdTx.msg.value.evidence_type,
    }


RecordT = Union[
    HeaderRecord,
    TxRecord,
    ChangeParamMsgRecord,
    DAOTransferMsgRecord,
    UpgradeMsgRecord,
    AppStakeMsgRecord,
    AppBeginUnstakeMsgRecord,
    AppUnjailMsgRecord,
    NodeStakeMsgRecord,
    NodeBeginUnstakeMsgRecord,
    NodeUnjailMsgRecord,
    SendMsgRecord,
    ClaimMsgRecord,
    RelayProofMsgRecord,
    dict,
]


def flatten_tx_message(tx: Transaction) -> tuple[Optional[RecordT], str, str]:
    if tx.stdTx.msg is None:
        return None, "Unknown", "Unknown"
    msg_type = tx.stdTx.msg.type_
    flat = {}
    if msg_type == "pocketcore/proof":
        flat = _flatten_relay_proof_msg(tx)
    elif msg_type == "pocketcore/claim":
        flat = _flatten_claim_msg(tx)
    elif msg_type == "pos/MsgStake":
        flat = _flatten_node_stake_msg(tx)
    elif msg_type == "pos/MsgBeginUnstake":
        flat = _flatten_node_begin_unstake_msg(tx)
    elif msg_type == "pos/MsgUnjail":
        flat = _flatten_node_unjail_msg(tx)
    elif msg_type == "pos/Send":
        flat = _flatten_send_msg(tx)
    elif msg_type == "apps/MsgAppStake":
        flat = _flatten_app_stake_msg(tx)
    elif msg_type == "apps/MsgAppBeginUnstake":
        flat = _flatten_app_begin_unstake_msg(tx)
    elif msg_type == "apps/MsgAppUnjail":
        flat = _flatten_app_unjail_msg(tx)
    elif msg_type == "gov/msg_dao_transfer":
        flat = _flatten_dao_transfer_msg(tx)
    elif msg_type == "gov/msg_change_param":
        flat = _flatten_change_param_msg(tx)
    elif msg_type == "gov/msg_upgrade":
        flat = _flatten_upgrade_msg(tx)
    module, t = msg_type.split("/")
    return flat, module, t


def schema_for_msg(module: str, type_: str) -> pa.schema:
    if module == "pos":
        if type_ == "Send":
            return send_msg_schema
        elif type_ == "MsgStake":
            return node_stake_msg_schema
        elif type_ == "MsgBeginUnstake":
            return node_begin_unstake_msg_schema
        elif type_ == "MsgUnjail":
            return node_unjail_msg_schema
    elif module == "pocketcore":
        if type_ == "proof":
            return proof_msg_schema
        elif type_ == "claim":
            return claim_msg_schema
    elif module == "apps":
        if type_ == "MsgAppStake":
            return app_stake_msg_schema
        elif type_ == "MsgAppUnjail":
            return app_unjail_msg_schema
        elif type_ == "MsgAppBeginUnstake":
            return app_begin_unstake_msg_schema
    elif module == "gov":
        if type_ == "msg_upgrade":
            return dao_upgrade_msg_schema
        elif type_ == "msg_change_param":
            return dao_change_param_msg_schema
        elif type_ == "msg_dao_transfer":
            return dao_transfer_msg_schema
