#!/usr/bin/env python3
from telethon.sync import TelegramClient  # библиотка telethon
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import configparser  # библиотека загрузки и редактирования конфигов
import os, sys  # библиотека работы с системой
import csv  # библиотека работы с csv файлами
import traceback  # библиотека печати трассировки стека
import time  # библиотека время
import random  # библиотека генератор случацных чисел

re = "\033[1;31m"
gr = "\033[1;32m"
cy = "\033[1;36m"
lb = "\033[1;34m"
wh = "\033[1;37m"

def banner():
    print(f"""
{re}╔╦╗{cy}┌─┐┌─┐┌─┐┌─┐┬─┐{re}╔═╗
{re} ║ {cy}├─┐├┤ ├─┘├─┤├┬┘{re}╚═╗
{re} ╩ {cy}└─┘└─┘┴  ┴ ┴┴└─{re}╚═╝

        """)


cpass = configparser.RawConfigParser()
cpass.read('config.data')  # config reading

try:
    api_id = cpass['cred']['id']
    api_hash = cpass['cred']['hash']
    phone = cpass['cred']['phone']
    client = TelegramClient(phone, api_id, api_hash)
except KeyError:
    banner()
    print(re + "[!] Config file is not found, execute: ",lb+"Setting.bat\n")
    sys.exit(1)

client.connect()                           # connection with the client
if not client.is_user_authorized():
    client.send_code_request(phone)
    banner()
    client.sign_in(phone, input(gr + '[+] Enter the code from Telegram: ' + re))

banner()
input_file = sys.argv[1]
users = []
with open(input_file, encoding='UTF-8') as f:
    rows = csv.reader(f, delimiter=",", lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['access_hash'] = int(row[2])
        user['name'] = row[3]
        users.append(user)

chats = []
last_date = None
chunk_size = 200
groups = []

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup == True:
            groups.append(chat)
    except:
        continue

i = 0
for group in groups:
    print(gr + '[' + cy + str(i) + gr + ']' + cy + ' - ' + group.title)
    i += 1

print(gr + '[+] Chose the group for adding participants')
g_index = input(gr + "[+] Введите номер : " + re)
target_group = groups[int(g_index)]

target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)

print(gr + "[1] add participants by using the identifier of the user (user id)"
           "\n[2] add participant by using the name of the user (username) ")
mode = int(input(gr + "Choose the parameter : " + re))
n = 0
print(users)
print('before for')
for user in users:
    n += 1
    if 1 == 1:
        time.sleep(1)
        try:
            print("Adding {}".format(user['id']))
            if mode == 1:
                if user['username'] == "":
                    continue
                user_to_add = client.get_input_entity(user['username'])
            elif mode == 2:
                user_to_add = InputPeerUser(user['id'], user['access_hash'])
            else:
                sys.exit(re + "[!] You didn't choose the adding option! Choose adding by user id or username.")
            client(InviteToChannelRequest(target_group_entity, [user_to_add]))
            print(gr + "[+] Waiting 10-30 seconds...")
            time.sleep(random.randrange(10, 30))  # time of waiting is mentioned
        except PeerFloodError:
            print(re + "[!] The message about flood error from Telegram is received. "
                       "\n[!] The scenario is being halted currently. "
                       "\n[!] Repeat the effort in awhile, please.")
        except UserPrivacyRestrictedError:
            print(
                re + "[!] The user proscribed to add himself. Skipped.")
        except:
            traceback.print_exc()
            print(re + "[!] The error occured.")
            continue
