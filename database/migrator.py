import os
import sys
import logging
import datetime
from typing import Tuple
from dotenv import load_dotenv
import psycopg2 as pg
from psycopg2._psycopg import cursor, connection


TABLES = ['documentsets', 'doctypes', 'files', 'filesdata', 'prompts']


def connect(db_name: str = 'postgres') -> Tuple[connection, cursor]:
  db_host = os.environ['DB_HOST']
  db_user = os.environ['DB_USER']
  db_password = os.environ['DB_PASSWORD']
  db_conn = pg.connect(dbname=db_name, user=db_user, password=db_password, host=db_host)
  db_cursor = db_conn.cursor()
  return db_conn, db_cursor


def disconnect(db_conn: connection, db_cursor: cursor) -> None:
  db_conn.close()
  db_cursor.close()


def check_database_exists() -> bool:
  db_name = os.environ['DB_NAME']
  db_conn, db_cursor = connect()
  sql = open('./database/sql/check_database_exists.mg.sql', 'r', encoding='utf8').read().replace('@DB_NAME', db_name);
  db_cursor.execute(sql)
  data = db_cursor.fetchall()
  result = bool(len(data))
  disconnect(db_conn, db_cursor)
  return result


def create_database() -> None:
  db_name = os.environ['DB_NAME']
  db_conn, db_cursor = connect()
  db_conn.autocommit = True
  sql = open('./database/sql/create_database.mg.sql', 'r', encoding='utf8').read().replace('@DB_NAME', db_name);
  db_cursor.execute(sql)
  disconnect(db_conn, db_cursor)


def drop_database() -> None:
  db_name = os.environ['DB_NAME']
  db_conn, db_cursor = connect()
  db_conn.autocommit = True
  sql = open('./database/sql/drop_database.mg.sql', 'r', encoding='utf8').read().replace('@DB_NAME', db_name);
  db_cursor.execute(sql)
  disconnect(db_conn, db_cursor)


def check_table_exists(table_name: str) -> bool:
  db_name = os.environ['DB_NAME']
  db_conn, db_cursor = connect(db_name=db_name)
  sql = open('./database/sql/check_table_exists.mg.sql', 'r', encoding='utf8').read().replace('@TABLE_NAME', table_name);
  db_cursor.execute(sql)
  data = db_cursor.fetchall()
  result = bool(len(data))
  disconnect(db_conn, db_cursor)
  return result


def create_table(table_name: str) -> None:
  db_name = os.environ['DB_NAME']
  db_conn, db_cursor = connect(db_name=db_name)
  sql = open(f'./database/sql/create_table_{table_name}.mg.sql', 'r', encoding='utf8').read();
  db_conn.autocommit = True
  db_cursor.execute(sql)
  disconnect(db_conn, db_cursor)


if __name__ == '__main__':
  load_dotenv(override=True)
  logging.basicConfig(level=logging.DEBUG,
                    format="<%(asctime)s> [%(levelname)s]: %(message)s",
                    handlers=[
                      logging.FileHandler(f'./logs/{datetime.date.today().isoformat()}.migrator.log', encoding='utf8'),
                      logging.StreamHandler()
                    ])
  logging.debug(f'database.migrator: started with args {sys.argv}')
  with_drop = True if '--fresh' in sys.argv else False

  if with_drop:
    logging.debug(f'database.migrator: drop database {os.environ["DB_NAME"]}')
    drop_database()
    logging.debug(f'database.migrator: database {os.environ["DB_NAME"]} droped')

  if not check_database_exists():
    logging.debug(f'database.migrator: create database {os.environ["DB_NAME"]}')
    create_database()
    logging.debug(f'database.migrator: database {os.environ["DB_NAME"]} created')
  for table in TABLES:
    if not check_table_exists(table):
      logging.debug(f'database.migrator: creating table {table}')
      create_table(table)
      logging.debug(f'database.migrator: table {table} created')
  
  logging.debug(f'database.migrator: finished')
