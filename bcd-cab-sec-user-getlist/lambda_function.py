
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
    response = execute_statement("SELECT user_id,email,first_nme,last_nme, pw, is_active,is_verified,last_updated FROM sec_user")
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
    
def execute_statement(sql):
    response = rds_client.execute_statement(
        secretArn = db_credentials_secret_store_arn,
        database = database_name,
        resourceArn = db_cluster_arn,
        sql = sql
        )
    return response