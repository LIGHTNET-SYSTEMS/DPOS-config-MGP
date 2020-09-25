import toml
import os
import sys
from utils import sleep, run, background, firstProducer, numProducers, accounts, retry
config = toml.load('./producer_config.toml')
producer_limit = 21

def addPeers():
    for i in range(producer_limit):
        run(config['cleos']['path'] + 'net connect 140.82.56.80:' + str(9000 + i))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("USAGE")
        sys.exit(1)
    config = toml.load(sys.argv[1])
    addPeers()