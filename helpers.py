import re
from datetime import datetime
from tinydb import TinyDB, where

# Set up DB
db = TinyDB('db.json')

# ................
# Helper Functions
# ................


def today(format="%Y-%m-%d"):
    """
    Today's date in the requested format

    :return: str
    """
    return datetime.today().strftime(format)


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
        print('get_from_cache(): Exception: ', e)
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
        print('write_to_cache(): Exception: ', e)


def is_youtube_url(url):
    """
    Check if the URL is a YouTube URL

    :param url: URL to be checked
    :return: bool
    """
    return "youtube" in url


def yt_embed_to_playable(url):
    """
    Convert YouTube embed URL to YouTube view URL

    :param url: YouTube embed URL
    :return: str: YouTube view URL
    """
    if "youtube" in url and "embed" in url:
        pattern = re.compile("embed/(.*)\?")
        result = pattern.search(url)
        if result:
            return f'https://youtube.com/watch?v={result.group(1)}'
    return url


def parse_query(message, command):
    """
    Parse query from message
    :param message: Full message with command and
    :param command: Bot command
    :return: str: The query param after the bot message
    """
    return ''.join(message.split(command)[1:]).strip()


def is_date(date):
    """
    Check if the date is in the format mm/dd
    :param date: Date to be tested for the pattern
    :return: bool
    """
    pattern = re.compile('^\d\d/\d\d$')
    if pattern.match(date):
        return True
    return False
