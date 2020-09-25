import toml
import random
from utils import vote, sleep, listProducers
config = toml.load('./config.toml')

if __name__ == '__main__':
    vote(0, 0 + config['general']['num_voters'])
    sleep(1)
    listProducers()
    