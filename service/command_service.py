import logging

from model.command import Command
from model.command_argument import CommandArgument


class CommandService():
    """ Service for handling commands sent to the app """

    COMMAND = 'welldone'  # The command that triggers the bot

    def __init__(self):
        self.logger = logging.getLogger()

    def extract_command(self, payload):
        """ Extract a command object from the payload object that gets sent by
            Slack. Returns a Command object if it was successful, None if it 
            wasn't.
        """
        try:

            # If it is not the correct command trigger, return None
            command = payload["command"]
            if command != "/{}".format(self.COMMAND):
                return None

            # Throws a KeyError if the Enum doesn't contain the given argument
            commandArg = CommandArgument[payload["text"].upper()]

            return Command(command, commandArg)

        except KeyError as e:
            self.logger.info("Invalid command argument: {}".format(e))
            return None
        except Exception as e:
            self.logger.info("Couldn't extract command: {}".format(e))
            return None
