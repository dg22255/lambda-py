#
## Imports
#
import boto3
import hashlib,os
from datetime import datetime

#
## Statics and variable declaration
#
rds_client = boto3.client('rds-data')
database_name = 'bcd_cab_sbx'
db_cluster_arn = 'arn:aws:rds:us-east-1:041407107837:cluster:bcd-cab-cluster-sbx'
db_credentials_secret_store_arn = 'arn:aws:secretsmanager:us-east-1:041407107837:secret:sbx-bcd_cab-postgres-IKmbPt'
msg={}
msg['status']=0

#
## Definitions
#

def lambda_handler(event, context):
    l = logger()
    l.msg("event: {}".format(event))
    
    # Parameter validation
    if event['action'] == 'increment':
        action = 'increment'
    elif event['action'] == 'decrement':
        action = 'decrement'
    else:
        l.msg("Invalid action passed: {}".format(event['action']),3)
        msg['status']=400
        msg['action']="ERROR: Invalid action"

    if str(type(event['targetDbVersion'])) == "<class 'int'>" or str(type(event['targetDbVersion'])) == "<class 'float'>":
        targetDbVersion = event['targetDbVersion']
    else:
        l.msg("Invalid targetDbVersion passed: {}".format(event['targetDbVersion']),3)
        l.msg("targetDbVersion type: {}".format(type(event['targetDbVersion'])),3)
        msg['status']=400
        msg['action']="ERROR: Invalid targetDbVersion"
    
    currentDbVersion = getDbVersion()
    msg['startingDbVersion']=currentDbVersion
    l.msg("Current database version is {}".format(currentDbVersion))

    if action == 'increment':
        #
        # Increment database version up to targetDbVersion
        #
        msg['action']="Incrementing"
        if currentDbVersion < targetDbVersion and currentDbVersion == 0.0:
            
            # v0 => v1  Initialize parm and user tables
            ###############################################
            l.msg("Implementing dababase version 1.0")
            ###############################################
            
            l.msg("Creating table (if not exists): vals_parmtype")
            execute_statement("CREATE TABLE IF NOT EXISTS vals_parmtype(typename VARCHAR(8) NOT NULL PRIMARY KEY);")

            l.msg("Creating table (if not exists): parm")
            execute_statement("""CREATE TABLE IF NOT EXISTS parm(
                                    parmname      VARCHAR(32) NOT NULL PRIMARY KEY,
                                    parmtype      VARCHAR(8) NOT NULL,
                                    parmval_dt    TIMESTAMP,
                                    parmval_st    VARCHAR(256),
                                    parmval_nu    REAL,
                                    last_updated  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                    FOREIGN KEY(parmtype) REFERENCES vals_parmtype(typename));
                                """)
            
            l.msg("Creating table (if not exists): sec_user")
            execute_statement("""CREATE TABLE IF NOT EXISTS sec_user(
                                    user_id SERIAL PRIMARY KEY,
                                    email VARCHAR(256) NOT NULL UNIQUE,
                                    first_nme VARCHAR(256),
                                    last_nme VARCHAR(256),
                                    pw VARCHAR(256),
                                    is_active BOOLEAN DEFAULT FALSE NOT NULL,
                                    is_verified BOOLEAN DEFAULT FALSE NOT NULL,
                                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                    );
                                """)

            l.msg("Creating table (if not exists): sec_app")
            execute_statement("""CREATE TABLE IF NOT EXISTS sec_app(
                                    app_id SERIAL PRIMARY KEY,
                                    app_name VARCHAR(256) NOT NULL,
                                    organization VARCHAR(256) NOT NULL,
                                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                    UNIQUE (app_name, organization)
                                    );
                                """)

            l.msg("Creating table (if not exists): sec_app_role")
            execute_statement("""CREATE TABLE IF NOT EXISTS sec_app_role(
                                    app_id INT,
                                    role_id SERIAL PRIMARY KEY,
                                    role_name VARCHAR(256) NOT NULL,
                                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                    FOREIGN KEY(app_id) REFERENCES sec_app(app_id)
                                    );
                                """)

            l.msg("Creating table (if not exists): sec_app_user")
            execute_statement("""CREATE TABLE IF NOT EXISTS sec_app_user(
                                    app_id INT,
                                    user_id INT,
                                    role_id INT,
                                    approved_by INT,
                                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                    PRIMARY KEY (app_id, user_id, role_id),
                                    FOREIGN KEY (app_id) REFERENCES sec_app(app_id),
                                    FOREIGN KEY (user_id) REFERENCES sec_user(user_id),
                                    FOREIGN KEY (role_id) REFERENCES sec_app_role(role_id),
                                    FOREIGN KEY (approved_by) REFERENCES sec_app(app_id)
                                    );
                                """)
            
            l.msg("Dababase version 1.0 implemented.")
            l.msg("Inserting base values for: vals_parmtype")
            execute_statement("INSERT INTO vals_parmtype(typename) VALUES('datetime'),('string'),('number') ON CONFLICT (typename) DO NOTHING;")
            setDbVersion(1.0)
            currentDbVersion = getDbVersion()
            
        if currentDbVersion < targetDbVersion and currentDbVersion == 1.0:
            
            # v1 => v2  Initialize cab and zd tables
            ###############################################
            l.msg("Implementing dababase version 2.0")
            ###############################################
            
            l.msg("Creating table (if not exists): vals_responsible_agency")
            execute_statement("CREATE TABLE IF NOT EXISTS vals_responsible_agency (val VARCHAR(64) PRIMARY KEY);")

            l.msg("Creating table (if not exists): vals_data_source")
            execute_statement("CREATE TABLE IF NOT EXISTS vals_data_source (val VARCHAR(64) PRIMARY KEY);")

            l.msg("Creating table (if not exists): vals_reason_for_change")
            execute_statement("CREATE TABLE IF NOT EXISTS vals_reason_for_change (val VARCHAR(64) PRIMARY KEY);")

            l.msg("Creating table (if not exists): vals_cab_status")
            execute_statement("CREATE TABLE IF NOT EXISTS vals_cab_status (val VARCHAR(64) PRIMARY KEY);")

            l.msg("Creating table (if not exists): vals_change_type")
            execute_statement("CREATE TABLE IF NOT EXISTS vals_change_type (val VARCHAR(64) PRIMARY KEY);")

            l.msg("Creating table (if not exists): vals_deployment_status")
            execute_statement("CREATE TABLE IF NOT EXISTS vals_deployment_status (val VARCHAR(64) PRIMARY KEY);")

            l.msg("Creating table (if not exists): vals_category")
            execute_statement("CREATE TABLE IF NOT EXISTS vals_category (val VARCHAR(64) PRIMARY KEY);")

            l.msg("Creating table (if not exists): vals_reoccurence")
            execute_statement("CREATE TABLE IF NOT EXISTS vals_reoccurence (val VARCHAR(64) PRIMARY KEY);")

            
            l.msg("Creating table (if not exists): cab_request")
            l.msg("Creating table (if not exists): cab_response")
            l.msg("Creating table (if not exists): cab_result")
            
            l.msg("Creating table (if not exists): zd_users")

            l.msg("Creating table (if not exists): zd_tickets")
            l.msg("Creating table (if not exists): zd_comments")

            l.msg("Dababase version 2.0 implemented.")
            setDbVersion(2.0)
            currentDbVersion = getDbVersion()
        msg['status']=200                                
    elif action == 'decrement':
        #
        # Deccrement database version down to targetDbVersion
        #
        msg['action']="Decrementing"
        
        if (currentDbVersion > targetDbVersion and currentDbVersion == 2.0) or targetDbVersion == 0:
            
            # v2 => v1  Delete cab and zd tables
            ###############################################
            l.msg("Decrementing dababase to version 1.0")
            ###############################################
            
            l.msg("Dropping table: cab_result",2)
            execute_statement("DROP TABLE IF EXISTS cab_result CASCADE;")
            l.msg("Dropping table: cab_response",2)
            execute_statement("DROP TABLE IF EXISTS cab_response CASCADE;")
            l.msg("Dropping table: cab_request",2)
            execute_statement("DROP TABLE IF EXISTS cab_request CASCADE;")
            
            l.msg("Dropping table: zd_comments",2)
            execute_statement("DROP TABLE IF EXISTS zd_comments CASCADE;")
            l.msg("Dropping table: zd_tickets",2)
            execute_statement("DROP TABLE IF EXISTS zd_tickets CASCADE;")
            l.msg("Dropping table: zd_users",2)
            execute_statement("DROP TABLE IF EXISTS zd_users CASCADE;")
            
            l.msg("Dropping table: vals_responsible_agency",2)
            execute_statement("DROP TABLE IF EXISTS vals_responsible_agency CASCADE;")
            l.msg("Dropping table: vals_data_source",2)
            execute_statement("DROP TABLE IF EXISTS vals_data_source CASCADE;")
            l.msg("Dropping table: vals_reason_for_change",2)
            execute_statement("DROP TABLE IF EXISTS vals_reason_for_change CASCADE;")
            l.msg("Dropping table: vals_cab_status",2)
            execute_statement("DROP TABLE IF EXISTS vals_cab_status CASCADE;")
            l.msg("Dropping table: vals_change_type",2)
            execute_statement("DROP TABLE IF EXISTS vals_change_type CASCADE;")
            l.msg("Dropping table: vals_deployment_status",2)
            execute_statement("DROP TABLE IF EXISTS vals_deployment_status CASCADE;")
            l.msg("Dropping table: vals_category",2)
            execute_statement("DROP TABLE IF EXISTS vals_category CASCADE;")
            l.msg("Dropping table: vals_reoccurence",2)
            execute_statement("DROP TABLE IF EXISTS vals_reoccurence CASCADE;")

            l.msg("Dababase version 1.0 implemented.")
            setDbVersion(1.0)
            currentDbVersion = getDbVersion()
        
        if targetDbVersion == 0:
            
            # v1 => v0  Delete parm and user tables
            ###############################################
            l.msg("Decrementing dababase to version 0.0")
            ###############################################

            l.msg("Dropping table: sec_app_user",2)
            execute_statement("DROP TABLE IF EXISTS sec_app_user CASCADE;")
            l.msg("Dropping table: sec_approle",2)
            execute_statement("DROP TABLE IF EXISTS sec_approle CASCADE;")
            l.msg("Dropping table: sec_app",2)
            execute_statement("DROP TABLE IF EXISTS sec_app CASCADE;")
            l.msg("Dropping table: sec_user",2)
            execute_statement("DROP TABLE IF EXISTS sec_user CASCADE;")
            
            l.msg("Dropping table: parm",2)
            execute_statement("DROP TABLE IF EXISTS parm CASCADE;")
            l.msg("Dropping table: vals_parmtype",2)
            execute_statement("DROP TABLE IF EXISTS vals_parmtype CASCADE;")
            currentDbVersion = getDbVersion()

            l.msg("Dababase version 0.0 implemented.")
        msg['status']=200
    else:
        msg['status']=400
        
    msg['targetDbVersion']=targetDbVersion
    msg['currentDbVersion']=currentDbVersion
    return msg
   
