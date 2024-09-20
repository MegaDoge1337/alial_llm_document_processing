import os
import logging
import aiofiles
import json
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import LlamaCpp


async def postprocessing(completion: str) -> dict:
    config_path = os.environ['LLAMACPP_POSTPROCESSING_CONFIG']
    config_file = await aiofiles.open(f'./configs/{config_path}', 'r', encoding='utf8')
    config = json.loads(await config_file.read())

    async def search_target(text: str, target: str) -> str:
        entry_exists = target in text
        if not entry_exists:
            return ''
        target_start = text.find(target) + len(target)
        value = ''
        for i in range(target_start, len(text)):
            if text[i] in config['stop']:
                return value
            elif text[i] in config['ignore']:
                continue
            else:
                value += text[i]
        return value.rstrip().strip()
    
    data = {}
    for target in config['targets']:
        data[target] = await search_target(completion, target)
    return data


async def make_completion(file_text: str, prompt_template: str, model_path: str) -> dict:
    template = PromptTemplate(
       input_variables=['file_text'],
       template=prompt_template
    )

    llm = LlamaCpp(
      model_path=model_path,
      n_ctx=8192,
      n_batch=8192,
      n_gpu_layers=-1,
      n_threads=4,
      temperature=0,
      max_tokens=500,
      top_p=0.95,
      top_k=10,
      seed=-1
    )

    chain = LLMChain(llm=llm, prompt=template, output_key='json')
    response = chain({'file_text': file_text})
    logging.debug(f'{__name__}.make_completion: {response["json"]}')
    postresponse = await postprocessing(response['json'])
    logging.debug(f'{__name__}.postprocessing: {postresponse}')
    return postresponse
