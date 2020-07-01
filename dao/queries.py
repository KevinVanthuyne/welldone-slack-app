class Queries():

    # Table creation

    CREATE_REWARD_TABLE = """CREATE TABLE IF NOT EXISTS rewards (
                                    id          INTEGER     PRIMARY KEY,
                                    sender      VARCHAR(32) NOT NULL,
                                    receiver    VARCHAR(32) NOT NULL,
                                    timestamp   TIMESTAMP   NOT NULL
                                );"""

    # Value insertion

    INSERT_REWARD = """INSERT INTO rewards (sender, receiver, timestamp)
                            VALUES (?, ?, ?);"""

    # Misc

    TABLE_EXISTS = """SELECT name FROM sqlite_master 
                            WHERE type='table' AND name='{}';"""

    COUNT_REWARDS_TODAY = """SELECT COUNT(id) FROM rewards
                             WHERE sender='{}' AND timestamp>=date('now','start of day')"""
