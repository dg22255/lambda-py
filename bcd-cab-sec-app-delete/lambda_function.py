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
   
    sql = "Delete from sec_app Where app_name =:app_name"
    parameter = [{'name':'app_name','value':{'stringValue':event['app_name']}}]
    msg['Message']='Delete Successful'
    
    response = execute_statement(sql,parameter)
    return msg
    # msg['insertResponse'] = response
    # TODO - Add error handling (including at a minimum: timout and does not ex)
    
    
    sql = "SELECT app_id, app_name,organization,last_updated FROM sec_app WHERE app_name = :app_name"
    parameter = [{'name':'app_name','value':{'stringValue':event['app_name']}}]
    response = execute_statement(sql,parameter)
    # msg['selectResponse'] = response
    # TODO - Add error handling (including timout)    

    for record in response['records']:
        app = {}
        app['app_id'] = record[0]['longValue']
        app['app_name'] = record[1]['stringValue']
        app['organization'] = record[2]['stringValue']
        app['last_updated'] = record[3]['stringValue']
        records.append(app)
    msg['app'] = records

    
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

