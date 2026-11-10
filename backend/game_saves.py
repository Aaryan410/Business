import re

from backend.database import get_db_connection

def load_game(account_id):
    with get_db_connection() as connection:
        save = connection.execute (
            """
            select money, multiplier, multiplier_cost,
                   income_multiplier, income_multiplier_cost
            from business.game_saves
            where account_id = %s
            """,
            (account_id,)
        ).fetchone()

    if save is None:
        return None

    return {
        "money": save["money"],
        "multiplier": save["multiplier"],
        "multiplierCost": save["multiplier_cost"],
        "incomeMultiplier": save["income_multiplier"],
        "incomeMultiplierCost": save["income_multiplier_cost"],
    }


def save_game(acount_id, data):
    if not isinstance(data, dict):
        raise ValueError("Save data must be a JSON object")

    required_fields = [
        "money",
        "multiplier",
        "multiplierCost",
        "incomeMultiplier",
        "incomeMultiplierCost",
    ]

    for key in required_fields:
        value = data.get(key)

        pattern = r"[0-9]+" if key == "money" else r"[1-9][0-9]*"

        if not isinstance(value, str) or not re.fullmatch(pattern, value):
            raise ValueError(f"Invalid save value: {key}.")

    with get_db_connection() as connection:
        connection.execute(
            """
            insert into business.game_saves (
                account_id,
                money,
                multiplier,
                multiplier_cost,
                income_multiplier,
                income_multiplier_cost
            )
            values (%s, %s, %s, %s, %s, %s)

            on conflict (account_id) do update set
                money = excluded.money,
                multiplier = excluded.multiplier,
                multiplier_cost = excluded.multiplier_cost,
                income_multiplier = excluded.income_multiplier,
                income_multiplier_cost = excluded.income_multiplier_cost,
                updated_at = now()
            """,
            (
                account_id,
                data["money"],
                data["multiplier"],
                data["multiplierCost"],
                data["incomeMultiplier"],
                data["incomeMultiplierCost"],
            ),
        )