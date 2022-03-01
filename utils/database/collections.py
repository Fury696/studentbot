import utils.database.sql_queries as sql_queries
from utils.time import timestamp
import datetime
import asyncpg

CONNECTION = asyncpg.connection.Connection

async def message_count_update(
    connection: CONNECTION,
    user_id: int,
    message_date: datetime.datetime
) -> tuple[int, int]:
    """Update message count and last message timestamp.
    Type: Coroutine
    Returns: (new message count, new last msg timestamp)
    """

    messages = await connection.fetchval(
        sql_queries.UPDATE_COLLECTIONS_MESSAGES,
        user_id
    )

    if not messages:
        messages = 0
    messages += 1

    last_message_timestamp = timestamp(message_date)

    await connection.execute(
        sql_queries.UPDATE_COLLECTIONS_MESSAGES,
        messages,
        user_id
    )
    await connection.execute(
        sql_queries.UPDATE_COLLECTIONS_LAST_MESSAGE_TIMESTAMP,
        last_message_timestamp,
        user_id
    )

    return messages, last_message_timestamp

async def update_bad_words(
    connection: CONNECTION,
    user_id: int
) -> int:
    """Updates bad words count at collections.
    Type: Coroutine
    Returns: new bad words count
    """
    bad_words = await connection.fetchval(
        sql_queries.SELECT_BAD_WORDS_FROM_COLLECTIONS,
        user_id
    )

    if not bad_words:
        bad_words = 0

    bad_words += 1

    await connection.execute(
        sql_queries.UPDATE_COLLECTIONS_BAD_WORDS,
        bad_words,
        user_id
    )

    return bad_words

async def get_message_count(
    connection: CONNECTION,
    user_id: int
) -> int:
    """Fetches message count.
    Type: Coroutine
    Returns: message count
    """
    message_count = await connection.fetchval(
        sql_queries.SELECT_MESSAGES_FROM_COLLECTIONS,
        user_id
    )

    if not message_count:
        message_count = 0

    return message_count

async def get_last_message_timestamp(
    connection: CONNECTION,
    user_id: int
) -> int | None:
    """Fetches last message timestamp.
    Type: Coroutine
    Returns: timestamp or None"""
    last_message_timestamp = await connection.fetchval(
        sql_queries.SELECT_LAST_MESSAGE_TIMESTAMP_FROM_COLLECTIONS,
        user_id
    )

    if not last_message_timestamp:
        last_message_timestamp = None
    
    return last_message_timestamp

async def get_bad_words_count(
    connection: CONNECTION,
    user_id: int
) -> int:
    """Fetches bad words count.
    Type: Coroutine
    Returns: bad words count
    """
    bad_words_count = await connection.fetchval(
        sql_queries.SELECT_BAD_WORDS_FROM_COLLECTIONS,
        user_id
    )

    if not bad_words_count:
        bad_words_count = 0

    return bad_words_count