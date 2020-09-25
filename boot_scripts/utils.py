import json
import toml
import subprocess
import time
import sys
import os
import json
import random

config = toml.load('./config.toml')

# global variables
with open('accounts.json') as f:
    a = json.load(f)
    if config['general']['user_limit']:
        del a['users'][config['general']['user_limit']:]
    # limit producers
    if config['general']['producer_limit']:
        del a['producers'][config['general']['producer_limit']:]
    firstProducer = len(a['users'])
    numProducers = len(a['producers'])
    accounts = a['users'] + a['producers']

maxClients = numProducers + 10

systemAccounts = [
    'eosio.bpay',
    'eosio.msig',
    'eosio.names',
    'eosio.ram',
    'eosio.ramfee',
    'eosio.stake',
    'eosio.token',
    'eosio.vpay',
    'eosio.rex',
    'eosio.wrap',
]

fundAccounts = [
    'market',
    'airdrops',
    'app'
]

# general functions
def sleep(t):
    print('sleep', t, '...')
    time.sleep(t)
    print('resume')

def run(args):
    print('bios: ', args)
    if subprocess.call(args, shell=True):
        print('bios: exiting because of error')
        sys.exit(1)

def background(args):
    print('bios:', args)
    return subprocess.Popen(args, shell=True)

def retry(args):
    while True:
        print('bios:', args)
        if subprocess.call(args, shell=True):
            print('*** Retry')
        else:
            break

def getOutput(args):
    print('bios:', args)
    proc = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE)
    return proc.communicate()[0].decode('utf-8')

def jsonArg(a):
    return " '" + json.dumps(a) + "' "

def getJsonOutput(args):
    return json.loads(getOutput(args))

# blockchain-specific functions
def startNode(nodeIndex, account):
    dir = config['general']['nodes_dir'] + ('%02d-' % nodeIndex) + account['name'] + '/'
    run('rm -rf ' + dir)
    run('mkdir -p ' + dir)
    otherOpts = ''.join(list(map(lambda i: '    --p2p-peer-address 0.0.0.0:' + str(9806 + i), range(nodeIndex))))
    if not nodeIndex: otherOpts += (
        '    --plugin eosio::history_plugin'
        '    --plugin eosio::history_api_plugin'
        '    --plugin eosio::net_api_plugin'
    )
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
        '    --p2p-listen-endpoint 0.0.0.0:' + str(9806 + nodeIndex) +
        '    --p2p-server-address 88.99.248.77:' + str(9806 + nodeIndex) +
        '    --max-clients ' + str(maxClients) +
        '    --p2p-max-nodes-per-host ' + str(maxClients) +
        '    --enable-stale-production'
        '    --allowed-connection any'
        '    --producer-name ' + account['name'] +
        '    --private-key \'["' + account['pub'] + '","' + account['pvt'] + '"]\'' 
        '    --plugin eosio::http_plugin'
        '    --plugin eosio::chain_api_plugin'
        '    --plugin eosio::chain_plugin'
        '    --plugin eosio::producer_api_plugin'
        '    --plugin eosio::producer_plugin'
        '    --access-control-allow-origin "*"'
        '    --access-control-allow-headers "Origin, X-Requested-With, Content-Type, Accept"' +
        otherOpts)
    with open(dir + 'stderr', mode='w') as f:
        f.write(cmd + '\n\n')
    background(cmd + '    2>>' + dir + 'stderr')
    sleep(1)
    if nodeIndex == 0:
        cmd = 'curl -X POST http://0.0.0.0:'+ str(8000 + nodeIndex) +'/v1/producer/schedule_protocol_feature_activations -d \'{"protocol_features_to_activate": ["0ec7e080177b2c02b278d5088611686b49d739925a92d9bfcacd7fc6b74053bd"]}\' '
        with open(dir + 'stderr', mode='w') as f:
            f.write(cmd + '\n\n')
        background(cmd + '    2>>' + dir + 'stderr')
        sleep(2)

def intToCurrency(i):
    return '%d.%04d %s' % (i // 10000, i % 10000, config['general']['symbol'])

def listProducers():
    run(config['cleos']['path'] + 'system listproducers')

def vote(b, e):
    for i in range(b, e):
        voter = accounts[i]['name']
        k = config['general']['num_producers_vote']
        if k > numProducers:
            k = numProducers - 1
        prods = random.sample(range(firstProducer, firstProducer + numProducers), k)
        prods = ' '.join(map(lambda x: accounts[x]['name'], prods))
        retry(config['cleos']['path'] + 'system voteproducer prods ' + voter + ' ' + prods)

def updateAuth(account, permission, parent, controller):
    run(config['cleos']['path'] + 'push action eosio updateauth' + jsonArg({
        'account': account,
        'permission': permission,
        'parent': parent,
        'auth': {
            'threshold': 1, 'keys': [], 'waits': [],
            'accounts': [{
                'weight': 1,
                'permission': {'actor': controller, 'permission': 'active'}
            }]
        }
    }) + '-p ' + account + '@' + permission)

def updateKey(account, permission, publicKey):
    run(config['cleos']['path'] + 'set account permission %s %s %s -p %s@owner' % (account, permission, publicKey, account))
    