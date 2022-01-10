import discord
from discord.ext import tasks
from discord.commands import slash_command, Option
from discord.utils import get
import random

# For Reddit
import asyncpraw
from datetime import datetime # Also used in bot's status
from pytz import timezone

bot = discord.Bot(intents=discord.Intents.all()) 
reddit = asyncpraw.Reddit(client_id = "REDACTED", client_secret = "REDACTED", user_agent = "REDACTED") # swuLzg6%QE1KQ@Rp*4Nd
SERVER_ID = 0
SERVERS = [0, 0] # Redacted
BOT_AUTHOR = 0
ADMINISTRATOR_IDS_ACTUAL = ["REDACTED", "REDACTED", "REDACTED"]
ADMINISTRATOR_IDS = ["REDACTED", "REDACTED", "REDACTED", "REDACTED", "REDACTED", "REDACTED", "REDACTED", "REDACTED", "REDACTED", "REDACTED", "REDACTED"] # For testing (REMOVE)

@bot.event
async def on_ready():
    print(f"{bot.user} is online")
    cycleStatuses.start()

statusArrays = ["Hello!", "The bot wishes you a good day!", "Hope you have a good day!", "Hello there!"]
@tasks.loop(seconds=15)
async def cycleStatuses():
    timeObj = datetime.now(timezone("US/Eastern"))
    x = str(timeObj.strftime('%I %M'))
    if (x[-2:] == "37" or x[-2:] == "47"):
        timeZ = "some place in the world!" # Default
        if(x[:2].rstrip() == "7"):
            timeZ = "EST"
        elif (x[:2].rstrip() == "8"):
            timeZ = "CST"
        elif (x[:2].rstrip() == "9"):
            timeZ = "MST"
        elif (x[:2].rstrip() == "10"):
            timeZ = "PST"
        elif (x[:2].rstrip() == "12"):
            timeZ = "Hawaii"
        await bot.change_presence(status=discord.Status.idle, activity=discord.Game(f"Happy 7:{x[-2:]}, {timeZ}!!!"))
    else:
        await bot.change_presence(status=discord.Status.idle, activity=discord.Game(random.choice(statusArrays)))

async def getNthWord(test_str, limit):
    count = 0
    res = ""
    for ele in test_str:
        if ele == ' ':
            count = count + 1
            if count == limit:
                break
            elif count == 1:
                res = ""
            else:
                res = res + ele
        elif ele == ".":
            break
        else:
            res = res + ele
   
    return res
# Above function is for the event below 
@bot.event
async def on_message(message):
    if message.content.lower().startswith("i'm") or message.content.lower().startswith("im"):
        msg = await getNthWord(message.content, 10)
        await message.channel.send(f"Hello {msg}, I'm {bot.user.name}.")

@bot.slash_command(guild_ids=[661404316392882203])
async def hello(ctx):
    await ctx.respond("Hello!")

