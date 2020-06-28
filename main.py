import os
import logging
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize a Flask app to host the events adapter
app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(
    os.getenv('SLACK_SIGNING_SECRET'), "/slack/events", app
)

# Initialize a Web API client
slack_web_client = WebClient(token=os.getenv('SLACK_BOT_TOKEN'))


@slack_events_adapter.on("message.channels")
def on_message_in_channel(payload):
    _handle_message(payload)


@slack_events_adapter.on("message.groups")
def on_message_in_private_channel(payload):
    _handle_message(payload)


def _handle_message(payload):
    logging.debug(payload)

    # event = payload.get("event", {})

    # # Get the id of the Slack user associated with the incoming event
    # user_id = event.get("user", {}).get("id")

    # # Open a DM with the new user.
    # response = slack_web_client.im_open(user_id)
    # channel = response["channel"]["id"]


if __name__ == "__main__":
    # Setup logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())

    # Run Flask app
    app.run(port=3000)
