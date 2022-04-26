#
## Imports
#
import boto3

#
## Statics and variable declaration
#
rds_client = boto3.client('rds-data')
database_name = 'bcd_cab_sbx'
db_cluster_arn = 'arn:aws:rds:us-east-1:041407107837:cluster:bcd-cab-cluster-sbx'
db_credentials_secret_store_arn = 'arn:aws:secretsmanager:us-east-1:041407107837:secret:sbx-bcd_cab-postgres-IKmbPt'

#
## Definitions
#

def lambda_handler(event, context):
    print("event: {}".format(event))
    response = execute_statement("SELECT * FROM {};".format(event['table']))
    return response
   
def execute_statement(sql):
    response = rds_client.execute_statement(
        secretArn = db_credentials_secret_store_arn,
        database = database_name,
        resourceArn = db_cluster_arn,
        sql = sql
        )
    return response