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
from service.user_service import UserService

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(logging.StreamHandler())

# Load environment variables from .env file
load_dotenv()

# Initialize a Flask app to host the events adapter
app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(
    os.getenv('SLACK_SIGNING_SECRET'), "/slack/events", app
)

# Initialize the services
user_service = UserService()
message_service = MessageService(user_service)
reward_service = RewardService()


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

    if (reward_service.give_reward(reward)):
        success = message_service.send_reward_notification(
            message.user, tagged_users[0]
        )


if __name__ == "__main__":
    # Run Flask app
    app.run(port=3000)
