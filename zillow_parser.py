import pandas as pd 
import json
import os
from snowflake_connector import SnowflakeConnector

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
df_long['Date'] = df_long['Date'].dt.strftime('%Y-%m-%d')

#Drop any rows where 'Date' failed to convert
df_long = df_long.dropna(subset=['Date'])

#print(df_long.head())

#Outputing Dataframe as CSV in same input folder
output_dir=os.path.dirname(zillow_csv)
os.makedirs(output_dir, exist_ok=True)
zillow_output_json=os.path.join(output_dir,'zillow_data.json')
df_long.to_json(zillow_output_json, orient='records',lines=True)


#Connecting and uploading JSON files to Snowflake
print("Establishing Snowflake connection...")
snowflake_conn=SnowflakeConnector(config)
snowflake_conn.create_snowflake_connection()
print("Snowflake connection established")

print("Uploading files to Snowflake stage...")
snowflake_conn.upload_files_to_stage([zillow_output_json])
print("File upload complete.")
