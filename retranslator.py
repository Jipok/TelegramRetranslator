#!/usr/bin/env python3
from telethon import TelegramClient, events, utils, sync
from pathlib import Path
import asyncio
#import socks #pip install pysocks
import traceback, sys


API_ID = YOUR_API_ID
API_HASH = 'YOUR_API_HASH'
BOT_ID = 'JipokTestBot'

###################################################################################

if len(sys.argv) < 2:
    sys.argv.append("default")

id_list_file = Path(sys.argv[1] + ".id_list")
id_list_file.touch() # Create if not exists
id_list = []

with id_list_file.open('r') as file:
    for line in file:
        tmp = line.strip()
        if len(tmp):
            id_list.append(int(tmp))

if len(id_list):
    TARGET = id_list[0]
else:
    TARGET = None

client = TelegramClient(sys.argv[1], API_ID, API_HASH,
                        #proxy=(socks.SOCKS5, "localhost", int(4567)),
                        )

sent_messages = {}
async def send(text, index = 0):
    # Edit previous messages if available
    if index in sent_messages:
        try:
            sent_messages[index] = await client.edit_message(sent_messages[index], text)
        except:
            pass
    # Or send new
    else:
        sent_messages[index] = await client.send_message(BOT_ID, text)

async def list_dialogs():
    dialogs = await client.get_dialogs()
    tmp = ""
    i = 1

    for dialog in reversed(dialogs):
        eid = dialog.entity.id
        name = utils.get_display_name(dialog.entity)

        if TARGET and eid == TARGET:
            tmp +=  "====== **TARGET** ======\n"
            tmp += ">> /%s: **%s** \n" % (eid, name)
            tmp +=  "========================\n"
        elif eid in id_list:
            tmp += ">> /%s: **%s** \n" % (eid, name)
        else:
            tmp += "/%s: %s \n" % (eid, name)
        # Split into multiple messages if there is a lot of text
        if len(tmp) > 3000:
            await send(tmp, i)
            i += 1
            tmp = ""
    if tmp != "":
        await send(tmp, i)
    
    # Send help message
    if TARGET:
        await send("Click on chat id above to toggle retranslation")
    else:
        await send("Select targert from a list")

# Handle messages sent to the BOT_ID as commands
@client.on(events.NewMessage(outgoing=True))
async def command_handler(event):
    try:
        global id_list
        global TARGET
        msg = event.message
        if msg.to_id is None:
            return
        if not hasattr(msg.to_id, 'user_id'):
            return
        if msg.to_id.user_id != BOT_ID:
            return

        # Toggle user/chat/channel for retranslation
        if (msg.message[0] == "/") and (len(msg.message) > 2):
            tmp = int(msg.message[1:])
            info = msg.message + " " + utils.get_display_name(await client.get_entity(tmp))
            if not TARGET:
                id_list.append(tmp)
                TARGET = tmp
                print("\x1b[32m SELF  \x1b[0m: Select target %s" % tmp)
            elif tmp == TARGET:
                id_list.clear()
                print("\x1b[31m SELF  \x1b[0m: Remove target %s" % tmp)
                TARGET = None
            elif tmp in id_list:
                id_list.remove(tmp)
                print("\x1b[31m SELF  \x1b[0m: Del %s" % tmp)
            else:
                id_list.append(tmp)
                print("\x1b[32m SELF  \x1b[0m: Add %s" % tmp)
            # Update id_list file
            with id_list_file.open('w') as file:
                for item in id_list:
                    file.write(str(item) + "\n")
            # Update list
            await list_dialogs()
        await msg.delete()
    except Exception as e:
        print('Error:\n', traceback.format_exc())
        await client.delete_dialog(BOT_ID)
        sent_messages.clear()
        await client.send_message(BOT_ID, "https://github.com/Jipok/TelegramRetranslator by @Jipok")
        await list_dialogs()

@client.on(events.NewMessage(incoming=True))
async def message_handler(event: events.NewMessage.Event):
    try:
        msg = event.message
        if hasattr(msg.to_id, 'channel_id'):
            sender_id = msg.to_id.channel_id
        elif hasattr(msg.to_id, 'chat_id'):
            sender_id = msg.to_id.chat_id
        elif hasattr(msg, 'from_id'):
            sender_id = msg.from_id

        # Forward message if need
        if sender_id in id_list:
            sender = await client.get_entity(sender_id)
            await client.forward_messages(TARGET, [msg])
    except Exception as e:
        print('Error:\n', traceback.format_exc())


def main():
    client.get_dialogs(limit=900) # Fix
    client.send_message(BOT_ID, "/start")
    # Clear chat with bot
    client.delete_dialog(BOT_ID)
    # Send start messages
    client.send_message(BOT_ID, "https://github.com/Jipok/TelegramRetranslator by @Jipok")
    asyncio.ensure_future(list_dialogs())


with client:
    main()
    print("Successfully started")
    print("Open your telegram client")
    client.run_until_disconnected()
