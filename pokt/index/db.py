from contextlib import contextmanager
import glob
import os
import threading
from typing import Sequence, Optional

import duckdb
import pandas as pd

from .schema import table_dir_map


class DuckDB:
    @staticmethod
    def get_table_names(con) -> list[str]:
        records = con.execute(
            "SELECT table_name FROM information_schema.tables"
        ).fetchall()
        return [r[0] for r in records]

    @classmethod
    def from_index_dir(cls, index_dir: str, db_fname: str = "duck.db"):
        if not os.path.isdir(index_dir):
            raise ValueError(
                "The provided index directory, {}, does not appear to be a directory"
            )
        db = cls(db_fname)
        tables = table_dir_map(index_dir)
        for name, parquets in tables.items():
            if glob.glob(parquets):
                db.add_parquets_to_table(parquets, name)
        return db

    def __init__(self, database: str = None, config: Optional[dict] = None):
        self._database = database if database is not None else ":memory:"
        self._config = config if config is not None else {}

        self.needs_writer = threading.Condition()
        self.needs_reader = threading.Condition()

        self.wants_reader = threading.Event()
        self.wants_writer = threading.Event()

        self.is_reader = threading.Event()
        self.is_writer = threading.Event()

        self.n_readers = 0
        self.n_writers = 0
        self._connection = self._connect(read_only=False)
        self.is_writer.set()

    def multiprocessing_setup(self):
        with self.read_only_cursor() as c:
            return c

    @contextmanager
    def _reader_cursor(self, **kwargs):
        if self.is_reader.is_set() and not self.wants_writer.is_set():
            cur = self._connection.cursor()
        else:
            with self.needs_reader:
                self.wants_reader.set()
                self.needs_writer.wait_for(self.no_writers)
                if self._connection is not None:
                    self._connection.close()
                self._connection = self._connect(read_only=True, **kwargs)
                self.is_reader.set()
                self.is_writer.clear()
                self.wants_reader.clear()
            cur = self._connection.cursor()
        try:
            self.n_readers += 1
            yield cur
        finally:
            cur.close()
            self.n_readers -= 1

    @contextmanager
    def _writer_cursor(self, **kwargs):
        if self.is_writer.is_set() and not self.wants_reader.is_set():
            cur = self._connection.cursor()
        else:
            with self.needs_writer:
                self.wants_writer.set()
                self.needs_reader.wait_for(self.no_readers)
                if self._connection is not None:
                    self._connection.close()
                self._connection = self._connect(**kwargs)
                self.is_writer.set()
                self.is_reader.clear()
                self.wants_writer.clear()
                cur = self._connection.cursor()
        try:
            self.n_writers += 1
            yield cur
        finally:
            cur.close()
            self.n_writers -= 1

    @contextmanager
    def _either_cursor(self, **kwargs):
        if self.is_reader.is_set() or self.wants_reader.is_set():
            method = self._reader_cursor
        else:
            method = self._writer_cursor
        with method(**kwargs) as cur:
            yield cur

    def _connect(self, read_only: bool = False, config: Optional[dict] = None):
        config = self._config if config is None else config
        return duckdb.connect(self._database, read_only=read_only, config=config)

    def update(self, database: str = None, config: Optional[dict] = None):
        if database and database != self._database:
            self._database = database
        if config is not None:
            self._config = config

    def no_readers(self) -> bool:
        return self.n_readers == 0 and not self.wants_reader.is_set()

    def no_writers(self) -> bool:
        return self.n_writers == 0 and not self.wants_writer.is_set()

    @contextmanager
    def cursor(self, config: Optional[dict] = None):
        config = self._config if config is None else config
        with self._either_cursor(config=config) as cur:
            yield cur

    @contextmanager
    def write_cursor(self, config: Optional[dict] = None):
        config = self._config if config is None else config
        with self._writer_cursor(config=config) as cur:
            yield cur

    @contextmanager
    def read_only_cursor(self, config: Optional[dict] = None):
        config = self._config if config is None else config
        with self._reader_cursor(config=config) as cur:
            yield cur

    def table_names(self) -> list[str]:
        with self.cursor() as cur:
            return DuckDB.get_table_names(cur)

    def table_exists(self, table_name: str) -> bool:
        if self._database != ":memory:" and not os.path.exists(self._database):
            return False
        with self.cursor() as con:
            table_names = DuckDB.get_table_names(con)
            return table_name in table_names

    def add_df_to_table(
        self, df: pd.DataFrame, table_name: str, unique_field: Optional[str] = None
    ):
        with self.write_cursor() as cur:
            if self.table_exists(table_name) and unique_field is None:
                DuckDB._insert_df_to_table(cur, df, table_name)
            elif self.table_exists(table_name) and unique_field is not None:
                DuckDB._insert_unique_df_to_table(cur, df, table_name, unique_field)
            else:
                DuckDB._create_table_from_df(cur, df, table_name)

    def add_parquets_to_table(
        self, parquets: str, table_name: str, unique_field: Optional[str] = None
    ):
        with self.write_cursor() as cur:
            if self.table_exists(table_name) and unique_field is None:
                DuckDB._insert_parquets_to_table(cur, parquets, table_name)
            elif self.table_exists(table_name) and unique_field is not None:
                DuckDB._insert_unique_parquets_to_table(
                    cur, parquets, table_name, unique_field
                )
            else:
                DuckDB._create_table_from_parquets(cur, parquets, table_name)

    @staticmethod
    def _create_table_from_df(con, df: pd.DataFrame, table_name: str):
        con.register("df_view_create", df)
        con.execute(
            "CREATE TABLE {} AS SELECT * FROM df_view_create".format(table_name)
        )

    @staticmethod
    def _create_table_from_parquets(con, parquets: str, table_name: str):
        con.execute(
            "CREATE TABLE {} AS SELECT * FROM read_parquet('{}');".format(
                table_name, parquets
            ),
        )

    @staticmethod
    def _insert_df_to_table(con, df: pd.DataFrame, table_name: str):
        con.register("df_view_insert", df)
        con.execute("INSERT INTO {} SELECT * FROM df_view_insert".format(table_name))

    @staticmethod
    def _insert_parquets_to_table(con, parquets: str, table_name: str):
        con.execute(
            "INSERT INTO {} SELECT * FROM read_parquet('{}');".format(
                table_name, parquets
            ),
        )

    @staticmethod
    def _insert_unique_parquets_to_table(
        con, parquets: str, table_name: str, unique_field: str
    ):
        con.execute(
            "INSERT INTO {} SELECT * FROM read_parquet('{}') WHERE {} NOT IN (SELECT {} FROM {});".format(
                table_name, parquets, unique_field, unique_field, table_name
            ),
        )

    @staticmethod
    def _insert_unique_df_to_table(
        con, df: pd.DataFrame, table_name: str, unique_field: str
    ):
        con.register("df_view_insert", df)
        con.execute(
            "INSERT INTO {} SELECT * FROM df_view_insert WHERE {} NOT IN (SELECT {} FROM {});".format(
                table_name, unique_field, unique_field, table_name
            ),
        )
