import tweepy
from telethon import TelegramClient, events
from datetime import datetime
import twitter_secs as tt
import telegram_secs as te
from rich import pretty, print

pretty.install()

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

chat = "Click&Tweet"
client = TelegramClient("anon", te.api_id, te.api_hash)
print("Waiting for new Telegram message event...")


@client.on(events.NewMessage(chat))
async def my_event_handler(event):

    # print(chath, senderh, chat_idh, sender_idh)

    def tweet(msg):
        # Write message whatever you want to post in twitter
        api.update_status(msg + " #LaxzTweeted")

    if "WhatsHappeningInMyanmar" in event.raw_text:
        print(event.text)
        try:
            tweet(event.text)
            print(f"{datetime.now()}, Tweeted.")
        except tweepy.error.TweepError:
            chat_event = await event.get_chat()
            sender_event = await event.get_sender()
            chat_id = event.chat_id
            sender_id = event.sender_id
            print(
                [
                    f"Chat : {chat_event}",
                    f"ChatID : {chat_id}",
                    f"Sender : {sender_event}",
                    f"SenderID : {sender_id}",
                ]
            )
            print(event.text)
            print(f"{datetime.now()}, Cannot Tweet!")
        # await event.reply('auto reply to event "Click To Tweet", tweeted!')


client.start()
client.run_until_disconnected()
