import os
import logging
from typing import Tuple, List, Any
import psycopg2 as pg
from psycopg2._psycopg import cursor, connection


async def connect() -> Tuple[connection, cursor]:
  db_host = os.environ['DB_HOST']
  db_name = os.environ['DB_NAME']
  db_user = os.environ['DB_USER']
  db_password = os.environ['DB_PASSWORD']
  db_conn = pg.connect(dbname=db_name, user=db_user, password=db_password, host=db_host)
  db_cursor = db_conn.cursor()
  return db_conn, db_cursor


async def disconnect(db_conn: connection, db_cursor: cursor) -> None:
  db_conn.close()
  db_cursor.close()


async def execute(query, autocommit=False) -> None:
  logging.debug(f'{__name__}.execute: query({query}) autocommit({autocommit})')
  db_conn, db_cursor = await connect()
  db_conn.autocommit = autocommit
  db_cursor.execute(query)
  await disconnect(db_conn, db_cursor)


async def fetchall(query) -> List[Tuple[Any, ...]]:
  logging.debug(f'{__name__}.fetchall: query({query})')
  db_conn, db_cursor = await connect()
  db_cursor.execute(query)
  data = db_cursor.fetchall()
  await disconnect(db_conn, db_cursor)
  return data


async def fetchone(query) -> Tuple[Any, ...] | None:
  logging.debug(f'{__name__}.fetchone: query({query})')
  db_conn, db_cursor = await connect()
  db_cursor.execute(query)
  data = db_cursor.fetchone()
  await disconnect(db_conn, db_cursor)
  return data
