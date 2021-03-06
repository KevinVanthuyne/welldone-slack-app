import os
import logging
from slack import WebClient
from slack.errors import SlackApiError

from model.message import Message
from service.user_service import UserService


class MessageService():
    """ Service for handling Message objects """

    KEYWORD = ":bacon:"

    def __init__(self, user_service: UserService):
        """ Initializes the MessageService with logger and a Slack WebClient """
        self.logger = logging.getLogger()
        self.user_service = user_service
        self.slack_web_client = WebClient(token=os.getenv('SLACK_BOT_TOKEN'))

    def extract_message(self, payload):
        """ Extract a message object from the payload object that gets sent by
            Slack. Returns a Message object if it was successful, None if it 
            wasn't.
        """
        # if payload doesn't contain "event" key stop handling message
        if not "event" in payload:
            return None
        event = payload["event"]

        # if event doesn't contain necessary keys stop handling message
        if not event.keys() >= {"channel_type", "user", "text", "blocks"}:
            return
        return Message(event["channel_type"], event["user"],
                       event["text"], event["blocks"])

    def has_valid_channel_type(self, message: Message):
        """ Checks if a message was sent in a public or private channel """
        return message.channel_type == "channel" or message.channel_type == "group"

    def contains_keyword(self, message: Message):
        """ Checks if the message contains the keyword/emoji that triggers
            rewarding a user
        """
        return MessageService.KEYWORD in message.content

    def get_tagged_users(self, message: Message):
        """ Get the user id's from all tagged users in the message with the
            duplicate user id's removed
        """
        user_ids = []
        for element in message.blocks[0]["elements"][0]["elements"]:
            if element["type"] == "user":
                user_ids.append(element["user_id"])
        return list(dict.fromkeys(user_ids))

    def send_reward_notifications(self, sender: str, receivers: list):
        """ Sends a DM to the receivers to notify them that they received a
            reward from someone

        Args:
            sender (str): user id of the person that sent the reward
            receivers (list[str]): array of user ids of the people that got
                                   tagged in the reward message
        """
        responses = []
        for receiver in receivers:
            responses.append(self.send_reward_notification(sender, receiver))

        return False not in responses

    def send_reward_notification(self, sender: str, receiver: str):
        """ Sends a DM to the receiver to notify them that they received a
            reward from someone

        Args:
            sender (str): user id of the person that sent the :bacon:
            receiver (str): array of user ids of the people that got
                                  tagged in the reward message
        """
        try:
            open_response = self.slack_web_client.conversations_open(
                users=[receiver]
            )

            channel_id = open_response["channel"]["id"]
            user = self.user_service.get_user_info(sender)
            self.slack_web_client.chat_postMessage(
                channel=channel_id,
                text="You got a {} from {}. Well done!".format(
                    self.KEYWORD, user["real_name"])
            )

            self.slack_web_client.conversations_close(
                channel=channel_id
            )
            self.logger.info(
                "Sent a reward notification from {} to {}".format(
                    sender, receiver)
            )

            return True
        except SlackApiError as e:
            self.logger.error("Reward notification sending failed.")
            self.logger.error(e)
            return False
