
import snowflake.connector
#Creating a snowflake connection

def create_snowflake_connection(config):
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

#Uploading/Removing files to Snowflake stage

def upload_files_to_stage(in_connection,filelist,stage_name):
    print(f"Removing all files from Snowflake stage {stage_name}...")
    cursor=in_connection.cursor()
    cursor.execute(f"REMOVE @{stage_name}")
    cursor.close()
    print(f"Removal of all files from Snowflake stage {stage_name} complete.")


    for file in filelist:
        print(f"Uploading {file} to Snowflake stage {stage_name}...")
        cursor=in_connection.cursor()
        cursor.execute(f"PUT file://{file} @{stage_name}")
        cursor.close()
        print(f"Upload of {file} to Snowflake stage {stage_name} complete.")