def getDbVersion():
    vals_parmtypeExists = False
    parmExists = False
    currentDbVersion = 0.0
    response = execute_statement("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';")
    results = response['records']
    for result in results:
        if result[0]['stringValue'] == 'parm': parmExists = True
        if result[0]['stringValue'] == 'vals_parmtype': vals_parmtypeExists = True
    if vals_parmtypeExists and parmExists:
        response = execute_statement("SELECT parmval_nu FROM parm WHERE parmname = 'DB_VERSION';")
        results = response['records']
        for result in results:
            currentDbVersion = result[0]['doubleValue']
    return currentDbVersion
   
def setDbVersion(dbVersion=0.0):
    sql="""INSERT INTO parm(parmname,parmtype,parmval_nu) VALUES ('DB_VERSION','number',{}) 
           ON CONFLICT (parmname) DO UPDATE SET parmtype='number',parmval_nu={},last_updated=CURRENT_TIMESTAMP;""".format(dbVersion,dbVersion)
    execute_statement(sql)
   
def execute_statement(sql):
    response = rds_client.execute_statement(
        secretArn = db_credentials_secret_store_arn,
        database = database_name,
        resourceArn = db_cluster_arn,
        sql = sql
        )
    return response
   
class logger:
    def __init__(self, logLevel=1):
        self.logLevel=logLevel
        self.switcher={0:'DEBUG: ',1:'INFO: ',2:'WARNING: ',3:'ERROR: '}
    def msg(self,msgtxt,msgtype=1):
        if msgtype >= self.logLevel:
            logdate=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            msgLvl=self.switcher.get(msgtype)
            frmtdMsgTxt="{}-{}{}".format(logdate,msgLvl,msgtxt)
            print(frmtdMsgTxt)
