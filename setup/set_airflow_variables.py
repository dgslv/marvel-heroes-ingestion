from airflow.models import Variable
from src.config import logger
import os

logger.info("Insert Variables has started")

variables_to_set = {
    "MARVEL_API_KEY": os.getenv("MARVEL_API_KEY"),
    "MARVEL_PRIVATE_KEY": os.getenv("MARVEL_PRIVATE_KEY"),
    "POSTGRES_DATALAKE_HOST": os.getenv("POSTGRES_DATALAKE_HOST"),
    "POSTGRES_DATALAKE_PORT": os.getenv("POSTGRES_DATALAKE_PORT"),
    "POSTGRES_DATALKE_DBNAME": os.getenv("POSTGRES_DATALAKE_DBNAME"),
    "POSTGRES_DATALAKE_USER": os.getenv("POSTGRES_DATALAKE_USER"),
    "POSTGRES_DATALAKE_PASS": os.getenv("POSTGRES_DATALAKE_PASS"),
}

for key, value in variables_to_set.items():
    logger.info(f"Inserting {key} into Airflow Variables...")
    Variable.set(key, value)

logger.info("Insert Variables has finished")