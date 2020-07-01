class Queries():
    INSERT_REWARD = """INSERT INTO rewards (sender, receiver, timestamp)
                            VALUES (?, ?, ?);"""

    TABLE_EXISTS = """SELECT name FROM sqlite_master 
                            WHERE type='table' AND name='{}';"""

    CREATE_REWARD_TABLE = """CREATE TABLE IF NOT EXISTS rewards (
                                        id          INTEGER     PRIMARY KEY,
                                        sender      VARCHAR(32) NOT NULL,
                                        receiver    VARCHAR(32) NOT NULL,
                                        timestamp   TIMESTAMP   NOT NULL
                                    );"""
