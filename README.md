# WellDone! Slack App
Slack app for rewarding people with bacon as a way of saying thanks.

## Setup
Run `pip3 install -r requirements.txt` to install all dependencies.

Run `python3 app.py` to start the Flask server that gets called by Slack when new messages are posted.

### Local setup 

Download [ngrok](https://ngrok.com/) and run it with `.\ngrok.exe http <flask-port>` (the default Flask port is 3000). After ngrok is started copy the https link.

Go to the app's configuration page on https://api.slack.com/apps/, click "Event Subscriptions" and change the "Request URL" to the ngrok URL with `/slack/events` appended.