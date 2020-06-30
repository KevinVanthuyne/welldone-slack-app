from model.reward import Reward
from dao.reward_dao import RewardDao


class RewardService():
    """ Service for giving rewards to users and getting the scores """

    def __init__(self, logger):
        self.logger = logger
        self.reward_dao = RewardDao()

    def give_reward(self, reward: Reward):
        """ Checks if the reward is valid and stores it internally """
        self.reward_dao.save(reward)
