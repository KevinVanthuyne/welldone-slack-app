from model.message import Message


class MessageService():
    """ Service for handling Message objects """

    KEYWORD = ":bacon:"

    @staticmethod
    def has_valid_channel_type(message: Message):
        """ Checks if a message was sent in a public or private channel """
        return message.channel_type == "channel" or message.channel_type == "group"

    @staticmethod
    def contains_keyword(message: Message):
        """ Checks if the message contains the keyword/emoji that triggers 
            rewarding a user 
        """
        return MessageService.KEYWORD in message.content

    @staticmethod
    def get_tagged_users(message: Message):
        """ Get the user id's from all tagged users in the message with the 
            duplicate user id's removed 
        """
        user_ids = []
        for element in message.blocks[0]["elements"][0]["elements"]:
            if element["type"] == "user":
                user_ids.append(element["user_id"])
        return list(dict.fromkeys(user_ids))
