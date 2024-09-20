import os
from anonymization import Anonymization, \
                          AnonymizerChain, \
                          PhoneNumberAnonymizer, \
                          NamedEntitiesAnonymizer, \
                          EmailAnonymizer


async def make_anonimization(text: str) -> str:
  anonimization_enabled = os.environ['ANONIMIZATION_ENABLED']
  if not anonimization_enabled:
    return text
  
  anon = Anonymization('ru_RU')
  anon_chain = AnonymizerChain(anon)
  anon_chain.add_anonymizers(NamedEntitiesAnonymizer('ru_core_news_lg'), PhoneNumberAnonymizer, EmailAnonymizer)
  fake_text = anon_chain.anonymize(text)
  return fake_text
