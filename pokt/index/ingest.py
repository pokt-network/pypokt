"""
Ingestion of blocks and their contained transactions from RPC.
"""
from collections import defaultdict
from dataclasses import dataclass
import multiprocessing as mp
import os
import queue
from typing import Union, Optional

import pyarrow as pa
import pyarrow.parquet as pq
from requests import Session


from ..rpc.utils import PoktRPCError, PortalRPCError
from ..rpc.models import BlockHeader, Transaction
from ..rpc.data.block import get_block_transactions, get_block
from .schema import (
    block_header_schema,
    tx_schema,
    flatten_header,
    flatten_tx,
    flatten_tx_message,
    schema_for_msg,
)

QueueT = Union[queue.Queue, mp.Queue]


class RetriesExceededError(Exception):
    pass


def ingest_txs_by_block(
    block_no: int,
    rpc_url: str,
    session: Optional[Session] = None,
    page: int = 1,
    retries: int = 100,
    txs: Optional[list[Transaction]] = None,
    progress_queue: Optional[QueueT] = None,
) -> list[Transaction]:
    if txs is None:
        txs = []
    try:
        block_txs = get_block_transactions(
            rpc_url, height=block_no, per_page=1000, page=page, session=session
        )
    except (PoktRPCError, PortalRPCError):
        if progress_queue:
            progress_queue.put(("error", "txs", block_no, page))
        if retries < 0:
            raise RetriesExceededError(
                "Out of retries getting block {} transactions page {}".format(
                    block_no, page
                )
            )
        return ingest_txs_by_block(
            block_no,
            rpc_url,
            session=session,
            page=page,
            retries=retries - 1,
            txs=txs,
            progress_queue=progress_queue,
        )
    while block_txs.txs:
        txs.extend(block_txs.txs)
        page += 1
        try:
            block_txs = get_block_transactions(
                rpc_url, height=block_no, per_page=1000, page=page, session=session
            )
        except (PoktRPCError, PortalRPCError):
            if progress_queue:
                progress_queue.put(("error", "txs", block_no, page))
            if retries < 0:
                raise RetriesExceededError(
                    "Out of retries getting block {} transactions page {}".format(
                        block_no, page
                    )
                )
            return ingest_txs_by_block(
                block_no,
                rpc_url,
                session=session,
                page=page,
                retries=retries - 1,
                txs=txs,
                progress_queue=progress_queue,
            )
    return txs


def ingest_block_header(
    block_no: int,
    rpc_url: str,
    session: Optional[Session] = None,
    retries: int = 100,
    progress_queue: Optional[QueueT] = None,
) -> BlockHeader:
    try:
        block = get_block(rpc_url, height=block_no, session=session)
    except (PoktRPCError, PortalRPCError):
        if progress_queue:
            progress_queue.put(("error", "block", block_no))
        if retries < 0:
            raise RetriesExceededError(
                "Out of retries getting block {}".format(block_no)
            )
        return ingest_block_header(
            block_no, rpc_url, session=session, retries=retries - 1
        )
    else:
        if block.block is None and retries > 0:
            return ingest_block_header(
                block_no,
                rpc_url,
                session=session,
                retries=retries - 1,
                progress_queue=progress_queue,
            )
    return block.block.header


def _block_headers_to_table(headers):
    record_dict = defaultdict(list)
    for header in headers:
        for k, v in header.items():
            record_dict[k].append(v)
    return pa.Table.from_pydict(record_dict).cast(block_header_schema)


def _txs_to_table(txs):
    record_dict = defaultdict(list)
    for tx in txs:
        for k, v in tx.items():
            record_dict[k].append(v)
    return pa.Table.from_pydict(record_dict).cast(tx_schema)


def flatten_tx_messages(txs):
    msgs = {
        "apps": defaultdict(list),
        "gov": defaultdict(list),
        "pos": defaultdict(list),
        "pocketcore": defaultdict(list),
    }
    for tx in txs:
        record, module, type_ = flatten_tx_message(tx)
        if record is not None:
            msgs[module][type_].append(record)
    return msgs


