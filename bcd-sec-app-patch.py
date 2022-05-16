#
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
    
    sql="UPDATE sec_app SET app_name = :app_name, organization = :organization, last_updated = CURRENT_TIMESTAMP WHERE app_name = :app_name"
    parameter = [{'name':'app_name','value':{'stringValue':event['app_name']}}, {'name':'organization','value':{'stringValue':event['organization']}}]
    msg['parameters'] = records
    response = execute_statement (sql,parameter)
    return msg
  
    sql = "SELECT app_id,app_name,organization,last_updated FROM sec_app WHERE appname = :appname"
    parameter = [{'name':'appname','value':{'stringValue':event['appname']}}]
    response = execute_statement(sql,parameter)
    
    for record in response['records']:
        parm = {}
        parm['app_id'] = record[0]['stringValue']
        parm['app_name'] = record[1]['stringValue']
        if parm['organization'] == 'string': parm['parmval'] = record[2]['stringValue']
        parm['last_udpated'] = record[3]['stringValue']
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