# Retranslator
Telegram client that forwards all messages from the selected channels/chats to one another

![](https://github.com/Jipok/TelegramRetranslator/blob/master/screenshot.png)

## Installation
1. Need python 3.5 or higher
2. `pip3 install telethon`
3. `wget https://raw.githubusercontent.com/Jipok/TelegramRetranslator/master/retranslator.py`
4. Register app on my.telegram.org
5. Change the API_HASH and API_ID in the script to values from my.telegram.org

## Run
1. `python3 retranslator.py`

*or*
```
chown +x ./retranslator.py
./retranslator.py
```
2. Log in
3. Open normal telegram client
4. Find a chat with the retranslator bot. There should be a list of dialogs with their id.
5. Select the channel/chat id where the messages will be forwarded.
6. Select the id of chats and channels from where messages should be forwarded.
7. Selecting same id again will remove chat/channel from forwarding.

## Multiple accounts
The script saves two files:
- `default.id_list` which contains the id list. The first ID in the file is the target
- `default.session` which contains data for authentication. This file is processed by telethon.

You can give the script another profile name:
```
python3 retranslator.py another_name
# or
./retranslator.py another_name
```
