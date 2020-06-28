class Message():
    """ Slack message received through the API """

    def __init__(self, channel_type: str, user: str, content: str):
        """ Initializes the Message Object

        Args:
            channel_type (str): type of channel the message was sent in
            user (str): user that sent the message
            content (str): content of the message
        """

        self.channel_type = channel_type
        self.user = user
        self.content = content

    def __str__(self):
        return "[Message] in {} by {}: {}".format(
            self.channel_type, self.user, self.content
        )
