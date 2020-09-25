#!/bin/bash
python3 00_kill_all.py                 
python3 01_create_wallet.py
python3 02_start_genesis_node.py
python3 03_create_system_accounts.py   
python3 04_set_initial_contracts.py    
python3 05_create_sys_token.py        
python3 06_set_system.py              
python3 07_premine.py                 
python3 08_create_staked_accounts.py   
