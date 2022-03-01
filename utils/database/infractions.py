import utils.database.sql_queries as sql_queries
from utils.time import timestamp
from config import CONFIRM_PASS
import datetime
import asyncpg

CONNECTION = asyncpg.connection.Connection

async def insert(
    connection: CONNECTION,
    user_id: int,
    issuer_id: int,
    expiry_date: datetime.datetime,
    issue_date: datetime.datetime,
    action: str,
    reason: str = "No reason provided",
) -> int | None:
    """Inserts a infraction to the given user id in the database.
    Type: Coroutine
    Returns: int (case)
    """
    issue_timestamp = timestamp(issue_date)
    expiry_timestamp = timestamp(expiry_date)
    action = action.strip().casefold()
    reason = reason.strip().casefold()
    active = True

    case = await connection.fetchval(
        sql_queries.INSERT_INTO_INFRACTIONS,
        user_id,
        issuer_id,
        issue_timestamp,
        expiry_timestamp,
        active,
        action,
        reason
    )

    return case

async def expire(
    connection: CONNECTION,
    case: int
) -> None:
    """Sets the given record case active to false.
    Type: Coroutine
    Returns: None
    """
    await connection.execute(
        sql_queries.UPDATE_INFRACTIONS_ACTIVE,
        False,
        case
    )

async def fetch_from_case(
    connection: CONNECTION,
    case: int
) -> asyncpg.Record:
    """Fetches a record with the given case.
    Type: Coroutine
    Returns: asyncpg.Record
    """
    record = await connection.fetchrow(
        sql_queries.SELECT_ALL_FROM_INFRACTIONS_WHERE_CASE,
        case
    )
    return record

async def fetch_from_user(
    connection: CONNECTION,
    user_id: int
) -> list[asyncpg.Record]:
    """Fetches multiple records with the given user id.
    Type: Coroutine
    Returns: list[asyncpg.Record]
    """
    records = await connection.fetch(
        sql_queries.SELECT_ALL_FROM_INFRACTIONS_WHERE_USER_ID,
        user_id
    )
    return records

async def fetch_from_action(
    connection: CONNECTION,
    user_id: int,
    action: str
) -> list[asyncpg.Record]:
    """Fetches multiple records with the given action.
    Type: Coroutine
    Returns: list[asyncpg.Record]
    """
    records = await connection.fetch(
        sql_queries.SELECT_ALL_FROM_INFRACTIONS_WHERE_USER_ID_AND_ACTION,
        user_id,
        action
    )
    return records

async def delete_from_case(
    connection: CONNECTION,
    case: int
) -> str:
    """Deletes specific record with the given case.
    Warning: This is a dangerous function.
    Type: Coroutine
    Returns: str (confirmation password for optional safety check)
    """
    await connection.execute(
        sql_queries.DELETE_ALL_FROM_INFRACTIONS_WHERE_CASE,
        case
    )
    return CONFIRM_PASS

async def delete_from_user(
    connection: CONNECTION,
    user_id: int
) -> str:
    """Deletes every record with the given user id.
    Warning: This is a dangerous function.
    Type: Coroutine
    Returns: str (confirmation password for optional safety check)
    """
    await connection.execute(
        sql_queries.DELETE_ALL_FROM_INFRACTIONS_WHERE_USER_ID,
        user_id
    )
    return CONFIRM_PASS

async def delete_from_action(
    connection: CONNECTION,
    user_id: int,
    action: str
) -> str:
    """Deletes every record with the given action.
    Warning: This is a dangerous function.
    Type: Coroutine
    Returns: str (confirmation password for optional safety check)
    """
    await connection.execute(
        sql_queries.DELETE_ALL_FROM_INFRACTIONS_WHERE_USER_ID_AND_ACTION,
        user_id,
        action
    )
    return CONFIRM_PASS

async def delete_all(
    connection: CONNECTION
) -> str:
    """Deletes every record from the database.
    Warning: This is a dangerous function.
    Type: Coroutine
    Returns: str (confirmation password for optional safety check)
    """
    await connection.execute(
        sql_queries.DELETE_ALL_FROM_INFRACTIONS
    )
    return CONFIRM_PASS

async def active_check(
    connection: CONNECTION,
    user_id: int
) -> list:
    """Checks for any active infraction for a user.
    Type: Coroutine
    Returns: list with action names, if no active infractions found an empty list will be returned.
    """

    records: asyncpg.Record = await connection.fetch(
        sql_queries.SELECT_ALL_FROM_INFRACTIONS_WHERE_USER_ID,
        user_id
    )
    actions = []
    for record in records:
        field_name = ""
        for field, value in record.items():
            field_name = field
            if field == "active" and value is True:
                break
        else:
            continue
        for field, value in record.items():
            if field == field_name:
                actions.append(field)
                break
    return actions