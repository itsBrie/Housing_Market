import requests 
import time 
import os
import json
from snowflake_connector import SnowflakeConnector

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

if __name__=='__main__':
    start_year=2019
    end_year=2023
    files_to_upload=get_census_data(start_year,end_year)
    print("Data retrieval complete")
    print("Establishing Snowflake connection...")
    snowflake_conn=SnowflakeConnector(config)
    snowflake_conn.create_snowflake_connection()
    print("Snowflake connection established")
    print("Removing files to Snowflake stage...")
    snowflake_conn.remove_files_from_stage()
    print("Uploading files to Snowflake stage...")
    snowflake_conn.upload_files_into_stage(files_to_upload)
    print("File upload complete.")
