from model.message import Message


class MessageService():
    """ Service for handling Message objects """

    @staticmethod
    def has_valid_channel_type(message: Message):
        """ Checks if a message was sent in a public or private channel """
        return message.channel_type == "channel" or message.channel_type == "group"
