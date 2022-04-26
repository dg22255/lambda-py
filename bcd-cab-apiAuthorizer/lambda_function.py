def lambda_handler(event, context):
    print(event)
    auth="Deny"
    if event['authorizationToken'] == 'abcdefghijklmnopqrstuvwxyzBogusToken0123456789':auth="Allow" 
    authResponse = { 
        "principalId": "user",
        "policyDocument":{
            "Version":"2012-10-17",
            "Statement":[
                {
                    "Action":"execute-api:Invoke",
                    "Resource":"arn:aws:execute-api:us-east-1:041407107837:wqtoft7ru3/*/GET/parmlist",
                    "Effect":auth
                }
            ]
        }
    }
    return authResponse