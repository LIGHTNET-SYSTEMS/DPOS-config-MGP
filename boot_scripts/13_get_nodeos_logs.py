import toml
import random
from utils import run

config = toml.load('./config.toml')

def getNodeosLogs():
    run('tail -n 60 ' + config['general']['nodes_dir'] + '00-eosio/stderr')

if __name__ == '__main__':
    getNodeosLogs()
    