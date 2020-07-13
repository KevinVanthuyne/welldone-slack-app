from model.command_argument import CommandArgument


class Command():
    """ Slack command object received through the API """

    def __init__(self, command: str, argument: CommandArgument):
        """ 
        Args:
            command (str): the command value. Should be /welldone
            argument (CommandArgument): the command's arguments
        """
        self.command = command
        self.argument = argument
