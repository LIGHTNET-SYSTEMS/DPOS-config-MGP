import toml
from utils import startNode
config = toml.load('./config.toml')


if __name__ == '__main__':
    startNode(0, {'name': 'eosio', 'pvt': config['keosd']['private_key'], 'pub': config['keosd']['public_key']})
