import os
import logging
from flask import Flask, Response, request
from slackeventsapi import SlackEventAdapter
from dotenv import load_dotenv
from datetime import datetime
from threading import Thread
import pprint

from model.message import Message
from model.reward import Reward
from service.message_service import MessageService
from service.reward_service import RewardService
from service.user_service import UserService
from service.command_service import CommandService
from service.scoreboard_blocks_service import ScoreboardBlocksService

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
command_service = CommandService()
scoreboard_blocks_service = ScoreboardBlocksService(
    message_service.KEYWORD, reward_service)


@slack_events_adapter.on("message")
def on_message(payload):
    handler_thread = Thread(target=_handle_message,
                            args=(payload,), daemon=True)
    handler_thread.start()
    return Response("Message received.", status=200)


@app.route('/slack/command/welldone', methods=['POST'])
def on_command():
    # TODO: check signing secret for auth

    response = _handle_command(request.form)

    if not response:
        return Response("Invalid command argument! Valid arguments are: `scoreboard`", 200)
    return Response(response, 200)


def _handle_message(payload):
    _pretty_print(payload)
    # try to extract a message from the payload and check if it was successful
    message = message_service.extract_message(payload)
    if not message:
        return

    # message should be sent in a public or private channel
    if not message_service.has_valid_channel_type(message):
        return

    # message should contain the reward keyword/emoji
    if not message_service.contains_keyword(message):
        return

    tagged_users = message_service.get_tagged_users(message)

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


def _handle_command(payload):
    _pretty_print(payload)

    # command should be valid
    command = command_service.extract_command(payload)
    if not command:
        return False

    payload = scoreboard_blocks_service.get_message_payload()
    # TODO send payload in channel that the command was posted in


def _pretty_print(obj):
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(obj)


if __name__ == "__main__":
    # Run Flask app
    app.run(port=3000)
