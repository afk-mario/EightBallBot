import requests
from random import randint
import json
from time import sleep
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
last_update = 719885454
botName = 'EightBallBot'
token = os.environ.get("TOKEN")
url = 'https://api.telegram.org/bot%s/' % token
helpTxt = "This a bot developed by @arlefreak to answer you'r questions \n /help to show this message \n /answer to answer you'r questions"
helpAnswertTxt = "Type the command /answer and then your question"
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
            if last_update < update['update_id']:
                last_update = update['update_id']
                print(last_update)
                if 'message' in update:
                    # It's a message! Let's send it back :D
                    # requests.get(url + 'sendMessage', params=dict(chat_id=update['message']['chat']['id'], text=update['message']['text']))
                    command = update['message'].get('text','')
                    answer = ''
                    if(command):
                        answer = GetCommand(update['message']['text'])
                    if(answer):
                        requests.get(url + 'sendMessage', params=dict(chat_id=update['message']['chat']['id'], text=answer))
                        print('Answer: ' + answer)
    sleep(3)

def GetCommand(msg):
    answer = ''
    msg = str(msg)
    if(msg):
        command = msg.split()[:1]
        command = str(command)
        words = msg.split()
        if(command.endswith('@' + botName)):
            command = command[:-(len(botName)+1)]
        print(str(command))
        if(commands['help'] in command):
            answer = helpTxt
            print(answer)
        elif(commands['answer'] in command):
            if(words and len(words) > 1):
                print('Question: ' + str(len(words)) + ' - ' + words[1] )
                answer = answers[randint(0,len(answers)-1)]
            else:
                answer = helpAnswertTxt
    return answer

if __name__ == "__main__":
    main()
