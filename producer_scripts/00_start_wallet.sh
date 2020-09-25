#!/bin/bash
. ./set_env.sh

rm -rf $WALLET_DIR
mkdir -p $WALLET_DIR
$KEOSD_PATH --unlock-timeout $KEOSD_UNLOCK_TIMEOUT --http-server-address $KEOSD_HTTP_URL --wallet-dir $WALLET_DIR &
sleep 1
$CLEOS_PATH --url $NODE_URL wallet create -f $WALLET_PASSWD_PATH
