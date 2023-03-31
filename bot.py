import discord
from discord.ext import commands
import csv
import random
import asyncio

from quest_tree import SituationNode, QuestTree
from user_interaction import Dialogue
from constants import Biome, Context
# from data_storage import DataStorage


intents = discord.Intents().default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', description="Cat game!!!", intents=intents)

# loading biomes and dialogues
biomes = [Biome.TEMPERATE, Biome.FRIGID, Biome.TROPICAL, Biome.ARID, Biome.URBAN]
dialogues = {}
with open('dialogues.csv') as csv_file:
    reader = csv.reader(csv_file)
    headings = next(reader)  
    for heading in headings:
        dialogues[heading] = []
    for row in reader:
        for heading, value in zip(headings, row):
            dialogues[heading].append(value)


# attempt at creating buttons 
class View(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.embed = None
        
    @discord.ui.button(label="Next", style=discord.ButtonStyle.green)
    async def next(self, button: discord.ui.Button, interaction: discord.Interaction):
        await button.response.edit_message(embed=self.embed)


@bot.command()
async def quest_start(ctx):
    """Begins a quest for the user.
    """
    view = View()
    biome = random.choice(biomes)
    
    # TODO no trees right now, just nodes
    quest_start_dialogues = dialogues['quest_start']
    situation_node = SituationNode(None, biome, {Context.ENTER: Dialogue(title="Start", message=random.choice(quest_start_dialogues), image_path=None)})
    # quest_start_tree = QuestTree(situation_node)
    quest_start_embed = situation_node.return_dialogue()
    
    investigate_dialogues = dialogues['investigate']
    situation_node = SituationNode(None, biome, {Context.ENTER: Dialogue(title="Investigate", message=random.choice(investigate_dialogues), image_path=None)})
    # investigate_tree = QuestTree(situation_node)
    # quest_start_tree.add_path(investigate_tree)
    investigate_embed = situation_node.return_dialogue()

    if biome == Biome.TEMPERATE:
        previews_dialogues = dialogues['temperate_previews']
    elif biome == Biome.FRIGID:
        previews_dialogues = dialogues['frigid_previews']
    elif biome == Biome.TROPICAL:
        previews_dialogues = dialogues['tropical_previews']
    elif biome == Biome.ARID:
        previews_dialogues = dialogues['arid_previews']
    elif biome == Biome.URBAN:
        previews_dialogues = dialogues['urban_previews']
    situation_node = SituationNode(None, biome, {Context.ENTER: Dialogue(title="Preview", message=random.choice(previews_dialogues), image_path=None)})
    preview_embed = situation_node.return_dialogue()
    
    if biome == Biome.TEMPERATE:
        entry_dialogues = dialogues['temperate_entry']
    elif biome == Biome.FRIGID:
        entry_dialogues = dialogues['frigid_entry']
    elif biome == Biome.TROPICAL:
        entry_dialogues = dialogues['tropical_entry']
    elif biome == Biome.ARID:
        entry_dialogues = dialogues['arid_entry']
    elif biome == Biome.URBAN:
        entry_dialogues = dialogues['urban_entry']
    situation_node = SituationNode(None, biome, {Context.ENTER: Dialogue(title="Entry", message=random.choice(entry_dialogues), image_path=None)})
    entry_embed = situation_node.return_dialogue()

    if biome == Biome.TEMPERATE:
        leave_dialogues = dialogues['temperate_entry']
    elif biome == Biome.FRIGID:
        leave_dialogues = dialogues['frigid_entry']
    elif biome == Biome.TROPICAL:
        leave_dialogues = dialogues['tropical_entry']
    elif biome == Biome.ARID:
        leave_dialogues = dialogues['arid_entry']
    elif biome == Biome.URBAN:
        leave_dialogues = dialogues['urban_entry']
    situation_node = SituationNode(None, biome, {Context.ENTER: Dialogue(title="Leave", message=random.choice(leave_dialogues), image_path=None)})
    leave_embed = situation_node.return_dialogue()
    
    # TODO change so rewards fit certain biome
    # if biome == Biome.TEMPERATE:
    #     possible_rewards = dialogues['temperate_entry']
    # elif biome == Biome.FRIGID:
    #     possible_rewards = dialogues['frigid_entry']
    # elif biome == Biome.TROPICAL:
    #     possible_rewards = dialogues['tropical_entry']
    # elif biome == Biome.ARID:
    #     possible_rewards = dialogues['arid_entry']
    # elif biome == Biome.URBAN:
    #     possible_rewards = dialogues['urban_entry']
    possible_rewards = dialogues['possible_reward_cat'] + dialogues['possible_reward_item']
    situation_node = SituationNode(None, biome, {Context.ENTER: Dialogue(title="Reward", message=random.choice(possible_rewards), image_path=None)})
    reward_embed = situation_node.return_dialogue()

    quest_end_dialogues = dialogues['quest_end']
    situation_node = SituationNode(None, biome, {Context.ENTER: Dialogue(title="End", message=random.choice(quest_end_dialogues), image_path=None)})
    quest_end_embed = situation_node.return_dialogue()
    
    contents = [quest_start_embed, investigate_embed, preview_embed, entry_embed, leave_embed, reward_embed, quest_end_embed]
    pages = 7
    curr_page = 1
    message = await ctx.send(embed=contents[0])
    await message.add_reaction("◀️")
    await message.add_reaction("▶️")

    def check(reaction, user):
            # This makes sure nobody except the command sender can interact with the "menu"
            return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=60, check=check)
            # waiting for a reaction to be added - times out after 60 seconds
            if str(reaction.emoji) == "▶️" and curr_page != pages:
                curr_page += 1
                await message.edit(embed=contents[curr_page])
                await message.remove_reaction(reaction, user)
                if curr_page == pages - 1:
                    await message.clear_reactions()
                    break

            elif str(reaction.emoji) == "◀️" and curr_page > 1:
                curr_page -= 1
                await message.edit(embed=contents[curr_page])
                await message.remove_reaction(reaction, user)

            else:
                # removes reactions if the user tries to go forward on the last page or backwards on the first page
                await message.remove_reaction(reaction, user)
        except asyncio.TimeoutError:
            await message.delete()
            break
            # ending the loop if user doesn't react after 60 seconds
    
    
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

# Tester functions for data_storage class. Remove these later.
@bot.command()
async def store_cat_tester(ctx, *, message):
    table = DataStorage(bot)
    user, guild = ctx.author.id, ctx.guild.id
    table.store_info(guild, user, message)
    await ctx.send("I have stored your message for you!")

@bot.command()
async def retrive_cats_tester(ctx):
    table = DataStorage(bot)
    user, guild = ctx.author.id, ctx.guild.id
    message = table.retrive_info(guild, user)
    await ctx.send(message)

@bot.command()
async def meow(ctx):
    await ctx.send("Meow!")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    
    
bot.run('MTA4MzI1MDc2NzI1MjY5MzA1NQ.GCxC67.wsHqq-2DviqNqHWl7nxmzuh3OQDTbPOCjR7fxg')
