import os
import logging
from flask import Flask
from slackeventsapi import SlackEventAdapter
from dotenv import load_dotenv
from datetime import datetime
import pprint

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
    # TODO: filter out channel_join messages and others
    # TODO: handle response: https://api.slack.com/events-api#responding_to_events
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(payload)
    event = payload["event"]
    message = Message(event["channel_type"], event["user"],
                      event["text"], event["blocks"])

    # message should be sent in a public or private channel
    if not message_service.has_valid_channel_type(message):
        return

    # message should contain the reward keyword/emoji
    if not message_service.contains_keyword(message):
        return

    tagged_users = message_service.get_tagged_users(
        message)  # TODO: filter out bot itself
    print(tagged_users)

    for tagged_user in tagged_users:
        # if the user giving rewards has reached the daily limit, stop giving rewards
        if not reward_service.can_give_reward(message.user):
            break

        # otherwise give the reward and send a notification to the receiver
        reward = Reward(message.user, tagged_user, datetime.now())
        if reward_service.give_reward(reward):
            message_service.send_reward_notification(
                message.user, tagged_users[0]
            )


if __name__ == "__main__":
    # Run Flask app
    app.run(port=3000)
