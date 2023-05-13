""" Cat's Cradle

This module contains classes representing an asynchronous SQLite connection.

Written by Edric Liu.
"""

from typing import Optional
from user import User
import aiosqlite


# Constants for table and column names.
USER_TABLE = "Users"
USER_ID_COL = "uid"
USER_POSITION_COL = "position"  # currently unused

CAT_RELATION_TABLE = "OwnedCats"
CAT_TYPE_COL = "cat"
CAT_COUNT_COL = "number"


class Database:
    """ Represents an asynchronous SQLite connection with wrapped SQL queries.
    Instances of this class must first call the load() method with valid arguments before using other methods.

    Users and cats share a one-to-many relationship; each user has many cats, but each instance of a cat has only one user that owns it.
    
    Contains methods for adding, retrieving, updating, and checking if the database contains users.
    """

    _db: Optional[aiosqlite.Connection]
    _ready: bool

    def __init__(self) -> None:
        """ Constructs a new Database. 
        Note that the asynchronous load() method must be called before methods can be used.
        """

        self._db = None
        self._ready = False

    async def is_ready(self) -> bool:
        """ Returns whether the database is ready; i.e. whether the load() method has been called yet.

        Asynchronous method.
        """

        return self._ready

    async def load(self, file_path: str) -> bool:
        """ Opens a connection to a new database from a given file.
        The database being ready does not negate future calls to this method; the database simply reloads its connection.

        Asynchronous method.
        """

        self._db = await aiosqlite.connect(file_path)

        await self._create_user_table()
        await self._create_cat_table()

        await self._db.commit()
        self._ready = True

    async def _create_user_table(self) -> None:
        """ Private method to create the user table. Note that cats are not stored in this table.

        Preconditions:
        - self.is_ready()

        Asynchronous method.
        """

        await self._db.execute(f"CREATE TABLE IF NOT EXISTS {USER_TABLE} (\
                                {USER_ID_COL} INTEGER PRIMARY KEY NOT NULL \
                                )")

    async def _create_cat_table(self) -> None:
        """ Private method to create the user-cat relational table.

        Preconditions:
        - self.is_ready()

        Asynchronous method.
        """

        await self._db.execute(f"CREATE TABLE IF NOT EXISTS {CAT_RELATION_TABLE} (\
                                {USER_ID_COL} INTEGER NOT NULL, \
                                {CAT_TYPE_COL} TEXT, \
                                {CAT_COUNT_COL} INTEGER, \
                                FOREIGN KEY ({USER_ID_COL}) \
                                    references {USER_TABLE} ({USER_ID_COL}) \
                                PRIMARY KEY ({USER_ID_COL}, {CAT_TYPE_COL}))")


    async def contains_user(self, id: int) -> bool:
        """ Returns whether the database contains a user by their ID. Throws DatabaseException if this database is not ready.

        Asynchronous method.
        """

        if not await self.is_ready():
            raise DatabaseException("Database not ready.")

        cursor = await self._db.execute(f"SELECT EXISTS(SELECT 1 FROM {USER_TABLE} WHERE {USER_ID_COL}={id})")
        result = await cursor.fetchone()
        return result[0] == 1

    async def add_user(self, user: User) -> None:
        """ Inserts a new user into the database. If the user already exists, their
        entry is updated instead through the update_user() method. Throws DatabaseException if this database is not ready.

        Asynchronous method.
        """

        if not await self.is_ready():
            raise DatabaseException("Database not ready.")
        
        if await self.contains_user(user.id):
            self.update_user(user)
            return

        async with self._db.cursor() as cursor:
            await cursor.execute(f"INSERT INTO {USER_TABLE} ({USER_ID_COL}) VALUES ({user.uid})")

            # This should not occur in normal gameplay.
            # The User class is a cache of the data in the database; new users should not have any cats.
            cats = user.get_cats()
            if len(cats) > 0:
                # Formats user inventory into SQL parameters, e.g. (cat, count), (cat, count), ...
                inventory = [
                    f"({user.uid}, \"{cat}\", {user.cats[cat]})"
                    for cat
                    in cats
                ]

                values = str.join(', ', inventory)
                await cursor.execute(f"INSERT INTO {CAT_RELATION_TABLE} \
                                     ({USER_ID_COL}, {CAT_TYPE_COL}, {CAT_COUNT_COL}) \
                                     VALUES {values}")

            await self._db.commit()


    async def update_user(self, user: User) -> None:
        """ Updates a user's inventory. If the user does not exist, their entry is added through the add_user() method.
        Throws DatabaseException if this database is not ready.
        """

        if not await self.is_ready():
            raise DatabaseException("Database not ready.")

        if not await self.contains_user(user.uid):
            self.add_user(user)
            return

        async with self._db.cursor() as cursor:
            cats = user.get_cats()
            for cat in cats:
                values = f"{user.uid}, \"{cat}\", {cats[cat]}"
                await cursor.execute(f"INSERT INTO {CAT_RELATION_TABLE} \
                                     ({USER_ID_COL}, {CAT_TYPE_COL}, {CAT_COUNT_COL}) \
                                     VALUES ({values}) \
                                     ON CONFLICT({USER_ID_COL}, {CAT_TYPE_COL}) \
                                     DO UPDATE SET {CAT_COUNT_COL}={cats[cat]}")

            await self._db.commit()



    async def get_user(self, id: int) -> Optional[User]:
        """ Returns a user from the database by ID. If the user does not exist, returns None. 
        Throws DatabaseException if this database is not ready.

        Asynchronous method.
        """

        if not await self.is_ready():
            raise DatabaseException("Database not ready.")

        if not await self.contains_user(id):
            return None

        cats = {}

        async with self._db.execute(f"SELECT {CAT_TYPE_COL}, {CAT_COUNT_COL} \
                                    FROM {CAT_RELATION_TABLE} \
                                    WHERE {USER_ID_COL} = {id}") as cursor:
            async for row in cursor:
                cat = row[0]
                number = row[1]

                cats[cat] = number

        return User(id, cats)


class DatabaseException(Exception):
    """ Represents an exception when using the Database class.
    """

    message: str

    def __init__(self, message: str) -> None:
        """ Creates a DatabaseException with a given message.
        """

        super().__init__()
        self.message = message

    def __str__(self) -> str:
        return self.message
