import subprocess
import sys
import json
import datetime

premineAccounts = ['team', 'priv', 'market', 'airdrops', 'app']
userNames = ['ltniolionsco', 'smartltnioco', 'ligntningini', 'betterthenyo', 'thebestlrnio', 'thebestusers', 'ltningfriend', 'crazyuserpro', 'monneymakers', 'proltniouser']
producerNames = ['lightsystem1', 'lightsystem2', 'lightsystem3', 'lightsystem4']

def run(args):
    if subprocess.call(args, shell=True):
        print('exiting because of error')
        sys.exit(1)


def generateKeyPairs(producerCount, userCount):
    run('mkdir keys')
    cmd = 'cleos --url http://0.0.0.0:8000 create key -f keys/%s.txt'
    run(cmd % ('eosio'))
    for name in premineAccounts:
        run(cmd % (name))
    for name in producerNames:
        run(cmd % (name))
    for name in userNames:
        run(cmd % (name))


def createAccountJson(producerCount, userCount):
    accounts = {
        "producers": [],
        "users": []
    }
    for name in producerNames:
        with open('keys/%s.txt' % (name), 'r') as f:
            pvt = f.readline().strip().split(' ')[2]
            pub = f.readline().strip().split(' ')[2]
            accounts["producers"].append({"name": name, "pub": pub})
            
    for name in userNames:
        with open('keys/%s.txt' % (name), 'r') as f:
            pvt = f.readline().strip().split(' ')[2]
            pub = f.readline().strip().split(' ')[2]
            accounts["users"].append({"name": name, "pub": pub, "pvt": pvt})
    with open('accounts.json', 'w') as f:
        json.dump(accounts, f, indent=4)


def generateGenesisConfig():
    with open('genesis.json', 'w') as f:
        genesis = {
            "initial_configuration": {
                "max_block_net_usage": 1048576,
                "target_block_net_usage_pct": 1000,
                "max_transaction_net_usage": 524288,
                "base_per_transaction_net_usage": 12,
                "net_usage_leeway": 500,
                "context_free_discount_net_usage_num": 20,
                "context_free_discount_net_usage_den": 100,
                "max_block_cpu_usage": 100000,
                "target_block_cpu_usage_pct": 500,
                "max_transaction_cpu_usage": 50000,
                "min_transaction_cpu_usage": 100,
                "max_transaction_lifetime": 3600,
                "deferred_trx_expiration_window": 600,
                "max_transaction_delay": 3888000,
                "max_inline_action_size": 4096,
                "max_inline_action_depth": 4,
                "max_authority_depth": 6
            },
            "initial_chain_id": "0000000000000000000000000000000000000000000000000000000000000000"
        }
        with open('keys/eosio.txt', 'r') as e:
            pvt = e.readline().strip().split(' ')[2]
            pub = e.readline().strip().split(' ')[2]
            genesis["initial_key"] = pub
            genesis["initial_timestamp"] = datetime.date.today().strftime("%Y-%m-%dT12:00:00.000")
            json.dump(genesis, f, indent=4)
            with open('config.toml', 'a') as c:
                c.write("private_key = '%s'\npublic_key = '%s'\n\n" % (pvt, pub))

    with open('config.toml', 'a') as f:
        with open('keys/priv.txt', 'r') as c:
            pvt = c.readline().strip().split(' ')[2]
            pub = c.readline().strip().split(' ')[2]
            f.write("[accounts]\npriv_incentive_public_key = '%s'\n" % (pub))
        with open('keys/team.txt', 'r') as c:
            pvt = c.readline().strip().split(' ')[2]
            pub = c.readline().strip().split(' ')[2]        
            f.write("team_holding_public_key = '%s'\n" % (pub))
        with open('keys/app.txt', 'r') as c:
            pvt = c.readline().strip().split(' ')[2]
            pub = c.readline().strip().split(' ')[2]
            f.write("app_public_key = '%s'\n" % (pub))
        with open('keys/market.txt', 'r') as c:
            pvt = c.readline().strip().split(' ')[2]
            pub = c.readline().strip().split(' ')[2]
            f.write("market_public_key = '%s'\n" % (pub))
        with open('keys/airdrops.txt', 'r') as c:
            pvt = c.readline().strip().split(' ')[2]
            pub = c.readline().strip().split(' ')[2]
            f.write("airdrops_public_key = '%s'\n" % (pub))


def generateProducerConfigs(producerCount, userCount):
    run('mkdir configs')
    run('mkdir env')
    for name in producerNames:
        with open('keys/%s.txt' % (name), 'r') as f:
            pvt = f.readline().strip().split(' ')[2]
            pub = f.readline().strip().split(' ')[2]
            run('cp config.ini configs/config_%s.ini'% (str(name)))
            run('cp set_env.sh env/set_env_%s.sh'% (str(name)))
            with open('configs/config_%s.ini' % (str(name)), 'a') as f:
                f.write('    producer-name = %s\n    signature-provider = %s=KEY:%s\n    agent-name = %s\n' %(name, pub, pvt, name))
            with open('env/set_env_%s.sh' % (str(name)), 'a') as f:
                f.write("export PROD_PRIVATE_KEY='%s'\nexport PROD_PUBLIC_KEY='%s'\nexport PROD_NAME='%s'\nexport CONFIG_NAME='config_%s.ini'" %(pvt, pub, name, str(name)))

            
if __name__ == '__main__':
    generateKeyPairs(4, 10)
    generateGenesisConfig()
    createAccountJson(4, 10)
    generateProducerConfigs(4, 10)
