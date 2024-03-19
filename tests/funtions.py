import requests
import json

API_URL = ''

def test_register_user(email: str):
    """
    Registers a new user via API call.

    Args:
        email (str): The email of the user to register.
    """
    url = f'{API_URL}/register-user'
    headers = {'Content-Type': 'application/json'}
    data = {"email": email}

    response = requests.post(url, headers=headers, data=json.dumps(data))

    print(json.loads(response.content.decode())['message'])


def test_confirm_user(email: str, confirmation_code: str):
    """
    Confirms the registration of a user via API call.

    Args:
        email (str): The email of the user.
        confirmation_code (str): The confirmation code received by the user.
    """
    url = f'{API_URL}/confirm-user'
    headers = {'Content-Type': 'application/json'}
    data = {"email": email, "confirmationCode": confirmation_code}

    response = requests.post(url, headers=headers, data=json.dumps(data))

    print(json.loads(response.content.decode())['message'])


def test_authenticate_user(email: str):
    """
    Authenticates a user via API call.

    Args:
        email (str): The email of the user to authenticate.
    """
    url = f'{API_URL}/authenticate-user'
    headers = {'Content-Type': 'application/json'}
    data = {"email": email}

    response = requests.post(url, headers=headers, data=json.dumps(data))

    print(json.loads(response.content.decode()))
