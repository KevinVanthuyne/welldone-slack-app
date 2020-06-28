class Message():
    """ Slack message received through the API """

    def __init__(self, channel_type: str, user: str, content: str, blocks: dict):
        self.channel_type = channel_type
        self.user = user
        self.content = content
        self.blocks = blocks

    def __str__(self):
        return "[Message] in {} by {}: {}".format(
            self.channel_type, self.user, self.content
        )
