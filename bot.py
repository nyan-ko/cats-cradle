import discord
from discord.ext import commands
import csv

from quest_tree import SituationNode, QuestTree
from user_interaction import Dialogue
from constants import Biome, Context


intents = discord.Intents().default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', description="Cat game!!!", intents=intents)

# maps biome to [Situation, Responses, Rewards] from quest_interactions.csv
situation = []
with open('quest_interactions.csv') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)  # skip the header row
    for row in reader:
        situation += row

# user commands
@bot.command()
async def quest_start(ctx):
    """Begins a quest for the user.
    """
    # TODO: change hardcoded SituationNode
    situation_node = SituationNode(situation[-1], situation[0], {Context.ENTER: Dialogue(title="Title", message="description", image_path=None)})
    quest = QuestTree(situation_node)
    embed = quest.quest_start()
    await ctx.send(embed=embed)

# @bot.command()
# async def help(ctx):
#     """Returns the interface for user commands.
#     """
#     embed = discord.Embed(
#             colour=discord.Colour.dark_gold(),
#             description="Meow: Sends a meow",
#             title=self.title
#         )
#     embed.set_image(url="https://upload.wikimedia.org/wikipedia/commons/4/4d/Cat_November_2010-1a.jpg")
#     await ctx.send(embed=embed)

@bot.command()
async def meow(ctx):
    await ctx.send("Meow!")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    
    
bot.run('bot token')
