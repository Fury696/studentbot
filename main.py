from asyncio import set_event_loop_policy, WindowsSelectorEventLoopPolicy
from config import TOKEN, DB_USER, DB_PASS, DB_HOST, DB_PORT
import utils.database.sql_queries as sql_queries
from disnake.utils import search_directory
from disnake.ext import commands
from disnake import Intents
import asyncpg


__author__ = "Yerlikaya"
__license__ = "MIT"


set_event_loop_policy(WindowsSelectorEventLoopPolicy())

class StudentBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            intents=Intents.all(),
            test_guilds=[937485181705666590],
            sync_commands_debug=True
        )
        # Type Annotate 'connection' to avoid linter type warnings later.
        self.connection: asyncpg.connection.Connection

    def setup(self) -> None:
        # load every module (that is recognised as a package) in the cogs. (include a __init__.py for cog directories)
        # avoiding modules that starts with '_' or is not a python file.
        for module in search_directory('cogs'):
            if not module.endswith(".py") or module.split(".")[-1].startswith("_"):
                continue
            self.load_extension(module)

    async def start(self, token, reconnect) -> None:
        """This method is overriding the default 'commands.Bot.start' method."""

        # Establishes one connection with private credentials to PostGreSQL
        # beta: updating to connection pools in later versions.
        self.connection = await asyncpg.connect(
            host=DB_HOST,
            database=DB_USER,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT
        )

        # Get important queries from utils.database.sql_queries including creating necessary tables.
        boot_queries = "\n".join([
            sql_queries.CREATE_TABLE_USERS,
            sql_queries.CREATE_TABLE_COLLECTIONS,
            sql_queries.CREATE_TABLE_INFRACTIONS,
            sql_queries.CREATE_TABLE_REPORTS
        ])

        await self.connection.execute(boot_queries)

        # Calling the default start method to not cause conflicts.
        await super().start(token, reconnect=reconnect)

    def run(self) -> None:
        self.setup()
        super().run(TOKEN, reconnect=True)


if __name__ == "__main__":
    bot = StudentBot()
    bot.run()
