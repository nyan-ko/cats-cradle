import discord
from discord.ext import commands
import csv

from quest_tree import SituationNode, QuestTree


intents = discord.Intents().default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', description="Cat game!!!", intents=intents)

# maps biome to [Situation, Responses, Rewards] from quest_interactions.csv
situation = {}
with open('quest_interactions.csv') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)  # skip the header row
    for row in reader:
        situation[row[0]] = row[1:]  

# user commands
@bot.command()
async def quest_start(ctx):
    await ctx.send("Message sent at the start of a quest.")

@bot.command()
async def help(ctx):
    """Returns the interface for user commands.
    """
    embed = discord.Embed(
            colour=discord.Colour.dark_gold(),
            description="Meow: Sends a meow",
            title=self.title
        )
        embed.set_image(url="https://upload.wikimedia.org/wikipedia/commons/4/4d/Cat_November_2010-1a.jpg")
    await ctx.send(embed=embed)

@bot.command()
async def meow(ctx):
    await ctx.send("Meow!")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def begin_quest():
    """Begins a quest for the user.
    """
    # pick a random situation from situation and create a SituationNode, situation = SituationNode()
    # quest = QuestTree(situation)
    # quest.begin_quest()
    
    
bot.run("<insert token here>")
