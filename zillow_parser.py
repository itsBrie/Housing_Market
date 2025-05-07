import pandas as pd 
import json
import os

#Getting CSV Path and Assigning it to var 
config_path=os.path.join(os.path.dirname(__file__),'config','config_file.json')
with open (config_path,'r')as config_file:
    config=json.load(config_file)

zillow_csv=config['zillow_csv_path']

#Reading the CSV file
df=pd.read_csv(zillow_csv)

#Defining the headers and date col
col_attr=['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName',
    'State', 'City', 'Metro', 'CountyName']

#Melting the DataFrame into a Long Format
df_long=df.melt(
    id_vars=col_attr,
    var_name='Date',
    value_name='HomeValue'
)
#Converting the Data column from string to datetime
df_long['Date'] = pd.to_datetime(df_long['Date'], format='%m/%d/%Y', errors='coerce')

#Drop any rows where 'Date' failed to convert
df_long = df_long.dropna(subset=['Date'])

print(df_long.head())

