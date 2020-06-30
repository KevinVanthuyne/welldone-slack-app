import os
import logging
from flask import Flask
from slackeventsapi import SlackEventAdapter
from dotenv import load_dotenv
from datetime import datetime

from model.message import Message
from model.reward import Reward
from service.message_service import MessageService
from service.reward_service import RewardService

LOGGER = logging.getLogger()

# Load environment variables from .env file
load_dotenv()

# Initialize a Flask app to host the events adapter
app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(
    os.getenv('SLACK_SIGNING_SECRET'), "/slack/events", app
)

# Initialize the services
message_service = MessageService(LOGGER)
reward_service = RewardService(LOGGER)


@slack_events_adapter.on("message")
def on_message(payload):
    _handle_message(payload)


def _handle_message(payload):
    event = payload["event"]
    message = Message(event["channel_type"], event["user"],
                      event["text"], event["blocks"])

    if not message_service.has_valid_channel_type(message):
        return

    if not message_service.contains_keyword(message):
        return

    tagged_users = message_service.get_tagged_users(message)
    reward = Reward(message.user, tagged_users[0], datetime.now())
    reward_service.give_reward(reward)
    success = message_service.send_reward_notification(
        message.user, tagged_users[0]
    )

    LOGGER.debug(success)


if __name__ == "__main__":
    # Setup logger
    LOGGER.setLevel(logging.DEBUG)
    LOGGER.addHandler(logging.StreamHandler())

    # Run Flask app
    app.run(port=3000)
