#
## Imports
#
import boto3
import hashlib
import os

#
## Static and variable declaration
#
rds_client = boto3.client('rds-data')
database_name = 'bcd_cab_sbx'
db_cluster_arn = 'arn:aws:rds:us-east-1:041407107837:cluster:bcd-cab-cluster-sbx'
db_credentials_secret_store_arn = 'arn:aws:secretsmanager:us-east-1:041407107837:secret:sbx-bcd_cab-postgres-IKmbPt'

#
## function definitions
#
def lambda_handler(event, context):
    print("event: {}".format(event))
    msg = {}
   #config = {}
    records = []
   
    #response = execute_statement("SELECT parmval_nu FROM parm WHERE parmname = 'CAB_SALT_LEN'",[])
    #for record in response['records']: config['CAB_SALT_LEN'] = int(record[0]['doubleValue'])
    #print("CAB_SALT_LEN: {}".format(config['CAB_SALT_LEN']))
    
    #response = execute_statement("SELECT parmval_nu FROM parm WHERE parmname = 'CAB_SALT_ITERS'",[])
    #for record in response['records']: config['CAB_SALT_ITERS'] = int(record[0]['doubleValue'])
    #print("CAB_SALT_ITERS: {}".format(config['CAB_SALT_ITERS']))
    
    #salt = os.urandom(config['CAB_SALT_LEN'])
    #key = hashlib.pbkdf2_hmac('sha256',event['pw'].encode('utf-8'),salt,config['CAB_SALT_ITERS'])
    #passwordHash = salt.hex() + key.hex()
    
    sql = """INSERT INTO sec_app_role (app_id,role_name, last_updated) VALUES(:app_id,:role_name,CURRENT_TIMESTAMP)"""
    parameter = [
                    {'name':'app_id','value':{'longValue':event['app_id']}},
                    {'name':'role_name','value':{'stringValue':event['role_name']}}
                ]

    response = execute_statement(sql,parameter)
    # msg['insertResponse'] = response
    # TODO - Add error handling (including at a minimum: timout and duplicate key)

    sql = "SELECT app_id,role_id,role_name, last_updated FROM sec_app_role WHERE role_name = :role_name"
    parameter = [{'name':'role_name','value':{'stringValue':event['role_name']}}]
    response = execute_statement(sql,parameter)
    # msg['selectResponse'] = response
    # TODO - Add error handling (including timout)    

    for record in response['records']:
        role = {}
        role['app_id'] = record[0]['longValue']
        role['role_id'] = record[1]['longValue']
        role['role_name'] = record[2]['stringValue']
        role['last_udpated'] = record[3]['stringValue']
        records.append(role)
    msg['role'] = records
    
    return msg

    
def execute_statement(sql,params):
    print("SQL: {}".format(sql))
    print("PARAMS: {}".format(params))
    response = rds_client.execute_statement(
        secretArn = db_credentials_secret_store_arn,
        database = database_name,
        resourceArn = db_cluster_arn,
        sql = sql,
        parameters = params
        )
    return response


       

