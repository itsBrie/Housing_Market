import requests 
import time 
import os
import json
import snowflake.connector

stage=None

config_path=os.path.join(os.path.dirname(__file__),'config_file.json')
with open (config_path,'r') as config_file:
    config=json.load(config_file)

API_KEY=config['API_KEY']