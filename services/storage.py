import os
import aiofiles


async def save(file_name: str, file_bytes: bytes) -> None:
  storage_path = os.environ['APP_FILE_STORAGE']
  file_path = f'{storage_path}/{file_name}'

  async with aiofiles.open(file_path, 'wb') as file:
    await file.write(file_bytes)


async def get_file_path(file_name: str) -> str:
  storage_path = os.environ['APP_FILE_STORAGE']
  return f'{storage_path}/{file_name}'
