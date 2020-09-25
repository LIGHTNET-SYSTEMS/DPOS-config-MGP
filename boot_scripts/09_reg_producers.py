import toml
from utils import run, retry, firstProducer, numProducers, sleep, accounts, listProducers
config = toml.load('./config.toml')

def regProducers(b, e):
    for i in range(b, e):
        a = accounts[i]
        retry(config['cleos']['path'] + 'system regproducer ' + a['name'] + ' ' + a['pub'] + ' https://' + a['name'] + '.com' + '/' + a['pub'])

if __name__ == '__main__':
    regProducers(firstProducer, firstProducer + numProducers)
    sleep(1)
    listProducers()
    