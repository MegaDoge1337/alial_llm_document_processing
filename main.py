import os
import logging
import datetime
from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI
from fastapi import UploadFile
from fastapi.responses import FileResponse
from dto import UploadFileResponse, \
                CalculationTokensRequest, \
                CalculationTokensResponse
from fastapi_utils.tasks import repeat_every
from contextlib import asynccontextmanager
import services.storage as storage
import services.scheduler as scheduler
import database.management as dbm


load_dotenv(override=True)
logging.basicConfig(level=logging.DEBUG,
                    format="<%(asctime)s> [%(levelname)s]: %(message)s",
                    handlers=[
                      logging.FileHandler(f'./logs/{datetime.date.today().isoformat()}.log', encoding='utf8'),
                      logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
  await scheduler.init_scheduler_flags()
  await run_scheduler()
  yield


@repeat_every(seconds=1, logger=logger, wait_first=True)
async def run_scheduler():
  await scheduler.run()


app = FastAPI(lifespan=lifespan)


@app.post('/tokens')
async def tokens(body: CalculationTokensRequest):
   from razdel import tokenize
   amount = len(list(tokenize(body.text)))
   response = CalculationTokensResponse()
   response.amount = amount
   return response


@app.post('/upload')
async def upload(file: UploadFile):
  await storage.save(file.filename, await file.read())
  response = UploadFileResponse()
  response.file_name = file.filename
  return response


@app.get('/view/{id}.pdf')
async def view(id: int):
    file_name = await dbm.get_file_name_by_id(id)
    file_path = await storage.get_file_path(file_name)
    return FileResponse(path=file_path, filename=file_name, media_type='application/octet-stream')


@app.post('/scheduler/lock')
async def scheduler_lock():
  await scheduler.lock_scheduler()
  return {'state': 'locked'}


@app.post('/scheduler/unlock')
async def scheduler_lock():
  await scheduler.unlock_scheduler()
  return {'state': 'unlocked'}


@app.get('/scheduler')
async def scheduler_lock():
  return {'state': 'locked' if (await scheduler.is_scheduler_locked()) else 'unlocked'}


if __name__ == '__main__':
  config = uvicorn.Config("main:app", 
                          host=os.environ['APP_HOST'],
                          port=int(os.environ['APP_PORT']),
                          ssl_keyfile="./ssl/private.key",
                          ssl_certfile="./ssl/certificate.crt",
                          log_level="trace")

  server = uvicorn.Server(config)
  server.run()
