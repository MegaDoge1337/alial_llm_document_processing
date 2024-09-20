import os
import logging
import database.management as dbm
import services.ocr as ocr
import services.llm as llm
import services.anon as anon
import services.storage as storage


async def init_scheduler_flags() -> None:
  os.environ['LOCK_SCHEDULER_FLAG'] = '0'


async def lock_scheduler() -> None:
  os.environ['LOCK_SCHEDULER_FLAG'] = '1'
  logging.basicConfig(level=logging.DEBUG)
  logging.debug(f'{__name__}.lock_scheduler: scheduler locked')


async def unlock_scheduler() -> None:
  os.environ['LOCK_SCHEDULER_FLAG'] = '0'
  logging.basicConfig(level=logging.DEBUG)
  logging.debug(f'{__name__}.lock_scheduler: scheduler unlocked')


async def is_scheduler_locked() -> bool:
  return os.environ['LOCK_SCHEDULER_FLAG'] == '1'


async def run() -> None:
  is_locked = await is_scheduler_locked()
  if not is_locked:
    await process_files()


async def process_files() -> None:
  files = await dbm.get_files_for_processing()
  if files is None:
    logging.debug(f'{__name__}.process_files: 0 files to processed')
    return None
  logging.debug(f'{__name__}.process_files: {len(files)} files to processed')
  filerow = files[0]
  filename = filerow[0]
  file_id = await dbm.get_file_id(filename)
  file_path = await storage.get_file_path(filename)
  file_text = await ocr.extract_text(file_path)
  file_text = file_text.replace("'", '"')
  await dbm.save_file_text_layer(filename, file_text)
  file_text = await anon.make_anonimization(file_text)

  file_data = await dbm.get_file_data(file_id)
  file_data_exists = (file_data != None)
  file_data_doctype_id = None
  if file_data_exists:
    file_data_doctype_id = await dbm.get_file_data_doctype_id(file_id)

  processing_data = await llm.process_document(file_text, file_data_exists, file_data_doctype_id)

  complex_data = {}
  complex_data.update(processing_data[1])
  complex_data['DocType'] = processing_data[0]['DocType']

  if file_data_exists:
    await dbm.update_file_data(file_id, processing_data[1])
  else:
    file_data_doctype_id = await dbm.get_doctype_id_by_name(complex_data['DocType'].strip().rstrip().capitalize())
    await dbm.create_file_data(file_id, file_data_doctype_id, complex_data)
    
  await dbm.set_file_status(file_id)
  logging.debug(f'{__name__}.process_files: {filename} processed')
