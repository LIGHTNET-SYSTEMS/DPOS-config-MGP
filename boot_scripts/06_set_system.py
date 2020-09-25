import toml
from utils import run, retry, jsonArg, sleep
config = toml.load('./config.toml')

def setSystem():
    retry(config['cleos']['path'] + 'set contract eosio ' + config['general']['contracts_dir'] + '/eosio.system/')
    sleep(1)
    run(config['cleos']['path'] + 'push action eosio setpriv' + jsonArg(['eosio.msig', 1]) + '-p eosio@active')
    run(config['cleos']['path'] + 'push action eosio init' + jsonArg(['0', '4,' + config['general']['symbol']]) + '-p eosio@active')


if __name__ == '__main__':
    setSystem()
    