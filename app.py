import os
import logging
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from dotenv import load_dotenv
import pprint

from model.message import Message

LOGGER = logging.getLogger()

# Load environment variables from .env file
load_dotenv()

# Initialize a Flask app to host the events adapter
app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(
    os.getenv('SLACK_SIGNING_SECRET'), "/slack/events", app
)

# Initialize a Web API client
slack_web_client = WebClient(token=os.getenv('SLACK_BOT_TOKEN'))


@slack_events_adapter.on("message")
def on_message(payload):
    _handle_message(payload)


def _handle_message(payload):
    # debug print
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(payload)

    event = payload["event"]
    message = Message(event["channel_type"], event["user"], event["text"])

    if not (message.channel_type == "channel" or message.channel_type == "group"):
        return

    LOGGER.debug(message)


if __name__ == "__main__":
    # Setup logger
    LOGGER.setLevel(logging.DEBUG)
    LOGGER.addHandler(logging.StreamHandler())

    # Run Flask app
    app.run(port=3000)
