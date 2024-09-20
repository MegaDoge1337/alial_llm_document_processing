from pydantic import BaseModel


class ProcessFileRequest(BaseModel):
    file_name: str


class CalculationTokensRequest(BaseModel):
    text: str


class UploadFileResponse():
    file_name: str


class CalculationTokensResponse():
    amount: int
