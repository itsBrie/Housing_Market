import requests 
import time 
import os
import json
import snowflake.connector

stage=None

#Setting up config file input
config_path=os.path.join(os.path.dirname(__file__),'config','config_file.json')
with open (config_path,'r') as config_file:
    config=json.load(config_file)

# file output dir
output_dir=os.path.join(os.path.dirname(__file__),'data')
os.makedirs(output_dir,exist_ok=True)

#Setting up URL & API Key 
API_KEY=config['API_KEY']
BASE_URL="https://api.census.gov/data/{year}/acs/acs5?"
PARAMS=("get=NAME,B01001_001E,B01001_002E,B01001_026E,B02001_002E,B02001_003E," 
"B02001_004E,B02001_005E,B02001_006E,B02001_007E,B02001_008E,B19013_001E"
"&for=place:*&in=state:48" 
"&key={key}")

