from argparse import ArgumentParser
from functools import partial
from glob import iglob
from multiprocessing import cpu_count, Manager, Pool, Queue
import os
import re
from typing import Optional

from pokt import PoktRPCDataProvider
from pokt.index.ingest import ingest_block_range


def chunks_bounds(start_block: int, end_block: int, batch_size: int):
    return [
        (a, b, batch_size)
        for a, b in zip(
            range(start_block, end_block, batch_size),
            list(range(start_block - 1 + batch_size, end_block, batch_size))
            + [end_block],
        )
    ]


total_txs = 0
total_blocks = 0
total_errors = 0


def progress_reader(queue):
    global total_blocks, total_errors, total_txs
    while not queue.empty():
        try:
            update = queue.get(timeout=0.05)
            if update[0] == "txs":
                total_txs += update[1]
            elif update[0] == "error":
                total_errors += 1
            else:
                total_blocks += update[1]
            print(
                "\rBlocks: {} Transactions: {} Errors: {} ".format(
                    total_blocks, total_txs, total_errors
                ),
                end="",
                flush=True,
            )
        except:
            break
    return True


def ingest_chunk(
    start: int,
    end: int,
    batch_size: int,
    queue: Queue,
    rpc_url: str,
    headers: str,
    txs: str,
):
    global total_errors
    try:
        ingest_block_range(
            start,
            end,
            rpc_url,
            headers,
            txs,
            batch_size=batch_size,
            progress_queue=queue,
        )
    except Exception as e:
        print("Error encountered during: {} - {}".format(start, end))
        print(e)
        total_errors += 1
    return queue


def get_latest_block(url):
    rpc = PoktRPCDataProvider(url)
    return rpc.get_height() - 1


def _get_file_last_block(pq_file):
    match = re.match(r".*block_[0-9]+-([0-9]+)\.parquet", pq_file)
    if match:
        return int(match.group(1))
    return 0


def get_last_indexed(headers_dir, txs_dir):
    headers_pattern = os.path.join(headers_dir, "*.parquet")
    txs_pattern = os.path.join(txs_dir, "*.parquet")
    try:
        headers_last = max([_get_file_last_block(f) for f in iglob(headers_pattern)])
    except ValueError:
        headers_last = 0
    try:
        txs_last = max([_get_file_last_block(f) for f in iglob(txs_pattern)])
    except ValueError:
        txs_last = 0
    if headers_last != txs_last:
        raise RuntimeError("Headers and Transactions don't have matching indexes")
    return txs_last


def run_indexer(
    start_block: int,
    end_block: int,
    rpc_url: str,
    headers: str,
    txs: str,
    batch_size: int = 500,
    n_cores: Optional[int] = None,
):
    man = Manager()
    progress = man.Queue()
    bounds = chunks_bounds(start_block, end_block, batch_size)
    worker = partial(
        ingest_chunk, queue=progress, rpc_url=rpc_url, headers=headers, txs=txs
    )
    pool = Pool(n_cores)
    for bound in bounds:
        pool.apply_async(worker, args=bound, callback=progress_reader)
    pool.close()
    pool.join()
    print()
    man.shutdown()


def main():
    default_base = os.getcwd()
    index_default = os.path.join(default_base, "index")
    rpc_default = "http://localhost:8081"
    parser = ArgumentParser(
        "pokt-index", description="Index the pocket network blockchain data"
    )
    parser.add_argument(
        "-s",
        "--start",
        type=int,
        default=None,
        help="The block to start indexing from, defaults to either the first block, or the last indexed block.",
    )
    parser.add_argument(
        "-e",
        "--end",
        type=int,
        default=None,
        help="The block to index to. Defaults to the latest block.",
    )
    parser.add_argument(
        "-j",
        "--n-cores",
        type=int,
        default=None,
        help="The number of cores to use when indexing, defaults to 4 less than the total core count.",
    )
    parser.add_argument(
        "-u",
        "--url",
        type=str,
        default=rpc_default,
        help="The rpc url, defaults to http://localhost:8081.",
    )
    parser.add_argument(
        "-d",
        "--index-dir",
        type=str,
        default=index_default,
        help="The directory where the indexed files should be written to. Defaults to 'index' of the current working directory.",
    )
    parser.add_argument(
        "-b",
        "--batch-size",
        type=int,
        default=250,
        help="The number of blocks to write to each parquet file. Defaults to 250.",
    )
    args = parser.parse_args()
    headers = os.path.join(args.index_dir, "headers")
    txs = os.path.join(args.index_dir, "txs")
    msgs = os.path.join(args.index_dir, "tx_msgs")
    pos = os.path.join(msgs, "pos")
    pos_msgs = [
        os.path.join(pos, t)
        for t in ("MsgStake", "MsgBeginUnstake", "MsgUnjail", "Send")
    ]
    gov = os.path.join(msgs, "gov")
    gov_msgs = [
        os.path.join(gov, t)
        for t in ("msg_dao_transfer", "msg_change_param", "msg_upgrade")
    ]
    apps = os.path.join(msgs, "apps")
    apps_msgs = [
        os.path.join(apps, t)
        for t in ("MsgAppStake", "MsgAppUnjail", "MsgAppBeginUnstake")
    ]
    core = os.path.join(msgs, "pocketcore")
    core_msgs = [os.path.join(core, t) for t in ("proof", "claim")]
    dirs = [headers, txs]
    for group in (pos_msgs, gov_msgs, apps_msgs, core_msgs):
        dirs.extend(group)
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)
    start = get_last_indexed(headers, txs) if args.start is None else args.start
    end = get_latest_block(args.url) if args.end is None else args.end
    n_cores = cpu_count() - 4 if args.n_cores is None else args.n_cores
    print("Writing batches of {} blocks to {}".format(args.batch_size, args.index_dir))
    print(
        "Indexing from block {} to block {} via {} using {} cores".format(
            start + 1, end, args.url, n_cores
        )
    )
    run_indexer(start + 1, end, args.url, headers, txs, args.batch_size, n_cores)


if __name__ == "__main__":
    main()
