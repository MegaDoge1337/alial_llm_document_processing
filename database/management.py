import aiofiles
from typing import Tuple, List, Any
import database.connector as db


async def get_classification_prompt() -> str:
  sql_file = await aiofiles.open('./database/sql/select_latest_prompt_by_type.func.sql', 'r', encoding='utf8')
  query = await sql_file.read()
  classification_prompt_query = query.replace('@TYPE', 'classification')
  classification_prompt: str = (await db.fetchone(classification_prompt_query))[0]
  return classification_prompt


async def get_doctype_name_by_id(doctype: int) -> str:
  sql_file = await aiofiles.open('./database/sql/select_doctype_name_by_id.func.sql', 'r', encoding='utf8')
  query = await sql_file.read()
  doctype_query = query.replace('@DOCTYPEID', str(doctype))
  doctype = (await db.fetchone(doctype_query))[0]
  return doctype


async def get_doctype_id_by_name(doctype: str) -> int:
  sql_file = await aiofiles.open('./database/sql/select_doctype_id_by_name.func.sql', 'r', encoding='utf8')
  query = await sql_file.read()
  doc_type_id_query = query.replace('@DOCTYPE', doctype)
  doc_type_id: str = (await db.fetchone(doc_type_id_query))[0]
  return int(doc_type_id)


async def get_extraction_prompt_by_doctype(doctype_id: int) -> str:
  sql_file = await aiofiles.open('./database/sql/select_extraction_prompt_by_doctype.func.sql', 'r', encoding='utf8')
  query = await sql_file.read()
  extraction_prompt_query = query.replace('@DOCTYPEID', str(doctype_id))
  extraction_prompt: str = (await db.fetchone(extraction_prompt_query))[0]
  return extraction_prompt


async def get_files_for_processing() -> List[Tuple[Any, ...]] | None:
  sql_file = await aiofiles.open('./database/sql/select_files_to_processing.func.sql', 'r', encoding='utf8')
  query = await sql_file.read()
  rows = await db.fetchall(query)
  return None if len(rows) == 0 else rows


async def save_file_text_layer(file_name: str, file_text: str) -> None:
  sql_file = await aiofiles.open('./database/sql/update_file_text_layer.func.sql', 'r', encoding='utf8')
  query = await sql_file.read()
  query = query.replace('@TEXTLAYER', file_text)
  query = query.replace('@FILENAME', file_name)
  await db.execute(query, autocommit=True)


async def get_file_id(file_name: str) -> int:
  sql_file = await aiofiles.open('./database/sql/select_file_id.func.sql', 'r', encoding='utf8')
  query = await sql_file.read()
  query = query.replace('@FILENAME', file_name)
  id = int((await db.fetchone(query))[0])
  return id


async def get_file_name_by_id(file_id: int) -> str:
  sql_file = await aiofiles.open('./database/sql/select_file_name_by_id.func.sql', 'r', encoding='utf8')
  query = await sql_file.read()
  query = query.replace('@FILEID', str(file_id))
  filename = (await db.fetchone(query))[0]
  return filename


async def create_file_data(file_id: int, doctype_id: int, file_data: dict) -> None:
  sql_file = await aiofiles.open('./database/sql/insert_file_data.func.sql', 'r', encoding='utf8')
  query = await sql_file.read()
  query = query.replace('@FILEID', str(file_id))
  query = query.replace('@DOCTYPEID', str(doctype_id))
  query = query.replace('@DOCMUMBER', file_data['DocNumber'] if 'DocNumber' in file_data.keys() else '-')
  query = query.replace('@DOCDATE', file_data['DocDate'] if 'DocDate' in file_data.keys() else '-')
  query = query.replace('@EXECUTOR', file_data['Executor'] if 'Executor' in file_data.keys() else '-')
  query = query.replace('@SUM', file_data['Sum'] if 'Sum' in file_data.keys() else '-')
  await db.execute(query, autocommit=True)


async def update_file_data(file_id: int, file_data: dict) -> None:
  sql_file = await aiofiles.open('./database/sql/update_file_data.func.sql', 'r', encoding='utf8')
  query = await sql_file.read()
  query = query.replace('@DOCMUMBER', file_data['DocNumber'] if 'DocNumber' in file_data.keys() else '-')
  query = query.replace('@DOCDATE', file_data['DocDate'] if 'DocDate' in file_data.keys() else '-')
  query = query.replace('@EXECUTOR', file_data['Executor'] if 'Executor' in file_data.keys() else '-')
  query = query.replace('@SUM', file_data['Sum'] if 'Sum' in file_data.keys() else '-')
  query = query.replace('@FILEID', str(file_id))
  await db.execute(query, autocommit=True)


async def get_file_data(file_id: int) -> Tuple[Any, ...] | None:
  sql_file = await aiofiles.open('./database/sql/select_file_data.func.sql', 'r', encoding='utf8')
  query = await sql_file.read()
  query = query.replace('@FILEID', str(file_id))
  file_data = await db.fetchone(query)
  return file_data


async def get_file_data_doctype_id(file_id: int) -> int | None:
  sql_file = await aiofiles.open('./database/sql/select_file_data_doctype.func.sql', 'r', encoding='utf8')
  query = await sql_file.read()
  query = query.replace('@FILEID', str(file_id))
  doctype = await db.fetchone(query)
  return int(doctype[0]) if doctype != None else None


async def set_file_status(file_id: int, status: str = 'Обработано') -> None:
  sql_file = await aiofiles.open('./database/sql/update_file_status.func.sql', 'r', encoding='utf8')
  query = await sql_file.read()
  query = query.replace('@STATUS', status)
  query = query.replace('@FILEID', str(file_id))
  await db.execute(query, autocommit=True)
