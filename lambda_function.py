import json
from discord_bot import client, TOKEN

def lambda_handler(event, context):
    client.run(TOKEN)
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from zip!')
    }