import re
from datetime import datetime
from tinydb import TinyDB, where

# Set up DB
db = TinyDB('db.json')

# ................
# Helper Functions
# ................


def today():
    """
    Today's date in the format 2021-03-15
    :return: str
    """
    return datetime.today().strftime("%Y-%m-%d")


def get_from_cache(table_name, key, value):
    """
    Query the database to see if the result is already cached

    :param table_name: Name of the db table
    :param key: Name of the table column to query against
    :param value: Value of the table column to compare with
    :return: Document if exists else None
    """
    try:
        table = db.table(table_name)
        return table.get(where(key) == value)
    except Exception as e:
        print('get_from_cache: Exception: ', e)
        return None


def write_to_cache(table_name, document, upsert_key=None):
    """
    Save a document in cache to be retrieved later

    :param table_name: Name of the db table
    :param document: dict of the document to be stored
    :param upsert_key: name of the key to be queried to check if the
    document has to upserted or inserted
    """
    try:
        table = db.table(table_name)
        if upsert_key:
            table.upsert(document, where(upsert_key) == document[upsert_key])
        else:
            table.insert(document)
        print(f'write_to_cache(): {table_name} saved to cache!')
    except Exception as e:
        print('write_to_cache: Exception: ', e)


def is_youtube_url(url):
    return "youtube" in url


def yt_embed_to_playable(url):
    if "youtube" in url and "embed" in url:
        pattern = re.compile("embed/(.*)\?")
        result = pattern.search(url)
        if result:
            return f'https://youtube.com/watch?v={result.group(1)}'
    return url
