import requests
import time as t
import json
import hashlib

from .config import Environment, logger, TLSAdapter
from .datalake.core import Datalake

env = Environment()
datalake = Datalake()

def get_hash(timestamp, public_key, private_key): 
    return hashlib.md5(
        (timestamp + private_key + public_key).encode('utf-8')
    ).hexdigest()

def get_heroes(offset=0, limit=100):
    try:
        logger.info(f"Getting heroes...")
        
        api_key = env.get_value("MARVEL_API_KEY")
        private_key = env.get_value("MARVEL_PRIVATE_KEY")
        timestamp = str(int(t.time()))
        _hash = get_hash(timestamp, api_key, private_key)
        
        with requests.session() as s:
            s.mount("https://", TLSAdapter())
            data = s.get(
                f"https://gateway.marvel.com:443/v1/public/characters?ts={timestamp}&apikey={api_key}&hash={_hash}&limit={limit}&offset={offset}"
            ).json()['data']
    
            logger.info(f"Total heroes got: {len(data['results'])}")

            return data
    except Exception as e:
        raise e


def insert_heroes_into_lake(heroes):
    try:
        logger.info(f"Inserting heroes into datalake...")
        timestamp = int(t.time())

        datalake\
            .insert_data("raw_marvel_heroes",
                         list(
                             map(lambda hero: (timestamp, json.dumps(hero)), heroes)
                         ))
    except Exception as e:
        logger.info(f"Error trying to insert heroes into datalake... :-(")
        raise e


def heroes_pipeline(offset=0):
    logger.info(f"Running Heroes Ingestion at Offset: {offset}")
    
    try:
        result = get_heroes(offset)

        heroes = result['results']
        
        insert_heroes_into_lake(heroes)

        if result['offset'] > result['total']:
            logger.info(f"Heroes Ingestion Finished")
        else:
            heroes_pipeline(
                offset=offset + result['limit']
            )

        return 1
    except Exception as e:
        logger.info(f"Heroes Ingestion Failed. Exiting..")
        raise e