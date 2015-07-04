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
import logging

log_path = join(dirname(__file__), 'log.log')
dotenv_path = join(dirname(__file__), '.env')
ini_path = join(dirname(__file__), 'config.ini')
load_dotenv(dotenv_path)
config = {}
logger = {}
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
    SetLogger()
    if argv is None or len(argv) <= 1:
        Init()
    else:
        print("I don't accept params for the moment")

def SetLogger():
    global logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    fh = logging.FileHandler(log_path)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.debug('Log Starting.')

def Init():
    t = Bot(token)
    if(t.CheckSettings()):
        global last_update
        global config
        config = SafeConfigParser()
        config.read(ini_path)
        last_update = config.getint('main', 'last_update')
        logger.debug("--- Init --- " + str(last_update))
    else:
        return
    while True:
        updates = t.GetUpdates()
        updt = Update(updates[len(updates)-1])
        logger.debug("Checking... " + str(updt.update_id))
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
                            tp = dict(force_reply = True, selective = True)
                            tmp = json.dumps(tp)
                            lastMsgId = update.message.message_id
                            t.SendMessage(msg.chat.id, answer, None, lastMsgId, tmp)
                        else:
                            t.SendMessage(msg.chat.id, answer)
                        logger.debug('Answer: ' + answer)
    sleep(3)

def UpdateLastUpdate(i):
    global last_update
    last_update = i
    config.set('main', 'last_update', str(last_update))
    with open('config.ini', 'w') as f:
        config.write(f)
    logger.debug("NewUpdate: " + str(last_update))

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
        logger.debug('Command: ' + str(command))
        if(commands['help'] in command):
            answer = helpTxt
            lastWasAQuestion = False
        elif(commands['answer'] in command):
            if(words and len(words) > 1):
                logger.debug('Question: ' + str(len(words)) + ' - ' + str(words[1]) )
                answer = answers[randint(0,len(answers)-1)]
            else:
                answer = helpAnswertTxt
            lastWasAQuestion = True
        else:
            logger.debug("No Command")
            if(lastWasAQuestion):
                answer = answers[randint(0,len(answers)-1)]
            lastWasAQuestion = False
    return answer

if __name__ == "__main__":
    main(sys.argv)
