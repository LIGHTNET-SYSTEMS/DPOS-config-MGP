import toml
from utils import sleep, run, background, firstProducer, numProducers, accounts
import os
config = toml.load('./config.toml')

def startWallet():
    run('rm -rf ' + os.path.abspath(config['keosd']['wallet_dir']))
    run('mkdir -p ' + os.path.abspath(config['keosd']['wallet_dir']))
    background(config['keosd']['path'] + ' --unlock-timeout %d --http-server-address %s --wallet-dir %s' % (config['keosd']['unlock_timeout'], config['keosd']['http_server_address'], os.path.abspath(config['keosd']['wallet_dir'])))
    sleep(.4)
    run(config['cleos']['path'] + 'wallet create --file %s ' % (config['keosd']['wallet_file']))

def importKeys():
    run(config['cleos']['path'] + 'wallet import --private-key ' + config['keosd']['private_key'])
    keys = {}
    for a in accounts:
        key = a['pvt']
        if not key in keys:
            if len(keys) >= config['general']['max_user_keys']:
                break
            keys[key] = True
            run(config['cleos']['path'] + 'wallet import --private-key ' + key)

if __name__ == '__main__':
    startWallet()
    importKeys()
    

