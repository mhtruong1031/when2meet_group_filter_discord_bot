import discord, random

from bot_token import bot_token
from When2Meet import When2Meet

# W2M Set-up
names  = ["april", "hao", "julie", "kelsey", "kenny", "max", "minh", "mon", "monica", "nellie", "sophia", "tamnhu", "teresa", "trisha"]
groups = {"Everyone":      names,
          "Victory Song":  ["max", "teresa", "april", "nellie", "minh", "kelsey", "sophia"],
          "EZ":            ["teresa", "max", "minh", "kelsey", "monica", "sophia"],
          "Me Nescesita":  ["nellie", "april", "minh", "monica", "hao", "sophia"],
          "Goated":        ["april", "minh", "kenny", "monica"],
          "LALALALA":      ["julie", "max", "teresa"],
          "Fact Check":    ["april", "nellie", "minh", "tamnhu", "kelsey"],
          "Super":         ["julie", "teresa", "april", "tamnhu", "kelsey", "sophia"],
          "BILLIE EILISH": ["nellie", "minh", "kenny", "monica", "julie"],
          "Hard":          ["april"],
          "AI":            ["max", "april", "minh"],
          "GRL GVNG":      ["april", "nellie", "tamnhu", "trisha", "monica", "hao"], 
          "Finesse":       ["max", "tamnhu", "kenny", "monica", "sophia"],
          "Shirt":         ["trisha", "monica"],
          "You Got It":    ["april", "tamnhu", "minh", "monica", "teresa", "hao"],
          "I Do":          ["nellie", "trisha", "monica"],
          "Breathe":       ["minh", "tamnhu", "monica", "nellie"],
          "Smoke":         ["max", "teresa", "april", "minh", "tamnhu"],
          "Law":           ["kelsey", "nellie", "minh", "teresa", "monica", "sophia"]
          }

obj = When2Meet('resources/datasets/when2meet.csv', names, groups)

# Client Set-up
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('availability for '):
        for index, group_name in enumerate(groups):
            if message.content[17:] == group_name.lower():
                obj.save_tablemap(obj.filter_table_distribution(group_name), f'resources/{group_name}.png')

                embed = discord.Embed(title=f"Group Availability for {group_name}")
                file = discord.File(f'resources/{group_name}.png', filename="image.png")
                embed.set_image(url="attachment://image.png")
                await message.channel.send(file=file, embed=embed)
                break
    
    if message.content.startswith("roll for"):
        await message.channel.send(str(random.randint(1,20)))

client.run(bot_token)