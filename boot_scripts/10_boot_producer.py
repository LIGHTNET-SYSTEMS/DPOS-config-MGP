import toml
import os
import sys
from utils import sleep, run, background, firstProducer, numProducers, accounts, retry
config = toml.load('./producer_config.toml')

def startWallet():
    run('rm -rf ' + os.path.abspath(config['keosd']['wallet_dir']))
    run('mkdir -p ' + os.path.abspath(config['keosd']['wallet_dir']))
    background(config['keosd']['path'] + ' --unlock-timeout %d --http-server-address %s --wallet-dir %s' % (config['keosd']['unlock_timeout'], config['keosd']['http_server_address'], os.path.abspath(config['keosd']['wallet_dir'])))
    sleep(.4)
    run(config['cleos']['path'] + 'wallet create  -f wallet.passwd')

def importKeys():
    run(config['cleos']['path'] + 'wallet import --private-key ' + config['prod']['pvt'])

def startSingleProducer(nodeIndex, account):
    dir = config['general']['nodes_dir'] + account['name'] + '/'
    run('rm -rf ' + dir)
    run('mkdir -p ' + dir)
    cmd = (
        config['nodeos']['path'] +
        '    --max-irreversible-block-age -1'
        '    --contracts-console'
        '    --genesis-json ' + os.path.abspath(config['general']['genesis']) +
        '    --blocks-dir ' + os.path.abspath(dir) + '/blocks'
        '    --config-dir ' + os.path.abspath(dir) +
        '    --data-dir ' + os.path.abspath(dir) +
        '    --chain-state-db-size-mb 1024'
        '    --http-server-address 0.0.0.0:' + str(8000 + nodeIndex) +
        '    --p2p-listen-endpoint 0.0.0.0:' + str(9000 + nodeIndex) +
        '    --p2p-server-address 140.82.56.80:' + str(9000 + nodeIndex) +
        '    --max-clients 100'
        '    --connection-cleanup-period 200'
        '    --p2p-max-nodes-per-host 100'
        '    --enable-stale-production'
        '    --allowed-connection any'
        '    --producer-name ' + account['name'] +
        '    --private-key \'["' + account['pub'] + '","' + account['pvt'] + '"]\''
        '    --plugin eosio::http_plugin'
        '    --plugin eosio::chain_api_plugin'
        '    --plugin eosio::producer_api_plugin'
        '    --plugin eosio::producer_plugin' 
        '    --plugin eosio::history_plugin'
        '    --plugin eosio::history_api_plugin'
        '    --plugin eosio::net_api_plugin'
        '    --plugin eosio::net_plugin'
        '    --access-control-allow-origin "*"'
        '    --access-control-allow-headers "Origin, X-Requested-With, Content-Type, Accept"'
        '    --p2p-peer-address 88.99.248.77:9000')
    with open(dir + 'stderr', mode='w') as f:
        f.write(cmd + '\n\n')
    background(cmd + '    2>>' + dir + 'stderr')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("USAGE: python3 boot_producer.py <<shouldStartWallet>> <<configPath>>")
        sys.exit(1)
    config = toml.load(sys.argv[2])
    if sys.argv[1] == "1":
        startWallet()

    importKeys()
    retry(config['cleos']['path'] + ' --url http://88.99.248.77:8000 system regproducer ' + config['prod']['name'] + ' ' + config['prod']['pub'] + ' https://' + config['prod']['name'] + '.com' + '/' + config['prod']['pub'])
    account = {
        'name': config['prod']['name'],
        'pub': config['prod']['pub'],
        'pvt': config['prod']['pvt']
    }
    startSingleProducer(config['prod']['index'], account)
    