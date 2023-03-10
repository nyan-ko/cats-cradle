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
