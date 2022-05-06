def lambda_handler(event, context):
    print(event)
    return {
        'status': 200,
        'body': 'abcdefghijklmnopqrstuvwxyzBogusToken0123456789'
    }