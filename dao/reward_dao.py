import sqlite3
from sqlite3 import Error
import logging

from model.reward import Reward


class RewardDao():
    """ Data access class for managing storage of Rewards """

    DATABASE_NAME = "welldone_database.db"
    INSERT_REWARD_QUERY = """INSERT INTO rewards (sender, receiver, timestamp)
                             VALUES (?, ?, ?);"""
    TABLE_EXISTS_QUERY = """SELECT name FROM sqlite_master 
                            WHERE type='table' AND name='{}';"""
    CREATE_REWARD_TABLE_QUERY = """CREATE TABLE IF NOT EXISTS rewards (
                                        id          INTEGER     PRIMARY KEY,
                                        sender      VARCHAR(32) NOT NULL,
                                        receiver    VARCHAR(32) NOT NULL,
                                        timestamp   TIMESTAMP   NOT NULL
                                    );"""

    def __init__(self):
        self.logger = logging.getLogger()
        self._create_database()

    def save(self, reward: Reward):
        """ Saves the reward to the database """
        try:
            with self._create_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(self.INSERT_REWARD_QUERY,
                               (reward.sender, reward.receiver, reward.timestamp))
                connection.commit()
                self.logger.info(
                    "Reward added to database: id:{} {}".format(cursor.lastrowid, reward))
                return True
        except Error as e:
            self.logger.error("Couldn't save reward to database: {}".format(e))
            return False

    def _create_database(self):
        """ Create the database if there is none and its tables to be able to 
            use it.
        """
        try:
            with self._create_connection() as connection:
                if not self._table_exists("rewards"):
                    self.logger.info("Couldn't find a database")
                    cursor = connection.cursor()
                    cursor.execute(self.CREATE_REWARD_TABLE_QUERY)
                    self.logger.info("Database created")
                else:
                    self.logger.info("Database detected")
                return True
        except Error as e:
            self.logger.error("Couldn't create database: {}".format(e))

    def _table_exists(self, table_name: str):
        """ Checks the database to see if a table exists """
        try:
            with self._create_connection() as connection:
                cursor = connection.cursor()
                # Table names can't be parameterized so .format() is used
                cursor.execute(self.TABLE_EXISTS_QUERY.format(table_name))
                if cursor.fetchone():
                    return True
        except Error as e:
            self.logger.error(
                "Couldn't check if table exists in database: {}".format(e))
        return False

    def _create_connection(self):
        """ Tries to open a connection to the database and returns the
            connection object. Warning: it does not close the connection,
            this has to be done manually.
        """
        try:
            return sqlite3.connect(self.DATABASE_NAME)
        except Error as e:
            self.logger.error("Couldn't connect to database: {}".format(e))
