#!/bin/env python3
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError
import configparser
import os, sys
import csv
import random
import time

re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"
lb = "\033[1;34m"
wh = "\033[1;37m"
SLEEP_TIME = 30

class main():

    def banner():
        
        print(f"""
    {re}╔╦╗{cy}┌─┐┌─┐┌─┐┌─┐┬─┐{re}╔═╗
    {re} ║ {cy}├─┐├┤ ├─┘├─┤├┬┘{re}╚═╗
    {re} ╩ {cy}└─┘└─┘┴  ┴ ┴┴└─{re}╚═╝
    
            """)

    def send_sms():
        try:
            cpass = configparser.RawConfigParser()
            cpass.read('config.data')
            api_id = cpass['cred']['id']
            api_hash = cpass['cred']['hash']
            phone = cpass['cred']['phone']
        except KeyError:
            main.banner()
            print(re + "[!] Config file is not found, execute: ",lb+"Setting.bat\n")
            sys.exit(1)

        client = TelegramClient(phone, api_id, api_hash)
         
        client.connect()
        if not client.is_user_authorized():
            client.send_code_request(phone)
            main.banner()
            client.sign_in(phone, input(gr + '[+] Input the code from Telegram: ' + re))

        main.banner()
        input_file = sys.argv[1]
        users = []
        with open(input_file, encoding='UTF-8') as f:
            rows = csv.reader(f,delimiter=",",lineterminator="\n")
            next(rows, None)
            for row in rows:
                user = {}
                user['username'] = row[0]
                user['id'] = int(row[1])
                user['access_hash'] = int(row[2])
                user['name'] = row[3]
                users.append(user)
        print(gr+"[1] send by user identifier (user id)"
           "\n[2] send by username (username) ")
        mode = int(input(gr+"Choose the parameter : "+re))
         
        message = input(gr+"[+] Input the text of your message : "+re)
         
        for user in users:
            if mode == 2:
                if user['username'] == "":
                    continue
                receiver = client.get_input_entity(user['username'])
            elif mode == 1:
                receiver = InputPeerUser(user['id'],user['access_hash'])
            else:
                print(re+"[!] Invalid mode, The exit is being executed")
                client.disconnect()
                sys.exit()
            try:
                print(gr+"[+] Sending the message:", user['name'])
                client.send_message(receiver, message.format(user['name']))
                print(gr+"[+] Waiting {} seconds".format(SLEEP_TIME))
                time.sleep(1)
            except PeerFloodError:
                print(re+"[!] The message about flood error from Telegram is received. "
                       "\n[!] The scenario is being halted currently. "
                       "\n[!] Repeat the effort in awhile, please, please.")
                client.disconnect()
                sys.exit()
            except Exception as e:
                print(re+"[!] Error:", e)
                print(re+"[!] Proceeding... ")
                continue
        client.disconnect()
        print("The task is completed. The message is sent to all the users.")



main.send_sms()
