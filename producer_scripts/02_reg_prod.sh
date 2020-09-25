#!/bin/bash
. ./set_env.sh

$CLEOS_PATH --url $GENESIS_NODE_URL system regproducer $PROD_NAME $PROD_PUBLIC_KEY http://lightnet.systems/
