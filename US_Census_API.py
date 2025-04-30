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

#Creating a snowflake connection
def create_snowflake_connection():
    print(f"Connecting to Snowflake as user {config['snowflake_user']} on account {config['snowflake_account']}...")
    global stage 
    conn=snowflake.connector.connect(
        user=config['snowflake_user'],
        password=config['snowflake_password'],
        account=config['snowflake_account'],
        warehouse=config['snowflake_warehouse'],
        schema=config['snowflake_schema'],
        role=config['snowflake_role'],
        database=config['snowflake_database'],
        authenticator='snowflake'
    )
    if conn is None:
        print("Connection failed")
        exit()
    else:
        print("Connection Successful")
    stage=config['snowflake_stage']
    return conn

#Get Census data from API
def get_census_data (start_year, end_year):
    output_files=[]
    for year in range(start_year,end_year+1):
        url=BASE_URL.format(year=year)+PARAMS.format(key=API_KEY)
        response=requests.get(url)
        if response.status_code!= 200:
            print(f"Error fetching data for {year} : {response.status_code}")
            continue

        data=response.json()
        headers=data[0]
        converted_data=[dict(zip(headers,row))|{"year":year}for row in data[1:]]

        with open(f"{output_dir}/TX_data_{year}.json","w",encoding="utf-8")as f:
           f.write(str(converted_data))
           output_file=f"{output_dir}/TX_data_{year}.json"
           print(f"Data for {year} written to {output_file}")
           output_files.append(output_file)
        time.sleep(1)
    return output_files