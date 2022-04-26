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
    sql = "SELECT app_id, user_id, role_id, approved_by, last_updated FROM sec_app_user WHERE app_id = :app_id"
    parameter = {'name':'app_id','value':{'stringValue':event['parmname']}}
    parameterset = [parameter]
    response = execute_statement(sql,parameterset)

    for record in response['records']:
        parm = {}
        parm['app_id'] = record[0]['stringValue']
        parm['user_id']  = record[1]['stringValue']
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