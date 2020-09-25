# Prerequirements

The launching network needs:
- blockchain;
- built system contracts;
- configurations.

To speed up installation, some deb packages will be used instead of building from sources.

For each node, run:
```
git clone https://github.com/LIGHTNET-SYSTEMS/DPOS-config
cd DPOS-config
sh install.sh
```
# Key Generation

Go to future genesis node and run:
```
cd gen_scripts/
```

3 configs are present.

`config.ini` is a node config draft, it contains general configurations for all block producers. It is important to 
set all block producers api in `p2p-peer-address`. 
`config.toml` is config for genesis node; it contains a number of configurations but the most important are `general`:
```
max_user_keys = <<<number of user keys which will be imported>>>
user_limit = <<<number of users that will be created with some initial balance>>>
producer_limit = <<<number of producers will be created with appropriate resources>>>>
...
num_voters = <<<number of users that votes during final step>>>
num_producers_vote = <<<number of producers that will receive votes during final step>>>
```
`set_env.sh` contains configs for block producer scripts.
User and producer names can be configured directly in `gen_configs.py` by `userNames`'s and `producerNames`'s modifications.   


If all configurations done, run: 

```
cd gen_scripts/
python3 gen_configs.py
```

This script:
- generates new key pairs: private and public keys for genesis node, block producers and users;
- creates *account.json* which is a file where public keys and account names for new accounts are stored,
it will be used by genesis node only;
- creates *configN.ini* for each block producer in directory `configs/`, this file is used to configure nodeos;
- creates *set_envN.sh* for each block producer in directory `env/`, this file is needed for block producer scripts;
- creates *config.toml* for genesis node, this file is used to configure genesis node during first launch;
- creates *genesis.json*.

On genesis node run:

```
cp config.toml ../boot_scripts/ && cp genesis.json ../ && cp accounts.json ../boot_scripts/ 
```

For each block producer do:
- copy genesis.json to root of the DPOS-config directory;
- copy *set_envN.sh* renamed to *set_env.sh* and *configN.ini* renamed to *config.ini* to producer_scripts. 

# Boot

There are different ways to configure node. For boot, one genesis node and few block producers are needed.

## Genesis Node

To start genesis node and prepare network run:

```
cd boot_scripts
./prepare_boot.sh
```
For this point of time, some things happened such as:
- local wallet was created and keosd (util for keys management) was run;
- genesis keys was imported - for now the user owned this keys has unlimited permissions;
- genesis node was started;
- special accounts (for future system management and premine) were created;
- system contracts were deployed;
- main network currency were created, premine amount were issue; 
- premine was sent to prepared accounts;
- accounts for first block producers and users were created.

Let's consider some commands to check that everything is as expected.

```
cleos --url http://0.0.0.0:8000 get currency balance eosio.token airdrops LTN
```
This commands will return airdrops funds amount that left after initial distribution among block producers and first users.

Change *airdrops* to another account name to see other funds:
- *app* - premine amount for commercial applications;
- *market* - premine amount for market incentives;
- *priv* - premine amount for private placement
- *team* - premine amount for team holding.

```
cleos --url http://0.0.0.0:8000 get info
```
This command returns general chain info.

```
cleos --url http://0.0.0.0:8000 get account USER_NAME
```
and

```
cleos --url http://0.0.0.0:8000 get account PRODUCER_NAME
```
These commands allows to verify that users and block producers accounts were created.

Try script:
```
python3 13_get_nodeos_logs.py
```
It returns genesis node logs, some information about new blocks are present.

If all is right, block producers can be registered and their nodes can be started. 

## Block Producer

Run:
```
cd producers_scripts
./boot_producer.sh
```
This script will:
- start keosd;
- import block producer keys;
- register block producer;
- run block producer node.

For now it does not produce blocks but is properly connected to genesis node.

Check it using command:

```
cleos --url http://0.0.0.0:8000 get info
```
*chain_id* should be the same as on the genesis node.

Repeat these steps for all block producers.

## Finalize Boot

Go to genesis node server and run:
```
./finalize_boot.sh
```
This script will:
- send permissions for system contracts management to block producers;
- vote for new block producers with first users keys;
- print genesis node logs.

If all is right, in logs new blocks are produced by new producers but not eosio.

