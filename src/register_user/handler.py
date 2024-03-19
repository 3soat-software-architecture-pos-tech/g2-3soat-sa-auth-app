import boto3
import json
import os

USER_POOL_CLIENT_ID = os.environ['USER_POOL_CLIENT_ID']
DEFAULT_PASSWORD = os.environ['DEFAULT_PASSWORD']

client = boto3.client('cognito-idp')

def register_user(event, context):
    """
    Registers a new user in the Amazon Cognito User Pool.

    Args:
        event (dict): The event object containing the HTTP request body.
        context (object): The context object representing the Lambda execution environment.

    Returns:
        dict: A dictionary containing the HTTP response status code and body.
              If successful, returns a 200 status code with a success message.
              If the user already exists, returns a 400 status code with an error message.
              If an unexpected error occurs, returns a 500 status code with an error message.
    """

    body = json.loads(event['body'])
    email = body.get('email')

    if not  email:
        response = {
            "statusCode": 400,
            "body": json.dumps({"message": "Email are required fields"})
        }
        return response

    try:
        response = client.sign_up(
            ClientId=USER_POOL_CLIENT_ID,
            Username=email,
            Password=DEFAULT_PASSWORD,
            UserAttributes=[
                {'Name': 'email', 'Value': email}
            ]
        )
        
        response = {
            "statusCode": 200,
            "body": json.dumps({"message": "User registered successfully. Please check your email to verify your account."})
        }

    except client.exceptions.UsernameExistsException:
        response = {
            "statusCode": 400,
            "body": json.dumps({"message": "User already exists"})
        }
        
    except Exception as e:
        response = {
            "statusCode": 500,
            "body": json.dumps({"message": str(e)})
        }

    return response
