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
   
    sql = "Delete from sec_user Where email=:email"
    parameter = [{'name':'email','value':{'stringValue':event['email']}}]
    msg['Message']='Delete Successful'
    
    response = execute_statement(sql,parameter)
    # msg['insertResponse'] = response
    # TODO - Add error handling (including at a minimum: timout and does not ex)
    
    
    sql = "SELECT user_id, email, first_nme, last_nme, pw, is_active, is_verified, last_updated FROM sec_user Where email=:email"
    parameter = [{'name':'email','value':{'stringValue':event['email']}}]
    msg['Message']='Delete Successful' 
      
    response = execute_statement(sql,parameter)
    # msg['selectResponse'] = response
    # TODO - Add error handling (including timout)    

    for record in response['records']:
        user = {}
        user['user_id'] = record[0]['longValue']
        user['email'] = record[1]['stringValue']
        user['first_nme'] = record[2]['stringValue']
        user['last_nme'] = record[3]['stringValue']
        user['pw'] = record[4]['stringValue']
        user['is_active'] = record[5]['booleanValue']
        user['is_verified'] = record[6]['booleanValue']
        user['last_updated'] = record[7]['stringValue']
        records.append(user)
    msg['user'] = records
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

