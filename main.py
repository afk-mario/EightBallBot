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
import logging, coloredlogs
from logging.handlers import RotatingFileHandler
import time

log_path = join(dirname(__file__), 'log.log')
dotenv_path = join(dirname(__file__), '.env')
ini_path = join(dirname(__file__), 'config.ini')
load_dotenv(dotenv_path)
config = {}
logger = {}
t = {}
last_update = 0
lastWasAQuestion = False
lastMsgId = 0
botName = 'EightBallBot'
token = os.environ.get("TOKEN")
startTxt = "Hi! I'm a bot developed by @arlefreak to answer your questions \nAvailable commands: \n- /start \n- /info \n- /help \n- /answer"
infoTxt  = "Author: @arlefreak \nGithub: https://github.com/Arlefreak/EightBallBot \nRate: https://telegram.me/storebot?start=EightBallBot\n\nDisclaimer: \nBy using this bot you agree that your doing so at your own risk. Authors will not be responsible for any choices based on advices from this bot. Informations displayed on our answers are not necessarily based on facts."
helpTxt = "Eight Ball Bot \n\nThis fortune-telling / advice seeking bot will help you with tough choices in your life. \n\n Commands: \n/answer - I will summon the dark forces to answer your question* /help - This message will be shown \n /info - Show more info about me \n\nFor Example: \n/answer will I ever find love? \n\n*make sure you as a question that can be answered with YES or NO, I will do my best to help you out."
stopTxt  = ["You can't stop me", "You can't stop progress", "NO", "Never",
"What is dead may never die, \n But rises again, harder and stronger"]
helpAnswersTxt = [
"Go ahead and ask me",
"I'm waiting for your question...",
"I need a question",
"Ask",
]

answers = [
"It is certain",
"It is decidedly so",
"Without a doubt",
"Yes definitely",
"You may rely on it",
"As I see it, yes",
"Most likely",
"Yes",
"Signs point to yes",
"Try again",
"Ask again later",
"Id'rather not tell you now",
"Cannot predict now",
"Concentrate and ask again",
"Don't count on it",
"My reply is no",
"My sources say no",
"Very doubtful",
"Perhaps",
"Umm...no",
"Your future self says no",
"Be serious",
"JUST DO IT!",
"Gooby pls",
"No",
"Ask me an honest to god question",
"..."
]
commands = {
'start': '/start',
'info': '/info',
'help': '/help',
'answer': '/answer',
'stop': '/stop'
}


def main(argv=None):
    SetLogger()
    if argv is None or len(argv) <= 1:
        Init()
    else:
        print("I don't accept params for the moment")

def SetLogger():
    global logger
    logging.getLogger("requests").setLevel(logging.WARNING)
    logger = logging.getLogger("EightBallBot")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')

    fh = RotatingFileHandler(log_path, mode='a', maxBytes=5*1024*1024, 
                                         backupCount=2, encoding=None, delay=0)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    
    coloredlogs.install(level=logging.DEBUG, show_hostname=False, show_name=False)
    logger.info('Log initialized')

def Init():
    global t
    global last_update
    global config
    t = Bot(token)
    if(t.CheckSettings()):
        config = SafeConfigParser()
        config.read(ini_path)
        last_update = config.getint('main', 'last_update')
        logger.info("-- Init --  " + str(last_update))
        UpdatesLoop()
    else:
        return

def UpdatesLoop():
    global last_update
    global t
    while True:
        logger.info("Checking... " + str(last_update))
        updates = t.GetUpdates(last_update,None,None)
        if(not updates):
            logger.error("Couldn't get udpates")
            return
        for update in updates:
            update = Update(update)
            if last_update < update.update_id:
                if(update.message):
                    msg = update.message
                    command = msg.text
                    answer = ''
                    logger.debug("From: %s" % update.message.from_user)
                    if(command):
                        answer = GetCommand(command)
                    if(answer):
                        if(lastWasAQuestion):
                            # TODO: Move to Wrapper 
                            tp = dict(force_reply = True, selective = True)
                            tmp = json.dumps(tp)
                            lastMsgId = update.message.message_id
                            t.SendMessage(msg.chat.id, answer, None, lastMsgId, tmp)
                        else:
                            t.SendMessage(msg.chat.id, answer)
                        logger.debug('Answer: ' + answer)
                UpdateLastUpdate(update.update_id)
        time.sleep(3)
    logger.error("ExitLoop!-----------------------------")

def UpdateLastUpdate(i):
    global last_update
    last_update = i
    config.set('main', 'last_update', str(last_update))
    with open(ini_path, 'w') as f:
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
        if("/" in command):
            logger.debug('Command: ' + str(command))
        else:
            logger.debug('Message: ' + str(msg))
        if(command.endswith('@' + botName)):
            command = command[:-(len(botName)+1)]
        if(commands['help'] in command):
            answer = helpTxt
            lastWasAQuestion = False
        elif(commands['answer'] in command):
            if(words and len(words) > 1):
                logger.debug('Question: ' + str(len(words)) + ' - ' + str(msg) )
                answer = answers[randint(0,len(answers)-1)]
            else:
                answer = helpAnswersTxt[randint(0,len(helpAnswersTxt)-1)]
                lastWasAQuestion = True
        elif(commands['start'] in command):
            answer = startTxt
            lastWasAQuestion = False
        elif(commands['info'] in command):
            answer = infoTxt
            lastWasAQuestion = False
        elif(commands['stop'] in command):
            answer = stopTxt[randint(0,len(stopTxt)-1)]
            lastWasAQuestion = False
        else:
            logger.debug("No Command")
            if(lastWasAQuestion):
                answer = answers[randint(0,len(answers)-1)]
                logger.debug('Question: ' + str(len(words)) + ' - ' + str(msg) )
            lastWasAQuestion = False
    return answer

if __name__ == "__main__":
    main(sys.argv)
