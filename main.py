# -*- coding: utf-8 -*-

import sys
import requests
from random import randint
import json
from time import sleep
import os
from os.path import join, dirname
from dotenv import load_dotenv
from configparser import SafeConfigParser
from TelegramBot import *

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
config = {}
last_update = 0
lastWasAQuestion = False
lastMsgId = 0
botName = 'EightBallBot'
token = os.environ.get("TOKEN")
helpTxt = "This a bot developed by @arlefreak to answer you'r questions \n /help to show this message \n /answer to answer you'r questions"
helpAnswertTxt = "Go ahead and ask me"
answers = [
"It is certain",
"It is decidedly so",
"Without a doubt",
"Yes definitely",
"You may rely on it",
"As I see it, yes",
"Most likely",
"Outlook good",
"Yes",
"Signs point to yes",
"Reply hazy try again",
"Ask again later",
"Better not tell you now",
"Cannot predict now",
"Concentrate and ask again",
"Don't count on it",
"My reply is no",
"My sources say no",
"Outlook not so good",
"Very doubtful"
]
commands = {
'help': '/help',
'answer': '/answer'
}


def main(argv=None):
    if argv is None or len(argv) <= 1:
        Init()
    else:
        print("I don't accept params for the moment")

def Init():
    t = Bot(token)
    if(t.CheckSettings()):
        global last_update
        global config
        config = SafeConfigParser()
        config.read('config.ini')
        last_update = config.getint('main', 'last_update')
        print("--- Init --- " + str(last_update))
    else:
        return
    while True:
        print("Checking...")
        updates = t.GetUpdates()
        # Ok, I've got 'em. Let's iterate through each one
        for update in updates:
            update = Update(update)
            if last_update < update.update_id:
                UpdateLastUpdate(update.update_id)
                if(update.message):
                    msg = update.message
                    command = msg.text
                    answer = ''
                    if(command):
                        answer = GetCommand(command)
                    if(answer):
                        if(answer == helpAnswertTxt):
                            # TODO: Move to Wrapper 
                            tp = dict(force_reply = True)
                            tmp = json.dumps(tp)
                            lastMsgId = update.message.message_id
                            t.SendMessage(msg.chat.id, answer, None, lastMsgId, tmp)
                        else:
                            t.SendMessage(msg.chat.id, answer)
                        print('Answer: ' + answer)
    sleep(3)

def UpdateLastUpdate(i):
    global last_update
    last_update = i
    config.set('main', 'last_update', str(last_update))
    with open('config.ini', 'w') as f:
        config.write(f)
    print("NewUpdate: " + str(last_update))

def GetCommand(msg):
    answer = ''
    msg = msg.encode("utf-8")
    global lastWasAQuestion
    global lastMsgId
    if(msg):
        command = msg.split()[:1]
        command = str(command)
        words = msg.split()
        if(command.endswith('@' + botName)):
            command = command[:-(len(botName)+1)]
        print('Command: ' + str(command))
        if(commands['help'] in command):
            answer = helpTxt
            lastWasAQuestion = False
        elif(commands['answer'] in command):
            if(words and len(words) > 1):
                print('Question: ' + str(len(words)) + ' - ' + str(words[1]) )
                answer = answers[randint(0,len(answers)-1)]
            else:
                answer = helpAnswertTxt
            lastWasAQuestion = True
        else:
            print("No Command")
            if(lastWasAQuestion):
                answer = answers[randint(0,len(answers)-1)]
            lastWasAQuestion = False
    return answer

if __name__ == "__main__":
    main(sys.argv)
