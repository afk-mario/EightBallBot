import requests
import json
from time import sleep

# This will mark the last update we've checked
last_update = 0
# Here, insert the token BotFather gave you for your bot.
token = 'YOUR_TOKEN_HERE'
# This is the url for communicating with your bot
url = 'https://api.telegram.org/bot%s/' % token

# We want to keep checking for updates. So this must be a never ending loop
while True:
    # My chat is up and running, I need to maintain it! Get me all chat updates
    get_updates = json.loads(requests.get(url + 'getUpdates').content)
    # Ok, I've got 'em. Let's iterate through each one
    for update in get_updates['result']:
        # First make sure I haven't read this update yet
        if last_update < update['update_id']:
            last_update = update['update_id']
            # I've got a new update. Let's see what it is.
            if 'message' in update:
                # It's a message! Let's send it back :D
                requests.get(url + 'sendMessage', params=dict(chat_id=update['message']['chat']['id'], text=update['message']['text']))
    # Let's wait a few seconds for new updates
    sleep(3)
