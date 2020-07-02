import logging

from model.reward import Reward
from dao.reward_dao import RewardDao


class RewardService():
    """ Service for giving rewards to users and getting the scores """

    MAX_ALLOWED_REWARDS = 50

    def __init__(self):
        self.logger = logging.getLogger()
        self.reward_dao = RewardDao()

    def give_reward(self, reward: Reward):
        """ Checks if the reward is valid and stores it internally """
        return self.reward_dao.save(reward)

    def can_give_reward(self, user_id: str):
        """ Checks if the user can give 1 more reward without reaching the 
            maximum allowed rewards 
        """
        reward_count = self.reward_dao.todays_given_rewards(user_id)
        if reward_count >= self.MAX_ALLOWED_REWARDS:
            self.logger.info(
                "User {} has reached the {} maximum rewards of today".format(user_id, self.MAX_ALLOWED_REWARDS))
            return False
        self.logger.info("User {} has given {} rewards out of the {} maximum today".format(
            user_id, reward_count, self.MAX_ALLOWED_REWARDS))
        return True
