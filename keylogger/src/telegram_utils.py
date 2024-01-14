import os
import json
import requests
from datetime import datetime
import io
import credentials
from constants import CREDENTIAL_FILE_TELEGRAM, CREDENTIAL_DIR

def send_info_telegram(token, chat_id, message='Empty', verbose=False):
    """
    Send a message through Telegram.

    Parameters:
    - token (str): Your Telegram bot token.
    - chat_id (str): Your Telegram chat ID.
    - message (str): The message to send.
    - verbose (bool): If True, print the JSON response. Default is False.

    Returns:
    - dict: The JSON response from the Telegram API.
    """

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {'chat_id': chat_id, 'text': message}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        json_response = response.json()
        if verbose:
            print(json_response)
        return json_response
    except requests.RequestException as e:
        error_message = {'error': f"Failed to send message: {e}"}
        if verbose:
            print(error_message)
        return error_message

def send_image_telegram(token, chat_id, image, caption='Screenshot', verbose=False):
    """
    Send an image through Telegram.

    Parameters:
    - token (str): Your Telegram bot token.
    - chat_id (str): Your Telegram chat ID.
    - image_path (str): Path to the image file.
    - caption (str): Caption for the image. Default is None.
    - verbose (bool): If True, print the JSON response. Default is False.

    Returns:
    - dict: The JSON response from the Telegram API.
    """
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    if caption:
        caption += ' - ' + datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    params = {'chat_id': chat_id, 'caption': caption} if caption else {
        'chat_id': chat_id}

    try:
        # Convert the image to bytes
        img_byte_array = io.BytesIO()
        image.save(img_byte_array, format='PNG')
        img_byte_array.seek(0)
        files = {'photo': img_byte_array}
        response = requests.post(url, params=params, files=files)
        response.raise_for_status()
        json_response = response.json()
        if verbose:
            print(json_response)
        return json_response
    except requests.RequestException as e:
        error_message = {'error': f"Failed to send image: {e}"}
        if verbose:
            print(error_message)
        return error_message
    
def load_credentials_telegram():
    """
    Load the Telegram credentials from the specified directory and file.

    Returns:
        dict: A dictionary containing the Telegram token and chat ID.
            - 'token' (str): The Telegram token.
            - 'chat_id' (str): The Telegram chat ID.
    """
    file_path = CREDENTIAL_DIR + CREDENTIAL_FILE_TELEGRAM

    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            token = data['TOKEN']
            chat_id = data['CHAT_ID']
    else:
        print("File not found:", file_path)
        return {}
    
    return {'token': token, 'chat_id': chat_id}

def load_credentials_telegram_from_script():
    """
    Load the Telegram credentials from a python script

    Returns:
        dict: A dictionary containing the Telegram token and chat ID.
            - 'token' (str): The Telegram token.
            - 'chat_id' (str): The Telegram chat ID.
    """
    return credentials.get_credentials()