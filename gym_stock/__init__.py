import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)

register(
    id='Stock-v1',
    entry_point='gym_stock.envs:StockEnv',
)
