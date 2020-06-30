import sqlite3
from sqlite3 import Error
import logging

from model.reward import Reward


class RewardDao():
    """ Data access class for managing storage of Rewards """

    def __init__(self):
        self.logger = logging.getLogger()

    def _create_connection(self):
        """ Tries to open a connection to the database and returns the
            connection object. Warning: it does not close the connection,
            this has to be done manually
        """
        try:
            return sqlite3.connect('test.db')
        except Error as e:
            self.logger.error("Couldn't connect to database: {}".format(e))

    def save(self, reward: Reward):
        """ Saves the reward to the database """
        try:
            with self._create_connection() as connection:
                query = """INSERT INTO rewards (sender, receiver, timestamp)
                            VALUES (?, ?, ?);"""
                cursor = connection.cursor()
                cursor.execute(query, reward)
                self.logger.info(
                    "Reward {} added to database".format(cursor.lastrowid))
        except Error as e:
            self.logger.error("Couldn't save reward to database: {}".format(e))
