
#Creating a snowflake connection
import snowflake.connector

class SnowflakeConnector:



    def __init__(self,config):
        self.config=config;
        self.conn=None;
        self.stage=config['snowflake_stage']


    def create_snowflake_connection(self):
        print(f"Connecting to Snowflake as user {self.config['snowflake_user']}git account {self.config['snowflake_account']}...")
        self.conn=snowflake.connector.connect(
            user=self.config['snowflake_user'],
            password=self.config['snowflake_password'],
            account=self.config['snowflake_account'],
            warehouse=self.config['snowflake_warehouse'],
            schema=self.config['snowflake_schema'],
            role=self.config['snowflake_role'],
            database=self.config['snowflake_database'],
            authenticator='snowflake'
        )
        if self.conn is None:
            print("Connection failed")
            exit()
        else:
            print("Connection Successful")
        return self.conn

    #Removing files from Snowflake stage
    def remove_files_from_stage(self):
            print(f"Removing all files from Snowflake stage {self.stage}...")
            cursor=self.conn.cursor()
            cursor.execute(f"REMOVE @{self.stage}")
            cursor.close()
            print(f"Removal of all files from Snowflake stage {self.stage} complete.")


    #Uploading files to stage
    def upload_files_to_stage(self,filelist):
        for file in filelist:
                print(f"Uploading {file} to Snowflake stage {self.stage}...")
                cursor=self.conn.cursor()
                cursor.execute(f"PUT file://{file} @{self.stage}")
                cursor.close()
                print(f"Upload of {file} to Snowflake stage {self.stage} complete.")


