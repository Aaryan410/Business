from backend.database import get_db_connection

with get_db_connection() as connection:
    result = connection.execute (
        "select to_regclass(%s) as account_table",
        ("business.accounts",),
    ).fetchone()

    print(result)