# Command to convert message to create typos for fun
@bot.slash_command(name = 'jumble', description = 'Convert your message into Aethish! Note: WIP.', guild_ids=SERVERS)
async def jumble(ctx, arg, level: Option(str, "Choose a level", choices=["low", "medium", "high", "insnae"], required=False, default="medium")):
    message = arg

    # convert the message to a list of characters
    message = list(message)

    typo_prob = 0
    #typo_prob = 0.1 if ("low" in level) else typo_prob = 0.2 if "medium" in level else typo_prob = 0.3 if "high" in level else typo_prob = 0.5 # percent (out of 1.0) of characters to become typos
    if level == "low":
        typo_prob = 0.1
    elif level == "medium":
        typo_prob = 0.2
    elif level == "high":
        typo_prob = 0.3
    else:
        typo_prob = 0.5

    # the number of characters that will be typos
    n_chars_to_flip = round(len(message) * typo_prob)
    # is a letter capitalized?
    capitalization = [False] * len(message)
    # make all characters lowercase & record uppercase
    for i in range(len(message)):
        capitalization[i] = message[i].isupper()
        message[i] = message[i].lower()

    # list of characters that will be flipped
    pos_to_flip = []
    for i in range(n_chars_to_flip):
        pos_to_flip.append(random.randint(0, len(message) - 1))

    # dictionary... for each letter list of letters
    # nearby on the keyboard
    nearbykeys = {
        'a': ['q','w','s','x','z', 'A'],
        'b': ['v','g','h'],
        'c': ['x','d','f','v', ' '],
        'd': ['s','e','r','f','c','x'],
        'e': ['w','s','d','r'],
        'f': ['d','r','t','g','v','c', 'e'],
        'g': ['f','t','y','h','b','v','r'],
        'h': ['g','y','u','j','n','b'],
        'i': ['u','j','k','o','l'],
        'j': ['h','u','i','k','n','m'],
        'k': ['j','i','o','l','m'],
        'l': ['k','o','p','i'],
        'm': ['n','j','k','l'],
        'n': ['b','h','j','m'],
        'o': ['i','k','l','p'],
        'p': ['o','l'],
        'q': ['w','a','s'],
        'r': ['e','d','f','t','g'],
        's': ['w','e','d','x','z','a'],
        't': ['r','f','g','y'],
        'u': ['y','h','j','i'],
        'v': ['c','f','g','v','b'],
        'w': ['q','a','s','e'],
        'x': ['z','s','d','c'],
        'y': ['t','g','h','u'],
        'z': ['a','s','x', 'Z'],
        ' ': ['c','v','b','n','m'],
        ',': ['<', '.', '>', ':', ';']
    }

    # insert typos
    for pos in pos_to_flip:
        # try-except in case of special characters
        try:
            typo_arrays = nearbykeys[message[pos]]
            message[pos] = random.choice(typo_arrays)
        except:
            break

    # reinsert capitalization
    for i in range(len(message)):
        if (capitalization[i]):
            message[i] = message[i].upper()

    # recombine the message into a string
    message = ''.join(message)

    # show the message in the console
    await ctx.respond(message)
    await logger(ctx.author, "aethish",f"`/aethish {arg} {level}`")

# Command to flag messages as false or misleading.
@bot.slash_command(name='misleading', description = 'ADMINS ONLY: Flag sus messages as false/misleading!', guild_ids=SERVERS)
async def flag(ctx, message_id):
    if (str(ctx.author.id) in ADMINISTRATOR_IDS):
        channel = bot.get_channel(ctx.channel.id)
        message = await channel.fetch_message(message_id)
        embed = discord.Embed(
        title = "ⓘ 𝗢𝗳𝗳𝗶𝗰𝗶𝗮𝗹 𝘀𝗼𝘂𝗿𝗰𝗲𝘀 𝘀𝘁𝗮𝘁𝗲𝗱 𝘁𝗵𝗮𝘁 𝘁𝗵𝗶𝘀 𝗶𝘀 𝗳𝗮𝗹𝘀𝗲 𝗮𝗻𝗱 𝗺𝗶𝘀𝗹𝗲𝗮𝗱𝗶𝗻𝗴",
        colour = discord.Colour(value=0xffffff)
        )
        await message.reply(embed=embed, mention_author=False)
        await ctx.respond("Sent!", ephemeral=True)
    else:
        await ctx.respond("You don't have permissions to run that command!", ephemeral=True)

    await logger(ctx.author, "flag",f"`/flag {message_id}`")

@bot.slash_command(name='test', guild_ids=[661404316392882203])
async def test(ctx, userid):
    print(f'Attempt to get userid {userid}')
    Status = ctx.guild.get_member(int(userid))
    await ctx.respond("You are " +  str(Status.status))

@bot.slash_command(name='modlist', description = 'Display the moderation staff and their online status.', guild_ids=SERVERS)
async def modlist(ctx):
    modStaff = ["REDACTED"] # test server
    onlineMods = []
    idleMods = []
    dndMods = []
    offlineMods = []

    for ID in modStaff:
        Member = ctx.guild.get_member(int(ID))
        if Member is None:
            continue

        #print(ctx.guild.name)
        #print(ID + " is " + str(Member.status))
        onlineMods.append(int(ID)) if (str(Member.status) == "online") else idleMods.append(int(ID)) if (str(Member.status) == "idle") else dndMods.append(int(ID)) if (str(Member.status) == "dnd") else offlineMods.append(int(ID)) # If member is online

    message, message2, message3, message4 = "", "", "", ""
    for oModsID in onlineMods:
        message += f"🟢 <@!{oModsID}>\n" 
    for iModsID in idleMods:
        message2 += f"🟡 <@!{iModsID}>\n"
    for dModsID in dndMods:
        message3 += f"🔴 <@!{dModsID}>\n"
    for ofModsID in offlineMods:
        message4 += f"⚫ <@!{ofModsID}>\n"

    # If the fields are blank, we need to have add a value so it doesn't crash.
    if message == "":
        message = "No online mods."
    if message2 == "":
        message2 = "No idle mods."
    if message3 == "":
        message3 = "No DND mods."
    if message4 == "":
        message4 = "No offline mods."

    embed = discord.Embed(
    title = "Server Moderation Staff",
   #description = message,
    colour = discord.Colour.blue()
    )

    embed.add_field(name="Online", value=message, inline=True)
    embed.add_field(name="Idle", value=message2, inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline = False)
    embed.add_field(name="DND", value=message3, inline=True)
    embed.add_field(name="Offline", value=message4, inline=True)
 
    await ctx.respond(embed=embed)
    await logger(ctx.author, "modlist",f"`/modlist`")

