import os
import pytesseract
from pdf2image import convert_from_path


async def make_ocr(file_path: str) -> str:
  tesseract_bin_path = os.environ['TESSERACT_BIN_PATH']
  tesseract_data_path = os.environ['TESSERACT_DATA_PATH']
  tesseract_lang = os.environ['TESSERACT_LANG']
  tessdata_dir_config = f'--tessdata-dir "{tesseract_data_path}"'
  poppler_bin_path = os.environ['POPPLER_BIN_PATH']
  pdf2image_dpi = int(os.environ['PDF2IMAGE_DPI'])
  pytesseract.pytesseract.tesseract_cmd = f"{tesseract_bin_path}/tesseract.exe"
  pages = convert_from_path(file_path, pdf2image_dpi, poppler_path=poppler_bin_path)
  return pytesseract.image_to_string(pages[0], lang=tesseract_lang, config=tessdata_dir_config)
