import discord
import mysql.connector
from mysql.connector import Error

class DataStorage:
    """Data storage class for Cats Cradle.
    
    TODO: Attributes and Representation Invariants
    """
    bot: discord.client

    def __init__(self, bot) -> None:
        self.bot = bot

    def store_cat(self, guild: discord.Guild, user: discord.User, cat: str) -> None:
        """Adds a cat to the database.

        Attributes:
        - guild: the id of the server of which the user executed the command.
        - user: the id of the user that exected the command.
        - cat: the cat type to be stored.

        Representation Invariants:
        - guild and user must be a valid discord id of length 18.
        - cat must be a valid cat type.
        """
        try:
            connection = mysql.connector.connect(host='localhost',
                                                    database='cats_cradle',
                                                    user='root',
                                                    password='root')
            mySql_Create_Table_Query = """CREATE TABLE DB_""" + str(guild) + """ (
                Id int(11) NOT NULL AUTO_INCREMENT,
                User varchar(18) NOT NULL,
                Cats varchar(5000) NOT NULL,
                PRIMARY KEY (ID))
                """
            cursor = connection.cursor()
            result = cursor.execute(mySql_Create_Table_Query)

        except mysql.connector.Error as error:
            print("Failed to create table in MySQL: {}".format(error))
        
        finally:
            if connection.is_connected():
                table = "DB_" + str(guild)
                mySQL_Insert_Row_Query = "INSERT INTO " + table + " (User, Cats) VALUES (%s, %s)"
                mySQL_Insert_Row_Values = (str(user), cat)

                cursor.execute(mySQL_Insert_Row_Query, mySQL_Insert_Row_Values)
                connection.commit()

                cursor.close()
                connection.close()

                print("Interaction complete, connections closed.")
    
    def retrive_cats(self, guild: discord.Guild, user = discord.User) -> dict[str, int]:
        """Retrieve the cats specific to the user from the database. Returns a dict of all the cats
        and their corresponding amounts.

        Representation Invariants:
        - guild and user must be a valid discord id of length 18.
        """
        table = "DB_" + str(guild)

        try:
            connection = mysql.connector.connect(host='localhost',
                                                    database='cats_cradle',
                                                    user='root',
                                                    password='root')
            
            cursor = connection.cursor()

            sql_select_query = "SELECT * from " + table + " WHERE User LIKE '"+ str(user) +"'"
            cursor.execute(sql_select_query)

            record = cursor.fetchall()

            cats = {}

            for row in record:
                cat = str(row[2])
                if cat not in cats:
                    cats[cat] = 1
                else:
                    cats[cat] += 1
            
            # TODO: turn this return into an embed
            return cats

        except mysql.connector.Error as error:
            print("Failed to get record from MySQL table: {}".format(error))
        
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("Connection closed.")


