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
    sql = """DELETE FROM parm where parmname = (:parmname)"""
    parameter = [{'name':'parmname','value':{'stringValue':event['parmname']}}]
    response = execute_statement(sql,parameter)

    sql = "SELECT parmname,parmtype,parmval_dt,parmval_st,parmval_nu,last_updated FROM parm WHERE parmname = :parmname"
    parameter = [{'name':'parmname','value':{'stringValue':event['parmname']}}]
    response = execute_statement(sql,parameter)
   
    for record in response['records']:
        parm = {}
        parm['parmname'] = record[0]['stringValue']
        parm['parmtype'] = record[1]['stringValue']
        if parm['parmtype'] == 'datetime': parm['parmval'] = record[2]['stringValue']
        if parm['parmtype'] == 'string': parm['parmval'] = record[3]['stringValue']
        if parm['parmtype'] == 'number': parm['parmval'] = record[4]['stringValue']
        parm['last_udpated'] = record[5]['stringValue']
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