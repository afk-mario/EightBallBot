import requests
from random import randint
import json
from time import sleep
import os
from os.path import join, dirname
from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
last_update = 719885425
token = os.environ.get("TOKEN")
url = 'https://api.telegram.org/bot%s/' % token
helpTxt = "This a bot developed by @arlefreak to answer you'r questions \n /help to show this message \n /answer to answer you'r questions"
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
    if argv is None:
        Init()

def Init():
    global last_update
    while True:
        print("Checking...")
        # My chat is up and running, I need to maintain it! Get me all chat updates
        get_updates = json.loads(requests.get(url + 'getUpdates').content)
        # Ok, I've got 'em. Let's iterate through each one
        for update in get_updates['result']:
            # First make sure I haven't read this update yet
            print(last_update)
            if last_update < update['update_id']:
                last_update = update['update_id']
                # I've got a new update. Let's see what it is.
                if 'message' in update:
                    # It's a message! Let's send it back :D
                    # requests.get(url + 'sendMessage', params=dict(chat_id=update['message']['chat']['id'], text=update['message']['text']))
                    command = update['message']['text']
                    if(command):
                        answer = GetCommand(update['message']['text'])
                    if(answer):
                        requests.get(url + 'sendMessage', params=dict(chat_id=update['message']['chat']['id'], text=answer))
    sleep(3)

def GetCommand(msg):
    answer = ''
    if(msg):
        command = msg.split()[:1]
        if(commands['help'] in command):
            answer = helpTxt
            print(str(command))
            print(answer)
        elif(commands['answer'] in command):
            answer = answers[randint(0,len(answers)-1)]
    return answer

if __name__ == "__main__":
    main()
