class ScoreboardBlocksService:
    """ Generates the Slack blocks for the scoreboard """

    SCOREBOARD_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "Top :bacon: givers:"
            ),
        },
    }

    def __init__(self, reward_keyword, reward_service):
        self.reward_keyword = reward_keyword
        self.reward_service = reward_service

    def get_message_payload(self):
        return {
            # "ts": self.timestamp,
            # "channel": self.channel,
            # "username": self.username,
            # "icon_emoji": self.icon_emoji,
            "blocks": [
                self.SCOREBOARD_BLOCK,
            ],
        }
