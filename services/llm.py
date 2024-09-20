import os
from typing import Tuple
import database.management as dbm


async def process_document(file_text: str, is_reprocessing: bool = False, doctype_id: int = None) -> Tuple[dict, dict]:
  llamacpp_backend_enabled = bool(os.environ['LLAMACPP_BACKEND_ENABLED'])
  
  if llamacpp_backend_enabled:
    from services.backend.llm.llamacpp_backend import make_completion
    model_path = os.environ['LLAMACPP_MODEL_PATH']
    classification = {}
    extraction = {}

    if not is_reprocessing:
      classification_prompt = await dbm.get_classification_prompt()
      classification = await make_completion(file_text, 
                                  classification_prompt,
                                  model_path)
    else:
      doctype = await dbm.get_doctype_name_by_id(doctype_id)
      classification['DocType'] = doctype
    
    if doctype_id == None:
      doctype_id = await dbm.get_doctype_id_by_name(classification['DocType'].strip().rstrip().capitalize())

    extraction_prompt = await dbm.get_extraction_prompt_by_doctype(doctype_id)
    extraction = await make_completion(file_text, 
                                 extraction_prompt,
                                 model_path)
    
    return classification, extraction
