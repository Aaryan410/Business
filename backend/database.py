import os

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row
from urllib.parse import urlsplit, parse_qsl, urlencode

load_dotenv()

def get_db_connection():
    database_url = os.getenv("POSTGRES_URL")

    if not database_url:
        raise RuntimeError("POSTGRES_URL is missing from your environment.")

    parts = urlsplit(database_url)

    query_parameters = [
        (key, value)
        for key, value in parse_qsl(
            parts.query,
            keep_blank_values = True,
        )
        if key != "supa"
    ]

    database_url = parts._replace(
        query = urlencode(query_parameters)
    ).geturl()

    return psycopg.connect (
        database_url, 
        sslmode = "require",
        connect_timeout = 10,
        prepare_threshold = None,
        row_factory = dict_row,
    )