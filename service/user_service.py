import os
import logging
from slack import WebClient
from slack.errors import SlackApiError


class UserService():

    # TODO: users can give 5 rewards per day

    def __init__(self):
        """ Initializes the MessageService with logger and a Slack WebClient """
        self.logger = logging.getLogger()
        self.slack_web_client = WebClient(token=os.getenv('SLACK_BOT_TOKEN'))

    def get_user_info(self, user_id: str):
        """ Gets the user object of the corresponding user id. """
        try:
            return self.slack_web_client.users_info(user=user_id)["user"]
        except SlackApiError as e:
            self.logger.error("Could not retrieve user info.")
            self.logger.error(e)
            return None