@bot.slash_command(name='suggest', description = 'Make a suggestion for the server staff to review. Trolls will be blacklisted!', guild_ids=SERVERS)
async def suggest(ctx, suggestion):
    SUGGESTION_LOGS_CHANNEL_ID_TESTING = 929188389863956561
    SUGGESTION_LOGS_CHANNEL_ID = SUGGESTION_LOGS_CHANNEL_ID_TESTING # Change later

    SUGGESTIONS_CHANNEL_ID_TESTING = 929197181330669649
    SUGGESTIONS_CHANNEL_ID = SUGGESTIONS_CHANNEL_ID_TESTING # Change later

    embed = discord.Embed(
        title = f"New Suggestion",
        description = suggestion,
        colour = discord.Colour.blue()
    )

    embed.set_author(name=f"{ctx.author.display_name} ({ctx.author.name}#{ctx.author.discriminator})", icon_url=ctx.author.display_avatar.url)
    await ctx.respond(f"Sent suggestion to <#{bot.get_channel(SUGGESTIONS_CHANNEL_ID).id}>", ephemeral=True)
    await bot.get_channel(SUGGESTIONS_CHANNEL_ID).send(embed=embed)

    embed.set_footer(text="If this is an abuse of the feature, you may blacklist using [Coming soon...].")
 
    logMessage = await bot.get_channel(SUGGESTION_LOGS_CHANNEL_ID).send(embed=embed)
    await logMessage.add_reaction("✅")
    await logMessage.add_reaction("➖")
    await logMessage.add_reaction("❌")

    # await logger(ctx.author, "suggest",f"`/suggest {suggestion}`") Might not be needed if there's a suggestion logging channel

@bot.slash_command(name='banner', description = "Get a user's banner", guild_ids=SERVERS)
async def banner(ctx, *, member: discord.Member = None):
    if member is None:
        member = ctx.author

    member = await bot.fetch_user(member.id)
    if member.banner is None:
        #print(member.banner)
        await ctx.respond(f"**{member.display_name} ({member.name}#{member.discriminator}) does not have a banner!**")
    else:
        embed = discord.Embed(
            title = f"{member.name}#{member.discriminator}'s profile banner",
            colour = discord.Colour.blue()
        )
        embed.set_image(url=member.banner.url)
        await ctx.respond(embed=embed)
    
    await logger(ctx.author, "banner",f"`/banner {member.id} ({member.name}#{member.discriminator})`")

@bot.slash_command(name='serveravatar', description = "Get a user's server/guild avatar (pfp)", guild_ids=SERVERS)
async def serveravatar(ctx, *, member: discord.Member = None):
    if member is None:
        member = ctx.author

    member = await bot.fetch_user(member.id)
    embed = discord.Embed(
        title = f"{member.name}#{member.discriminator}'s server avatar",
        colour = discord.Colour.blue()
    )
    embed.set_image(url=member.display_avatar.url)
    await ctx.respond(embed=embed)
    
    await logger(ctx.author, "serveravatar",f"`/serveravatar {member.id} ({member.name}#{member.discriminator})`")

@bot.slash_command(name='help', description = "Get a list of commands for the bot.", guild_ids=SERVERS)
async def help(ctx):
    embed = discord.Embed(
        title = f"List of commands in {ctx.guild.name} server.",
        colour = discord.Colour.blue(),
        # Commands: aethish, banner, flag, modlist, serveravatar, suggest
        description = "`aethish`: Convert your message into Aethish! Note: WIP.\n`banner`: Get a user's banner\n`flag`: ADMINS ONLY: Flag sus messages as false/misleading!\n`modlist`: Display the moderation staff and their online status.\n`serveravatar`: Get a user's server/guild avatar (pfp)\n`suggest`: Make a suggestion for the server staff to review. Trolls will be blacklisted!"
    )
    await ctx.respond(embed=embed)
    await logger(ctx.author, "help",f"`/help`")

