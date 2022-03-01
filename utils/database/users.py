import utils.database.sql_queries as sql_queries
from utils.time import timestamp
import datetime
import asyncpg

CONNECTION = asyncpg.connection.Connection

async def on_join(
    connection: CONNECTION,
    user_id: int,
    join_date: datetime.datetime
) -> int:
    """Inserts additional information about the user on guild join.
    Type: Coroutine
    Returns: on join timestamp
    """
    joined_timestamp = timestamp(join_date)

    await connection.execute(
        sql_queries.INSERT_INTO_USERS,
        user_id,
        True,
        joined_timestamp
    )

    await connection.execute(
        sql_queries.INSERT_INTO_COLLECTIONS,
        user_id
    )

    return joined_timestamp

async def on_leave(
    connection: CONNECTION,
    user_id: int,
    left_date: datetime.datetime
) -> int:
    """Updates the leaving timestamp for the user.
    Type: Coroutine
    Returns: on leave timestamp
    """
    left_timestamp = timestamp(left_date)

    await connection.execute(
        sql_queries.UPDATE_USERS_LEFT_TIMESTAMP,
        left_timestamp,
        user_id
    )

    return left_timestamp

async def suspect(
    connection: CONNECTION,
    user_id: int
) -> tuple[int, int]:
    """Updates the suspicions value for the user.
    Type: Coroutine
    Returns: (new suspicions value, new total suspicions value)
    """
    active_suspicions = await connection.fetchval(
        sql_queries.SELECT_ACTIVE_SUSPICIONS_FROM_USERS,
        user_id
    )

    if not active_suspicions:
        active_suspicions = 0
    active_suspicions += 1

    total_suspicions = await connection.fetchval(
        sql_queries.SELECT_TOTAL_SUSPICIONS_FROM_USERS,
        user_id
    )

    if not total_suspicions:
        total_suspicions = active_suspicions

    await connection.execute(
        sql_queries.UPDATE_USERS_ACTIVE_SUSPICIONS,
        active_suspicions,
        user_id
    )

    await connection.execute(
        sql_queries.UPDATE_USERS_TOTAL_SUSPICIONS,
        total_suspicions,
        user_id
    )

    return active_suspicions, total_suspicions

async def appraise(
    connection: CONNECTION,
    user_id: int
) -> int:
    """Updates the appraise value for the user.
    Type: Coroutine
    Returns: (new appraise value)
    """
    appraises = await connection.fetchval(
        sql_queries.SELECT_APPRAISES_FROM_USERS,
        user_id
    )

    if not appraises:
        appraises = 0
    appraises += 1

    await connection.execute(
        sql_queries.UPDATE_USERS_APPRAISES,
        appraises,
        user_id
    )

    return appraises

async def unsuspect(
    connection: CONNECTION,
    user_id: int
) -> tuple[int, int]:
    """Updates the suspicions value for the user.
    Type: Coroutine
    Returns: (new suspicions value, new total suspicions value)
    """
    active_suspicions = await connection.fetchval(
        sql_queries.SELECT_ACTIVE_SUSPICIONS_FROM_USERS,
        user_id
    )

    if not active_suspicions:
        active_suspicions = 1
    active_suspicions -= 1

    total_suspicions = await connection.fetchval(
        sql_queries.SELECT_TOTAL_SUSPICIONS_FROM_USERS,
        user_id
    )

    if not total_suspicions:
        total_suspicions = active_suspicions

    await connection.execute(
        sql_queries.UPDATE_USERS_ACTIVE_SUSPICIONS,
        active_suspicions
    )

    return active_suspicions, total_suspicions

async def user_exists(
    connection: CONNECTION,
    user_id: int
) -> bool:
    selected_id = await connection.fetchval(
        sql_queries.SELECT_ID_FROM_USERS,
        user_id
    )
    if not selected_id:
        return False
    return True