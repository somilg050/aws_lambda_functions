import json
import requests

def lambda_handler(event, context):
    api_url = "https://api.example.com/data"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return {
            'statusCode': 200,
            'body': json.dumps(response.json())
        }
    except requests.exceptions.RequestException as e:
        return {
            'statusCode': response.status_code if response else 500,
            'body': json.dumps({'error': str(e)})
        }