def _msgs_to_tables(msgs):
    tables = {
        "apps": {},
        "gov": {},
        "pos": {},
        "pocketcore": {},
    }
    for module, items in msgs.items():
        for type_, msgs in items.items():
            record_dict = defaultdict(list)
            for msg in msgs:
                for k, v in msg.items():
                    record_dict[k].append(v)
            tables[module][type_] = pa.Table.from_pydict(record_dict).cast(
                schema_for_msg(module, type_)
            )
    return tables


def _append_msg_tables(msgs_dir, tables, start_block, end_block):
    for module, items in tables.items():
        for type_, table in items.items():
            parquet_dir = os.path.join(msgs_dir, module, type_)
            _parquet_append(parquet_dir, table, start_block, end_block)


def _parquet_append(parquet_dir, table, start_block, end_block):
    def _parquet_name_callback(*args, **kwargs):
        return "block_{}-{}.parquet".format(start_block, end_block)

    pq.write_to_dataset(
        table, parquet_dir, partition_filename_cb=_parquet_name_callback
    )


def ingest_block(
    block_no: int,
    rpc_url: str,
    session: Optional[Session] = None,
    progress_queue: Optional[QueueT] = None,
):
    txs = ingest_txs_by_block(block_no, rpc_url, session, progress_queue=progress_queue)
    flat_txs = [flatten_tx(tx) for tx in txs]
    msgs = flatten_tx_messages(txs)
    header = ingest_block_header(
        block_no, rpc_url, session, progress_queue=progress_queue
    )
    flat_header = flatten_header(header)
    return flat_txs, flat_header, msgs


def ingest_block_range(
    starting_block: int,
    ending_block: int,
    rpc_url: str,
    block_parquet,
    tx_parquet,
    msgs_parquet,
    batch_size=1000,
    session: Optional[Session] = None,
    progress_queue: Optional[QueueT] = None,
):
    if session is None:
        session = Session()
    txs = []
    headers = []
    msgs = {
        "apps": defaultdict(list),
        "gov": defaultdict(list),
        "pos": defaultdict(list),
        "pocketcore": defaultdict(list),
    }
    group_start = block_no = starting_block
    for i, block_no in enumerate(range(starting_block, ending_block + 1)):
        if i != 0 and i % batch_size == 0:
            header_table = _block_headers_to_table(headers)
            txs_table = _txs_to_table(txs)
            msgs_tables = _msgs_to_tables(msgs)
            _parquet_append(block_parquet, header_table, group_start, block_no)
            _parquet_append(tx_parquet, txs_table, group_start, block_no)
            _append_msg_tables(msgs_parquet, msgs_tables, group_start, block_no)
            if progress_queue:
                progress_queue.put(("block", len(headers)))
                progress_queue.put(("txs", len(txs)))
            group_start = block_no
            txs = []
            headers = []
            msgs = {
                "apps": defaultdict(list),
                "gov": defaultdict(list),
                "pos": defaultdict(list),
                "pocketcore": defaultdict(list),
            }
        block_txs, block_header, block_msgs = ingest_block(
            block_no, rpc_url, session=session
        )
        txs.extend(block_txs)
        headers.append(block_header)
        for mod, items in block_msgs.items():
            for t, ms in items.items():
                msgs[mod][t].extend(ms)
    if headers:
        header_table = _block_headers_to_table(headers)
        _parquet_append(block_parquet, header_table, group_start, block_no)
    if txs:
        txs_table = _txs_to_table(txs)
        _parquet_append(tx_parquet, txs_table, group_start, block_no)
    if msgs:
        msgs_tables = _msgs_to_tables(msgs)
        _append_msg_tables(msgs_parquet, msgs_tables, group_start, block_no)
    if progress_queue:
        progress_queue.put(("block", len(headers)))
        progress_queue.put(("txs", len(txs)))
