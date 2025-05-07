import pandas as pd 
import json
import os

#Getting CSV Path and Assigning it to var 
config_path=os.path.join(os.path.dirname(__file__),'config','config_file.json')
with open (config_path,'r')as config_file:
    config=json.load(config_file)

zillow_csv=config['zillow_csv_path']

