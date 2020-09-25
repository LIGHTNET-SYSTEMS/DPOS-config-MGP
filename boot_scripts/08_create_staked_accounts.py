import toml
import numpy
from utils import retry, accounts, firstProducer, numProducers, intToCurrency
config = toml.load('./config.toml')

def allocateFunds(b, e):
    total = 0
    for i in range(b, e):
        if i >= firstProducer and i < firstProducer + numProducers:
            funds = round(config['funds']['producer_funds'] * 10000)
        else:
            funds = round(config['funds']['user_funds'] * 10000)
        total += funds
        accounts[i]['funds'] = funds
    return total

def createStakedAccounts(b, e):
    ramFunds = round(config['funds']['ram_funds'] * 10000)
    configuredMinStake = round(config['funds']['min_stake'] * 10000)
    maxUnstaked = round(config['funds']['max_unstaked'] * 10000)
    for i in range(b, e):
        a = accounts[i]
        funds = a['funds']
        print('#' * 80)
        print('# %d/%d %s %s' % (i, e, a['name'], intToCurrency(funds)))
        print('#' * 80)
        if funds < ramFunds:
            print('skipping %s: not enough funds to cover ram' % a['name'])
            continue
        minStake = min(funds - ramFunds, configuredMinStake)
        unstaked = min(funds - ramFunds - minStake, maxUnstaked)
        stake = funds - ramFunds - unstaked
        stakeNet = round(stake / 2)
        stakeCpu = stake - stakeNet
        print('%s: total funds=%s, ram=%s, net=%s, cpu=%s, unstaked=%s' % (a['name'], intToCurrency(a['funds']), intToCurrency(ramFunds), intToCurrency(stakeNet), intToCurrency(stakeCpu), intToCurrency(unstaked)))
        assert(funds == ramFunds + stakeNet + stakeCpu + unstaked)
        retry(config['cleos']['path'] + 'system newaccount --transfer airdrops %s %s --stake-net "%s" --stake-cpu "%s" --buy-ram "%s" ' % 
            (a['name'], a['pub'], intToCurrency(stakeNet), intToCurrency(stakeCpu), intToCurrency(ramFunds)))
        if unstaked:
            retry(config['cleos']['path'] + 'transfer airdrops %s "%s"' % (a['name'], intToCurrency(unstaked)))

if __name__ == '__main__':
    allocateFunds(0, len(accounts))
    createStakedAccounts(0, len(accounts))
