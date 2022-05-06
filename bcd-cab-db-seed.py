#
## Imports
#
import boto3
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

# v1
root_email = 'stephen.dishman@tn.gov'
root_first_nme = 'Stephen'
root_last_nme = 'Dishman'
root_pw_init = 'abc123'
app_name = 'BCD CAB'
app_org = 'TN STS BCD'
sec_role = 'sec_admin'

#v2
# No initial values needed here.

#
## Definitions
#

def lambda_handler(event, context):
    l = logger()
    l.msg("event: {}".format(event))
    
    # Parameter validation
    if str(type(event['seedDbVersion'])) == "<class 'int'>" or str(type(event['seedDbVersion'])) == "<class 'float'>":
        seedDbVersion = event['seedDbVersion']
    else:
        l.msg("Invalid seedDbVersion passed: {}".format(event['seedDbVersion']),3)
        l.msg("seedDbVersion type: {}".format(type(event['seedDbVersion'])),3)
        msg['status']=400
        msg['action']="ERROR: Invalid seedDbVersion"
    
    l.msg("Seeding values for version {} of the database".format(seedDbVersion))

    #
    # Increment database version up to seedDbVersion
    #
    if seedDbVersion == 1:
        
        # v0 => v1  Initialize parm and user tables
        l.msg("Seeding data in dababase version 1.0")
        
        l.msg("Recording salt length.")
        execute_statement("""INSERT INTO parm(parmname,parmtype,parmval_nu) 
                                  VALUES ('CAB_SALT_LEN','number',32)
                             ON CONFLICT (parmname) DO UPDATE 
                                     SET parmtype='number',
                                         parmval_nu=32,
                                         last_updated=CURRENT_TIMESTAMP
                                         ;""")

        l.msg("Recording salt iterations.")
        execute_statement("""INSERT INTO parm(parmname,parmtype,parmval_nu) 
                                  VALUES ('CAB_SALT_ITERS','number',10003)
                             ON CONFLICT (parmname) DO UPDATE 
                                     SET parmtype='number',
                                         parmval_nu=10003,
                                         last_updated=CURRENT_TIMESTAMP
                                         ;""")

        ## l.msg("Inserting base values for: sec_user")
        ## pw = hashlib.pbkdf2_hmac('sha256',root_pw_init.encode('utf-8)'),salt,100003)
        ## execute_statement("""INSERT INTO sec_user(email,first_nme,last_nme,pw,is_active,is_verified) 
        ##                           VALUES ('{}','{}','{}',{},1,1)
        ##                      ON CONFLICT (email) DO UPDATE
        ##                              SET a ;""".format(root_email,root_first_nme,root_last_nme,pw))
                                    
        ## l.msg("Inserting base values for: sec_app")
        ## execute_statement("""INSERT INTO sec_app(app_name,organization)
        ##                           VALUES ('{}','{}')
        ##                                  ;""".format(app_name,app_org))

        ## l.msg("Getting app_id to create role.",0)
        ## response = execute_statement("SELECT app_id FROM sec_app WHERE app_name='{}' AND organization='{}';".format(app_name,app_org))
        ## results = response['records']
        ## for result in results:
        ##     app_id = result[0]['longValue']
        ## l.msg("Inserting base role for: sec_app_role")
        ## execute_statement("""INSERT INTO sec_app_role(app_id,role_name)
        ##                           VALUES ({},'{}')
        ##                                  ;""".format(app_id,sec_role))

        ## l.msg("Getting user_id to assign role.",0)
        ## response = execute_statement("SELECT user_id FROM sec_user WHERE email='{}';".format(root_email))
        ## results = response['records']
        ## for result in results:
        ##     user_id = result[0]['longValue']

        ## l.msg("Getting role_id to assign role.",0)
        ## response = execute_statement("SELECT role_id FROM sec_app_role WHERE app_id = {} AND role_name = ;".format(root_email))
        ## results = response['records']
        ## for result in results:
        ##     role_id = result[0]['longValue']
        
        ## l.msg("Inserting base role for: sec_app_user")
        ## execute_statement("""INSERT INTO sec_app_user (app_id,user_id,role_id,approved_by)
        ##                           VALUES ({},{},{},{})
        ##                           ;""".format(app_id,user_id,role_id,user_id))

        
    if seedDbVersion == 2:
        
        # v1 => v2  Initialize cab and zd tables
        l.msg("Seeding data in dababase version 2.0")
        
        l.msg("Inserting base values for: vals_responsible_agency")
        execute_statement("""INSERT INTO vals_responsible_agency (val) 
                             VALUES ('Business and Community Development Domain (the domain IT)'),
                                    ('Department of Economic and Community Development'),
                                    ('Department of Labor and Work Force Development'),
                                    ('Department of Revenue'),
                                    ('Department of Tourism'),
                                    ('Strategic Technology Solutions (STS)'),
                                    ('None')
                                 ON CONFLICT (val) DO NOTHING
                                    ;""")

        l.msg("Inserting base values for: vals_data_source")
        execute_statement("""INSERT INTO vals_data_source (val)
                             VALUES ('RFS'),
                                    ('ServiceNow'),
                                    ('Solutions Delivery (PMO)'),
                                    ('STS Change Calendar'),
                                    ('ZenDesk'),
                                    ('None'),
                                    ('Other')
                                 ON CONFLICT (val) DO NOTHING
                                    ;""")

        l.msg("Inserting base values for: vals_reason_for_change")
        execute_statement("""INSERT INTO vals_reason_for_change (val)
                             VALUES ('Business Project Deployment'),
                                    ('IT Project Deployment'),
                                    ('Service Request - Break Fix'),
                                    ('Service Request - Enhancement'),
                                    ('Other'),
                                    ('other'),
                                    ('None')
                                 ON CONFLICT (val) DO NOTHING
                                    ;""")

        l.msg("Inserting base values for: vals_cab_status")
        execute_statement("""INSERT INTO vals_cab_status (val)
                             VALUES ('Open'),('Closed'),('open'),('closed'),('None'),('none')
                                 ON CONFLICT (val) DO NOTHING;""")

        l.msg("Inserting base values for: vals_change_type")
        execute_statement("""INSERT INTO vals_change_type (val)
                             VALUES ('Minor'),('Major'),('Emergency'),('Communication Item')
                                 ON CONFLICT (val) DO NOTHING;""")

        l.msg("Inserting base values for: vals_deployment_status")
        execute_statement("""INSERT INTO vals_deployment_status (val)
                             VALUES ('Awaiting approval'),
                                    ('Approved – awaiting deployment'),
                                    ('Denied'),
                                    ('Deployment successful'),
                                    ('Deployment failed'),
                                    ('Withdrawn'),
                                    ('N/A - Info only'),
                                    ('None'),
                                    ('none'),
                                    ('Deployment Successful')     
                                 ON CONFLICT (val) DO NOTHING
                                    ;""")

        l.msg("Inserting base values for: vals_category")
        execute_statement("""INSERT INTO vals_category (val) 
                             VALUES ('MM'),('SMM'),('None')
                                 ON CONFLICT (val) DO NOTHING;""")

        l.msg("Inserting base values for: vals_reoccurence")
        execute_statement("""INSERT INTO vals_reoccurence (val)
                             VALUES ('3rd Thurs'),('4th Friday'),('4th Sat'),('Adhoc'),('Continuously'),('None')
                                 ON CONFLICT (val) DO NOTHING;""")

    msg['status']=200                                
    return msg
   
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
