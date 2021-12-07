import tweepy
from telethon import TelegramClient, events
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.types import InputStickerSetID
import datetime
from rich import pretty, print
from rich.console import Console

from credentials import *
import textcolors as css

pretty.install()
console = Console()

# Authenticate to Twitter
auth = tweepy.OAuthHandler(twitter_app_api_key, twitter_app_api_secret)
auth.set_access_token(twitter_access_token, twitter_access_token_secret)
api = tweepy.API(auth)  # Create the actual interface to twitter, using credentials


def getDateTime() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def printMessage(message: str, error: bool) -> None:
    print(f"[red] {getDateTime()} :\n {message}[/red]") if error else print(f"[green] {getDateTime()} :\n {message}[/green]")


try:
    api.verify_credentials()
    printMessage("Authenticated to twitter", False)
except:
    printMessage("Failed to authenticate to twitter", True)


# Specify Channel name to caught broadcasting posts
chat = "Click&Tweet"
# Authenticate to Telegram
client = TelegramClient("anon", telegram_api_id, telegram_api_hash)
# print("Hello", style="#af00ff")
console.print("Waiting for new Telegram message event...", style=css.dodgerblue)


async def sendMessageToTelegram(message: str, event_id: int) -> None:
    await client.send_message(chat, message, comment_to=event_id)

async def sendStickerToTelegram(event_id: int) -> None:
    stickers = await client(GetStickerSetRequest(
    stickerset=InputStickerSetID(
        id=891885078961979401, access_hash=-6312850271542209510
    )))
    await client.send_file(chat, stickers.documents[10], comment_to=event_id)


@client.on(events.NewMessage(chat))
async def my_event_handler(event: events.NewMessage.Event) -> None:
    def make_tweet(msg: str) -> None:
        # Post to twitter
        api.update_status(msg + "\n#LaxzTweeted")

    if "WhatsHappeningInMyanmar" in event.raw_text or "ASIEANengageNUG" in event.raw_text:
        printMessage(
            message=f"-----------------------------------\n {event.text} \n-----------------",
            error=False,
        )
        try:
            make_tweet(msg=event.text)
            printMessage(message="Tweeted", error=False)
            await sendMessageToTelegram(
                message=f"Previous Event- **{event.id}** is Tweeted.",
                event_id=event.id + 1,
            )
            printMessage(message=f"Commented to Message ID : {event.id}", error=False)
        except tweepy.TweepyException as e:
            printMessage(message=f"[red]This need to be tweeted manually.[/red]", error=True)
            if isinstance(e, list) and "code" in e[0] and e[0]["code"] == 187:
                await client.send_message(
                    chat,
                    f"{getDateTime()} => **Error on event** => {event.id} - ```errorCode:{e[0]['code']}```",
                    comment_to=event.id + 1,
                )
                printMessage(message=f"Commented to Message ID : {event.id}", error=True)
                print(f"Error message : {e[0].message}")
            else:
                print(f"[bold magenta] Unhandled Exception : {e} [/bold magenta]")
        print("-----------------------------------")
    elif "Goodnight" in event.raw_text:
        print("\a")
        await sendMessageToTelegram(message="Client is disconnecting ...", event_id=event.id)
        if "Thomas" in event.raw_text:
            await sendMessageToTelegram(message="__Goodnight **Admin Thomas**__.`Be Safe`.", event_id=event.id)
        else:
            await sendMessageToTelegram(message="__Goodnight **Admin 🐼🎋**__. `Be Safe`.", event_id=event.id)
        await sendStickerToTelegram(event_id=event.id)
        printMessage(
            message=f"[orange]{getDateTime()}, Script is gonna stop.[/orange]",
            error=False,
        )
        client.disconnect()
    else:
        print("passed")


client.start()
client.run_until_disconnected()
