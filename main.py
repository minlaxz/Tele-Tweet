# Library imports
import tweepy
from telethon import TelegramClient, events
from datetime import datetime
from rich import pretty, print
from rich.console import Console

# Security key imports
import twitter_secs as tt
import telegram_secs as te
import textcolors as css

pretty.install()
console = Console()

# Authenticate to Twitter
auth = tweepy.OAuthHandler(tt.app_api_key, tt.app_api_secret)
auth.set_access_token(tt.access_token, tt.access_token_secret)

# Creation of the actual interface, using authentication
api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("[green]Twitter Authentication OK[/green]")
except:
    print("[red]Error during twitter authentication[/red]")

# Specify Channel name to caught broadcasting posts
chat = "Click&Tweet"

# Authenticate to Telegram
client = TelegramClient("anon", te.api_id, te.api_hash)

# print("Hello", style="#af00ff")
console.print("Waiting for new Telegram message event...", style=css.dodgetblue)


@client.on(events.NewMessage(chat))
async def my_event_handler(event):
    def make_tweet(msg):
        # Write message whatever you want to post in twitter
        api.update_status(msg + "\n#LaxzTweeted")

    if (
        "WhatsHappeningInMyanmar" in event.raw_text
        or "ASIEANengageNUG" in event.raw_text
    ):
        print("-----------------------------------")
        print(event.text)
        print("---------------")
        try:
            make_tweet(event.text)
            print(f"[green]{datetime.now()}, Tweeted.[/green]")
            await client.send_message(
                chat,
                "Previous Event- {} is Tweeted.".format(event.id),
                comment_to=event.id + 1,
            )
            print(f"Commented to Message ID : {event.id}")
        except tweepy.error.TweepError as e:
            print(f"[bold magenta] {e} [/bold magenta]")
            print(f"[red]{datetime.now()}, This need to be tweeted manually.[/red]")

        # await event.reply("auto reply to event, tweeted!")
        print("-----------------------------------")
    elif "Goodnight" in event.raw_text:
        await client.send_message(
            chat,
            "Event {}, __Goodnight **Admins**__. `Be Safe`.".format(event.id),
            comment_to=event.id,
        )
        # await client.send_file('me', '/home/me/Pictures/holidays.jpg')
        print(f"[orange]{datetime.now()}, Script is gonna stop.[/orange]")

    else:
        pass


client.start()
client.run_until_disconnected()
