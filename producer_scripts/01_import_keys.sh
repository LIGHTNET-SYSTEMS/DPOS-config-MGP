#!/bin/bash
. ./set_env.sh

$CLEOS_PATH --url $NODE_URL wallet import --private-key $PROD_PRIVATE_KEY
