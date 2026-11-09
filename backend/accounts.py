import re

from psycopg.errors import UniqueViolation
from werkzeug.security import (generate_password_hash, check_password_hash)

from backend.database import get_db_connection

def create_account(username, password):
    username = username.strip().lower()

    if not re.fullmatch(r"[a-z0-9_]{3,30}", username):
        raise ValueError("Username must contain 3-30 letters, numbers, or underscores.")

    if not 8 <= len(password) <= 128:
        raise ValueError("Password must contain 8-128 letters, numbers, underscores.")

    password_hash = generate_password_hash(password)

    try:
        with get_db_connection() as connection:
            account = connection.execute(
                """
                insert into business.accounts (username, password_hash)
                values (%s, %s)
                returning id, username
                """,
                (username, password_hash)
            ).fetchone()

    except UniqueViolation as error:
        if error.diag.constraint_name == "business_username_unique":
            raise ValueError("That username is already taken") from None
        raise 

    return {
        "id": str(account["id"]),
        "username": account["username"],
    }


def authenticate_account(username, password):
    username = username.strip().lower()

    if not re.fullmatch(r"[a-z0-9_]{3,30}", username):
        return None

    if not 8 <= len(password) <= 128:
        return None

    with get_db_connection() as connection: 
        account = connection.execute (
            """
            select id, username, password_hash
            from business.accounts
            where username = %s
            """,
            (username,),
        ).fetchone()

    if account is None:
        return None

    if not check_password_hash(account["password_hash"], password):
        return None

    return {
        "id": str(account["id"]),
        "username": account["username"],
    }