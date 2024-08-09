import boto3
import json
import time

def start_state_machine(body):
    # Create a session with AWS credentials
    session = boto3.Session(
        aws_access_key_id='',
        aws_secret_access_key='',
        region_name=''
    )
    
    # Create a client to interact with AWS Step Functions
    step_functions_client = session.client('stepfunctions')
    
    # Define the ARN of the Step Function that you want to start
    state_machine_arn = 'arn:aws:states::stateMachine:apiProxyStateMachine'
    
    # Define the input to pass to the Step Function
    input_data = body
    
    # Start the Step Function with the specified input
    response = step_functions_client.start_execution(
        stateMachineArn=state_machine_arn,
        input=json.dumps(input_data)
    )
    
    # Wait for the execution to complete
    while True:
        execution_status = step_functions_client.describe_execution(
            executionArn=response['executionArn']
        )['status']
        if execution_status in ['SUCCEEDED', 'FAILED', 'ABORTED']:
            break
    
    execution_output = step_functions_client.describe_execution(
        executionArn=response['executionArn']
    )
    
    if(execution_output['status'] == 'SUCCEEDED'):
        return execution_output['output']
    else:
        return execution_output['status']

def lambda_handler(event, context):
    event = event["body"]
    data = start_state_machine(event)
    response = json.loads(data)
    return {
        "statusCode": response["statusCode"],
        "body": response["body"]
    }
