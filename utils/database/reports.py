import utils.database.sql_queries as sql_queries
from utils.time import timestamp
import datetime
import asyncpg

CONNECTION = asyncpg.connection.Connection

async def insert(
    connection: CONNECTION,
    user_id: int,
    issuer_id: int,
    issue_date: datetime.datetime,
    reason: str = "No reason provided"
) -> int | None:
    """Inserts a report to the given user id in the databse.
    Type: Coroutine
    Returns: int (case)
    """
    reason = reason.strip().casefold()
    issue_timestamp = timestamp(issue_date)
    case = await connection.fetchval(
        sql_queries.INSERT_INTO_REPORTS,
        user_id,
        issuer_id,
        issue_timestamp,
        reason
    )
    return case

async def get_report(
    connection: CONNECTION,
    case: int
) -> asyncpg.Record | None:
    """Fetches one single report with the case id given.
    Type: Coroutine
    Returns: asyncpg.Record (Record object) or None
    """
    record = await connection.fetchrow(
        sql_queries.SELECT_ALL_FROM_REPORTS_WHERE_CASE,
        case
    )
    return record

async def get_reports(
    connection: CONNECTION,
    user_id: int
) -> list[asyncpg.Record] | None:
    """Fetches multiple reports from the given user id.
    Type: Coroutine
    Returns: a list of asyncpg.Record objects or None
    """
    records = await connection.fetch(
        sql_queries.SELECT_ALL_FROM_REPORTS_WHERE_USER_ID,
        user_id
    )
    return records
