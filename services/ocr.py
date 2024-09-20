import os


async def extract_text(file_path: str) -> str:
  tesseract_backend_enabled = bool(os.environ['TESSERACT_BACKEND_ENABLED'])
  if tesseract_backend_enabled:
    from services.backend.tesseract.tesseract_backend import make_ocr
    return await make_ocr(file_path)
