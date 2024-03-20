import boto3
import json
import os

USER_POOL_CLIENT_ID = os.environ['USER_POOL_CLIENT_ID']
DEFAULT_PASSWORD = os.environ['DEFAULT_PASSWORD']

client = boto3.client('cognito-idp')
    
def authenticate_user(event, context):
    """
    Authenticates a user in the Amazon Cognito User Pool.

    Args:
        event (dict): The event object containing the HTTP request body.
        context (object): The context object representing the Lambda execution environment.

    Returns:
        dict: A dictionary containing the HTTP response status code and body.
              If successful, returns a 200 status code with a success message and an access token.
              If the user is not found or the credentials are incorrect, returns a 404 or 401 status code with an error message respectively.
              If an unexpected error occurs, returns a 500 status code with an error message.
    """

    body = json.loads(event['body'])
    email = body.get('email')

    if not email:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Email are required"})
        }

    try:
        response = client.initiate_auth(
            ClientId=USER_POOL_CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': DEFAULT_PASSWORD
            }
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "User authenticated successfully", "accessToken": response['AuthenticationResult']['AccessToken']})
        }
    
    except client.exceptions.UserNotFoundException:
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "Email not found"})
        }
    
    except client.exceptions.NotAuthorizedException:
        return {
            "statusCode": 401,
            "body": json.dumps({"message": "Incorrect email"})
        }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": str(e)})
        }