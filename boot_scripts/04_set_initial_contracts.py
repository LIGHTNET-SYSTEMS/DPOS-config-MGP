import toml
from utils import run
config = toml.load('./config.toml')

def setInitialContracts():
    run(config['cleos']['path'] + 'set contract eosio.token ' + config['general']['contracts_dir'] + '/eosio.token/')
    run(config['cleos']['path'] + 'set contract eosio.msig ' + config['general']['contracts_dir'] + '/eosio.msig/')
    run(config['cleos']['path'] + 'set contract eosio.wrap ' + config['general']['contracts_dir'] + '/eosio.wrap/')

if __name__ == '__main__':
    setInitialContracts()
