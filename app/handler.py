import boto3
import json
import os

USER_POOL_CLIENT_ID = os.environ['USER_POOL_CLIENT_ID']
DEFAULT_PASSWORD = 'L40|=fq;O@#U'

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


def confirm_user(event, context):
    """
    Confirms the registration of a user in the Amazon Cognito User Pool using the confirmation code.

    Args:
        event (dict): The event object containing the HTTP request body.
        context (object): The context object representing the Lambda execution environment.

    Returns:
        dict: A dictionary containing the HTTP response status code and body.
              If successful, returns a 200 status code with a success message.
              If the user is not found or the confirmation code is invalid, returns a 404 or 400 status code with an error message respectively.
              If an unexpected error occurs, returns a 500 status code with an error message.
    """
    
    body = json.loads(event['body'])
    email = body.get('email')
    confirmation_code = body.get('confirmationCode')

    if not email or not confirmation_code:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Email and confirmation code are required"})
        }

    try:
        response = client.confirm_sign_up(
            ClientId=USER_POOL_CLIENT_ID,
            ConfirmationCode=confirmation_code,
            Username=email
        )
        return {
            "statusCode": 200,
            "body": json.dumps({"message": f"User confirmed successfully, response: {response}"})
        }
    except client.exceptions.UserNotFoundException:
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "User not found"})
        }
    except client.exceptions.CodeMismatchException:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid confirmation code"})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": str(e)})
        }
    

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