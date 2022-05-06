ds#
## Imports
#
import boto3

#
## Static and variable declaration
#
rds_client = boto3.client('rds-data')
database_name = 'bcd_cab_sbx'
db_cluster_arn = 'arn:aws:rds:us-east-1:041407107837:cluster:bcd-cab-cluster-sbx'
db_credentials_secret_store_arn = 'arn:aws:secretsmanager:us-east-1:041407107837:secret:sbx-bcd_cab-postgres-IKmbPt'

def lambda_handler(event, context):
    print("event: {}".format(event))
    msg = {}
    records = []
    if event['parmname'] == 'app_id': 
       sql = """INSERT INTO sec_app_user (app_id,last_updated) VALUES(:parmname, CURRENT_TIMESTAMP)"""
       parameter = [{'name':'app_id','value':{'stringValue':event['parmname']}}]
       msg['Message']= 'Successful'
    elif event['parmname'] == 'user_id': 
        sql = """INSERT INTO sec_app_user (user_id,last_updated) VALUES(:parmname, CURRENT_TIMESTAMP)"""
        parameter = [{'name':'user_id','value':{'stringValue':event['parmname']}}]
        msg['Message']= 'Successful'
    elif event['parmname'] == 'role_id': 
       sql = """INSERT INTO sec_app_user (role_id,last_updated) VALUES(:parmname, CURRENT_TIMESTAMP)"""
       parameter = [{'name':'role_id','value':{'stringValue':event['parmname']}}]
        msg['Message']= 'Successful'
    else:
        msg['Message']= 'Invalid parmtype'

    response = execute_statement(sql,parameter)

    # msg['insertResponse'] = response
    # TODO - Add error handling (including at a minimum: timout and does not ex)
    
    
        for record in response['records']:
        parm = {}
        parm['app_id'] = record[0]['longValue']
        parm['user_id']  = record[1]['longValue']
        if parm['role_id'] == 'number': parm['parmval'] = record[2]['stringValue']
        if parm['approved_by'] == 'number': parm['parmval'] = record[3]['stringValue']
        parm['last_udpated'] = record[4]['stringValue']
        records.append(parm)
    msg['parameters'] = records
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