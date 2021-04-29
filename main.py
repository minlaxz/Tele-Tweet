import tweepy
from telethon import TelegramClient, events

import twitter_secs as tt
import telegram_secs as te


# Authenticate to Twitter
auth = tweepy.OAuthHandler(tt.app_api_key, tt.app_api_secret)
auth.set_access_token(tt.access_token, tt.access_token_secret)

# Creation of the actual interface, using authentication
api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Twitter Authentication OK")
except:
    print("Error during twitter authentication")

chat = 'Click&Tweet'
client = TelegramClient('anon', te.api_id, te.api_hash)

@client.on(events.NewMessage(chat))
async def my_event_handler(event):
    chath = await event.get_chat()
    senderh = await event.get_sender()
    chat_idh = event.chat_id
    sender_idh = event.sender_id

    # print(chath, senderh, chat_idh, sender_idh)

    def tweet(msg):
        # Sample method, used to update a status, you can write message whatever you want to post in twitter
        api.update_status(msg + " #TweetByLaxz" )
    
    if 'Click To Tweet' in event.raw_text:
        # print(event.raw_text)
        print('Tweeted')
        tweet(event.raw_text)
        await event.reply('auto reply to event "Click To Tweet", tweeted!')

client.start()
client.run_until_disconnected()










