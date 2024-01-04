# Python scripts
This repository is intended for storing Python scripts for the purpose of learning and developing new skills. 

## Keylogger

### Project Disclaimer:
This project is undertaken solely for educational purposes, and there is no intention of engaging in any malicious activities. It is created with the sole purpose of learning and improving skills. Any use of the project for harmful or unethical actions is strictly discouraged.

### Description
The keylogger works as follows:
If executed, it will run until the process is killed or interrupted. It works by logging all keystrokes and captures screenshots every minute by default. The script saves the screenshots and logs in the *logs* and *imgs* directories. 

### Types of Logs:
There are two types of logs:
- **Raw:** This type of log records all the keystrokes in the order the user inputs them.
- **Processed:** This type of log only records alphanumeric characters, with the goal of storing messages in a readable format.

### Credentials
If you want to try it you must implement the following script named **credentials.py** and place it in *src* folder:

```
def get_credentials():
    """
    Return a dictionary containing the necessary credentials for accessing the Telegram API.

    :return: A dictionary with the following keys:
             - "TOKEN": The access token for the Telegram bot.
             - "CHAT_ID": The ID of the chat to which the bot will send messages.
    :rtype: dict
    """
    return {
        "token": token,
        "chat_id": chat_id
    }
```
### Understanding Telegram Bot Credentials
When working with Telegram bots, two key components are essential for communication: the `token` and the `chat_id`.

#### Token
The `token` serves as a unique identifier for your Telegram bot. It is provided by the BotFather, Telegram's tool for creating and managing bots. This token is crucial for your Python script to authenticate and interact with the Telegram API, allowing your bot to send and receive messages. Ensure that you replace the placeholder `token` in the script with the actual token assigned to your bot by the BotFather.

#### Chat_id
The `chat_id` represents the unique identifier for a specific chat or conversation on Telegram. 
To obtain the `chat_id` for your Telegram bot, start a chat with the bot, send a message to trigger an update, and make a request to the Telegram Bot API using the URL `https://api.telegram.org/bot{TOKEN}/getUpdates`, replacing `{TOKEN}` with your actual bot token. Inspect the JSON response for the `chat` object within the `message` object, which contains the `chat_id`. Use the obtained `chat_id` in your Python script to ensure seamless communication with the Telegram API.