@bot.slash_command(name='hotposts', description = "Show a random hot post in the subreddit", guild_ids=SERVERS)
async def hotposts(ctx, level: Option(str, "Choose the limit (top 10, 50, etc.)", choices=["5", "10", "50", "100"], required=False, default=10)):
    subreddit = await reddit.subreddit("memes")
    all_subs = []

    hot = subreddit.hot(limit = int(level))
    async for submission in hot:
        all_subs.append(submission)
    
    random_sub = random.choice(all_subs)
    while random_sub.stickied: # We don't want a stickied post to be at the hot section
        random_sub = random.choice(all_subs)

    embed = discord.Embed(
        title=random_sub.title,
        description=f"_From {random_sub.author.name}_\n\n{random_sub.selftext}",
        colour = discord.Colour.blue(),
        url = f"https://www.reddit.com{random_sub.permalink}"
    )
    embed.set_image(url=random_sub.url)
    #embed.add_field(name=f"_Post from {random_sub.author}_", value=random_sub.selftext,inline=False)

    footer = datetime.utcfromtimestamp(random_sub.created_utc).strftime('%x\t%I:%M:%S %p')
    if random_sub.edited:
        footer += " (Edited) "
    embed.set_footer(text=f"{footer}\t\t👍{str(random_sub.score)} ({str(random_sub.upvote_ratio*100)}%) | 💬{str(random_sub.num_comments)}")
    
    await ctx.respond(embed=embed)
    await logger(ctx.author, "hotposts",f"`/hotposts {level}`")

@bot.slash_command(name='meme', description = "Show a random hot post in the subreddit", guild_ids=SERVERS)
async def meme(ctx, subreddit: Option(str, "Choose the subreddit", choices=["memes", "ComedyCemetery","brooklynninenine", "PandR", "DunderMifflin", "formuladank"], required=False, default="memes"), level: Option(str, "Choose the limit (top 10, 50, etc.)", choices=["5", "10", "50", "100"], required=False, default=10)):
    subreddit = await reddit.subreddit(subreddit)
    all_subs = []

    hot = subreddit.hot(limit = int(level))
    async for submission in hot:
        all_subs.append(submission)
    
    random_sub = random.choice(all_subs)
    while random_sub.stickied or random_sub.over_18: # We don't want a stickied or a NSFW post to be at the hot section
        random_sub = random.choice(all_subs)

    embed = discord.Embed(
        title=random_sub.title,
        description=f"From {random_sub.author.name}\n\n{random_sub.selftext}",
        colour = discord.Colour.blue(),
        url = f"https://www.reddit.com{random_sub.permalink}"
    )
    embed.set_image(url=random_sub.url)
    #embed.add_field(name=f"_Post from {random_sub.author}_", value=random_sub.selftext,inline=False)

    footer = datetime.utcfromtimestamp(random_sub.created_utc).strftime('%x\t%I:%M:%S %p UTC')
    if random_sub.edited:
        footer += " (Edited) "
    embed.set_footer(text=f"{footer}\t\t👍{str(random_sub.score)} ({str(random_sub.upvote_ratio*100)}%) | 💬{str(random_sub.num_comments)}")
    
    await ctx.respond(embed=embed)
    await logger(ctx.author, "hotposts",f"`/hotposts {level}`")

@bot.slash_command(name='memberslist', description = "To print an array of members", guild_ids=SERVERS)
async def memberslist(ctx):
    if(ctx.author.id == BOT_AUTHOR):
        arrayStr = "["
        namesStr = "["
        async for member in ctx.guild.fetch_members(limit=150):
            arrayStr += f'"{str(member.id)}", '
            namesStr += f"{member.name}, "
        arrayStr = arrayStr[:-2] + "]" # Remove last 2 useless characters
        namesStr = namesStr[:-2] + "]"
        await ctx.respond(f"{arrayStr}\n{namesStr}")
    else:
        await ctx.respond("You don't have permissions! This is a testing command.", ephemeral=True)

async def logger(user, command, full):
    BOT_COMMANDS_LOG_CHANNEL = 929282356353826876

    embed = discord.Embed(
        title=f"{command} ran by {user.display_name} ({user.name}#{user.discriminator})",
        description=full,
        colour = discord.Colour.blue()
    )
    await bot.get_channel(BOT_COMMANDS_LOG_CHANNEL).send(embed=embed)

bot.run('REDACTED')