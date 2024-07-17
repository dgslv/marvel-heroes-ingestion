
class Query:
    raw_marvel_heroes = """
        INSERT INTO datalake.raw_marvel_heroes (ingestion_timestamp, payload)
        VALUES (%s, %s)
    """
    