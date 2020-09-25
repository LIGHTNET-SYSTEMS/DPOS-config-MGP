#!/bin/bash
. ./set_env.sh

$CLEOS_PATH --url $GENESIS_NODE_URL system claimrewards $PROD_NAME -p$PROD_NAME
