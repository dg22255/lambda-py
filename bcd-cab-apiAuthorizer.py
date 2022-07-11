def lambda_handler(event, context):
    print(event)
    auth="Deny"
    if event['Resource'] == 'GET':
        if event['authorizationToken'] == 'abcdefghijklmnopqrstuvwxyzBogusToken0123456789':auth="Allow" 
        authResponse = { 
            "principalId": "user",
            "policyDocument":{
                "Version":"2012-10-17",
                "Statement":[
                    {
                        "Action":"execute-api:Invoke",
                        "Resource":"arn:aws:execute-api:us-east-1:041407107837:wqtoft7ru3/*/GET/*",
                        "Effect":auth
                    }
                ]
            }
        }
    elif event['Resource'] == 'DELETE':
        if event['authorizationToken'] == 'abcdefghijklmnopqrstuvwxyzBogusToken0123456789':auth="Allow" 
        authResponse = { 
            "principalId": "user",
            "policyDocument":{
                "Version":"2012-10-17",
                "Statement":[
                    {
                        "Action":"execute-api:Invoke",
                        "Resource":"arn:aws:execute-api:us-east-1:041407107837:wqtoft7ru3/*/DELETE/*",
                        "Effect":auth
                    }
                ]
            }
        }    
    elif event['Resource'] == 'POST':
        if event['authorizationToken'] == 'abcdefghijklmnopqrstuvwxyzBogusToken0123456789':auth="Allow" 
        authResponse = { 
            "principalId": "user",
            "policyDocument":{
                "Version":"2012-10-17",
                "Statement":[
                    {
                        "Action":"execute-api:Invoke",
                        "Resource":"arn:aws:execute-api:us-east-1:041407107837:wqtoft7ru3/*/POST/*",
                        "Effect":auth
                    }
                ]
            }
        }
    else:
        if event['authorizationToken'] == 'abcdefghijklmnopqrstuvwxyzBogusToken0123456789':auth="Allow" 
        authResponse = { 
            "principalId": "user",
            "policyDocument":{
                "Version":"2012-10-17",
                "Statement":[
                    {
                        "Action":"execute-api:Invoke",
                        "Resource":"arn:aws:execute-api:us-east-1:041407107837:wqtoft7ru3/*/PATCH/*",
                        "Effect":auth
                    }
                ]
            }
        }
    return authResponse