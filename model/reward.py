from datetime import datetime


class Reward():
    """ Stores who gave the reward, who received it and when """

    def __init__(self, sender: str, receiver: str, timestamp: datetime):
        """
        Args:
            sender (str): user id of award sender
            receiver (str): user id of award receiver
            timestamp (datetime): timestamp when the award was given
        """
        self.sender = sender
        self.receiver = receiver
        self.timestamp = timestamp

    def __str__(self):
        return "[Reward] {} to {} at {}".format(
            self.sender, self.receiver, self.timestamp
        )
