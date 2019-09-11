import discord
import asyncio
import feedparser


'''
A Discord bot that sends you messages whenever there's an update on your favorite YouTube channels, podcasts, or whatever uses a RSS feed.
All you need is a .txt file containing the name and feed URL, separated by a ";".
Example: "PewDiePie;https://www.youtube.com/feeds/videos.xml?channel_id=UC-lHJZR3Gqxm24_Vd_AJ5Yw;New entry
          YouTube;https://www.youtube.com/feeds/videos.xml?channel_id=UC-lHJZR3Gqxm24_Vd_AJ5YwUCBR8-60-B28hp2BmDPdntcQ;New entry
          ...
          Name;URL;Last updated entry
          ..."

A verification is made every WAIT_TIME minutes. You can specify this WAIT_TIME below. If there is an update, a message is sent 
to the specified Discord channel containing the name, date and link of the last entry.
You can add and remove entries with "!add" and "!remove";
Clear the chat with "!clear";
And check the last entry for a single feed with "!check FeedName"
'''


# Configuration
TOKEN = 'YOUR TOKEN HERE'
CHANNEL_ID = YOUR_DISCORD_CHANNEL_ID_HERE
WAIT_TIME = 300
FEED_FILE_PATH = "Feed.txt"
###


FEEDS = []
CLIENT = discord.Client()


class Feed:
    name = ""
    url = ""
    last_modified = ""
    title = ""
    link = ""
    
    def __init__(self, name, url, link):
        self.name = name
        self.url = url
        self.link = link

    pass


@CLIENT.event
async def on_message(msg):
    # Ping
    if msg.content == "!ping":
        await msg.channel.send("Pong!")
        print("Pong!")

    # Stop the bot
    if msg.content == '!stop':
        print("Stopping by command...")
        await msg.channel.send("Stopping...")
        await CLIENT.logout()

    # Leave guild
    if msg.content == "!leave":
        print("Leaving server...")
        await msg.channel.send("Leaving...")
        await msg.guild.leave()

    # Add name and url to FeedItToMe
    if msg.content == "!add":
        await msg.channel.send("Tell me the name: ")

        name = await CLIENT.wait_for("message", check=lambda message: message.author == msg.author)
        name = name.content
        name = str(name)

        await msg.channel.send("Now tell me the URL: ")

        url = await CLIENT.wait_for("message", check=lambda message: message.author == msg.author)
        url = url.content
        url = str(url)

        await add(name, url)
        await msg.channel.send(f"All right! {name} will be added.")

    # Remove entry from FeedItToMe
    if msg.content == "!remove":
        await msg.channel.send("Tell me the name: ")

        name = await CLIENT.wait_for("message", check=lambda message: message.author == msg.author)
        name = name.content
        name = str(name)

        if await remove(name):
            await msg.channel.send(f"All right! {name} will be removed.")
        else:
            await msg.channel.send(f"Sorry, but I couldn't find {name} on your feed.")

    # Delete x messages from the channel. Ex: !clear 5
    if msg.content.startswith("!clear"):
        msg_limit = int(msg.content[7:])
        print(f"Clearing chat... {msg_limit}")
        await msg.channel.purge(limit=msg_limit)

    # Check last updated entry for specified feed. Ex: !check PewDiePie
    if msg.content.startswith("!check "):
        name = msg.content[7:]
        if not await check(name, msg.channel):
            await msg.channel.send(f"Sorry, but I couldn't find {name} on your feed.")


async def add(name, url):
    FEEDS.append(Feed(name, url, "new"))


async def remove(name):
    for f in FEEDS:
        if f.name == name:
            FEEDS.remove(f)
            return True

    return False


async def check(name, channel):
    for f in FEEDS:
        if f.name == name:
            msg = f"Last updated entry for {f.name}:\n{f.link}"
            
            await channel.send(msg)
            return True

    return False        


async def notify(feed):
    msg = f"New **{feed.name}**!\nTitle: **{feed.title}**\nUpdated on: {feed.last_modified}\nLink: {feed.link}"
    channel = CLIENT.get_channel(CHANNEL_ID)

    await channel.send(msg)


async def feed():
    await CLIENT.wait_until_ready()

    while True:
        for f in FEEDS:
            d = feedparser.parse(f.url)

            if f.link != d.entries[0].link:
                f.last_modified = d.entries[0].updated
                f.title = d.entries[0].title
                f.link = d.entries[0].link

                print(f.name + "\n" + f.title)

                await notify(f)
            else:
                print(f"{f.name}... Check.")

        print(f"All checked! Next check in {WAIT_TIME / 60} minutes.")
        await asyncio.sleep(WAIT_TIME)


def save():
    with open(FEED_FILE_PATH, "w") as file:
        for f in FEEDS:
            file.write(f"{f.name};{f.url};{f.link}\n")

    print("All saved!")


async def start():
    with open(FEED_FILE_PATH) as f:
        for line in f:
            feed = line.split(";")
            FEEDS.append(Feed(feed[0], feed[1], feed[2].rstrip()))


@CLIENT.event
async def on_ready():
    print('Logged in as: ')
    print(CLIENT.user.name)
    print(CLIENT.user.id)
    print('------')
    print(CLIENT.users)


try:
    CLIENT.loop.create_task(start())
    CLIENT.loop.create_task(feed())
    CLIENT.run(TOKEN)
finally:
    save()
