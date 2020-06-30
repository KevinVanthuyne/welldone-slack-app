from model.reward import Reward


class RewardService():
    """ Service for giving rewards to users and getting the scores """

    def __init__(self, logger):
        self.logger = logger
        self.rewards = []

    def give_reward(self, reward: Reward):
        """ Checks if the reward is valid and stores it internally """
        self.rewards.append(reward)
        self.logger.info("Saved reward: {}".format(reward))
