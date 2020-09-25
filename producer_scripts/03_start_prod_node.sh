#!/bin/bash
. ./set_env.sh

mkdir -p $CONFIG_DIR
cp config.ini $CONFIG_DIR/config.ini 
$NODEOS_PATH --config-dir $CONFIG_DIR --data-dir $DATA_DIR --genesis-json $GENESIS_JSON
