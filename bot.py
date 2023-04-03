import discord
from discord.ext import commands
from discord import app_commands
import csv
import random
import asyncio
import sqlite3
import aiosqlite

from quest_tree import SituationNode, QuestTree
from user_interaction import Dialogue, DialogueGenerator
from constants import Biome, Context
from data_storage import DataStorage
from test_tree import p
from deserializer import TreeDeserializer


intents = discord.Intents().default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', description="Cat game!!!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    # slash commands
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(e)
    # database
    bot.db = await aiosqlite.connect("bot.db")
    async with bot.db.cursor() as cursor:
        await cursor.execute('CREATE TABLE IF NOT EXISTS inventory (id INTEGER, inventory TEXT)')
    await bot.db.commit()
    print("Database ready!")
    print('------')

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
            
# loading pre-generated tree
deserializer = TreeDeserializer(p)
arid_large = deserializer.deserialize_tree('data/tree/arid-large.csv')
global curr_dialogues
curr_dialogues = arid_large.current_node.dialogue
global next_route_options
next_route_options = arid_large.paths
    
# Views (buttons)
# class EnterView(discord.ui.View):
#     def __init__(self):
#         super().__init__()
#     @discord.ui.button(label="Next", style=discord.ButtonStyle.blurple)
#     async def investigate(self, interaction: discord.Interaction, button: discord.ui.Button):
#         context = Context.ENTER
#         embed=discord.Embed(title='Next', color=discord.Color.blue())
#         await interaction.response.send_message(curr_dialogues[context], view=InvestigateView())
#         self.stop()
        
class InvestigateView(discord.ui.View):
    def __init__(self):
        super().__init__()
    @discord.ui.button(label="Next", style=discord.ButtonStyle.blurple)
    async def investigate(self, interaction: discord.Interaction, button: discord.ui.Button):
        context = Context.INVESTIGATE
        embed = discord.Embed(description=curr_dialogues[context], color=discord.Color.blue())
        await interaction.response.send_message(embed=embed, view=PreviewView())
        self.stop()
    
class PreviewView(discord.ui.View):
    def __init__(self):
        super().__init__()
    @discord.ui.button(label="Next", style=discord.ButtonStyle.blurple)
    async def preview(self, interaction: discord.Interaction, button: discord.ui.Button):
        context = Context.PREVIEW
        embed = discord.Embed(description=curr_dialogues[context], color=discord.Color.blue())
        await interaction.response.send_message(embed=embed, view=ExitView())
        self.stop()
        
class ExitView(discord.ui.View):
    def __init__(self):
        super().__init__()
    @discord.ui.button(label="Next", style=discord.ButtonStyle.blurple)
    async def exit(self, interaction: discord.Interaction, button: discord.ui.Button):
        context = Context.EXIT
        embed = discord.Embed(description=curr_dialogues[context], color=discord.Color.blue())
        await interaction.response.send_message(embed=embed, view=NextPathsView())
        self.stop()
        # TODO: exit dialogue is not kept in chat and is overridden by nextpathview previews of next nodes FIX
        
        
class NextPathsView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.route_keys = [key for key in next_route_options]
        self.curr_index = 0
        
    @discord.ui.button(label="Back", style=discord.ButtonStyle.blurple)
    async def Route1(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.curr_index = (self.curr_index - 1) % len(self.route_keys)
        curr_tree = next_route_options[self.route_keys[self.curr_index]]
        curr_dialogues = curr_tree.current_node.dialogue
        context = Context.ENTER
        embed = discord.Embed(title="Choose a Path!", description=curr_dialogues[context], color=discord.Color.blue())
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="Select", style=discord.ButtonStyle.green)
    async def Route2(self, interaction: discord.Interaction, button: discord.ui.Button):
        global curr_dialogues
        global next_route_options
        curr_tree = next_route_options[self.route_keys[self.curr_index]]
        curr_dialogues = curr_tree.current_node.dialogue
        next_route_options = curr_tree.paths
        context = Context.ENTER 
        embed = discord.Embed(description=curr_dialogues[context], color=discord.Color.blue())
        await interaction.response.send_message(embed=embed, view=InvestigateView())
        self.stop()
        
    @discord.ui.button(label="Next", style=discord.ButtonStyle.blurple)
    async def Route3(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.curr_index = (self.curr_index + 1) % len(self.route_keys)
        curr_tree = next_route_options[self.route_keys[self.curr_index]]
        curr_dialogues = curr_tree.current_node.dialogue
        context = Context.ENTER
        embed = discord.Embed(title="Choose a Path!", description=curr_dialogues[context], color=discord.Color.blue())
        await interaction.response.edit_message(embed=embed, view=self)
        
        
@bot.tree.command(name='quest-start')
async def quest_start(interaction: discord.Interaction):
    while True:
        dialogues = arid_large.current_node.dialogue
        context = Context.ENTER
        curr_view = InvestigateView()
        embed = discord.Embed(description=curr_dialogues[context], color=discord.Color.blue())
        await interaction.response.send_message(embed=embed, view=curr_view)
        await curr_view.wait()
    
    returned_cat_placeholder = 'Tabby'
    await update_inventory(interaction, returned_cat_placeholder)

async def update_inventory(interaction: discord.Interaction, cat: str):
    async with bot.db.cursor() as cursor:
        await cursor.execute('INSERT INTO inventory VALUES(?, ?)', (interaction.user.id, cat))
    await bot.db.commit()
    return

async def view_inventory(interaction: discord.Interaction):
    async with bot.db.cursor() as cursor:
        await cursor.execute('SELECT cats FROM inventory WHERE id = ?', (interaction.user.id,))
        data = await cursor.fetchone()
        print(data)
        if data is None:
            return None
        else:
            cat = data[0]
            return cat

# async def update_inventory(interaction: discord.Interaction):
#     db = await aiosqlite.connect(r"C:\Users\Janet\cats-cradle\bot.db")
#     async with db.cursor() as cursor:
#         await cursor.execute('SELECT id FROM inventory WHERE cats = ?', (interaction.user.id,))
#         data = await cursor.fetchone()
#         if data is None:
#             await create_inventory(interaction)
#         await cursor.execute('UPDATE inventory SET cats = ? WHERE id = ?', (data[0] + '1', interaction.user.id))
#     await db.commit()

@bot.tree.command(name='cats')
async def cats(interaction: discord.Interaction):
    cat = await view_inventory(interaction)
    if cat is None:
        embed = discord.Embed(title='You have no cats yet! Use /quest-start to being adopting.')
    else:
        embed = discord.Embed(title=interaction.user, description=cat, color=discord.Color.random())
    await interaction.response.send_message(embed=embed)


class ChoiceButtons(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        
    @discord.ui.button(label="test 1", style=discord.ButtonStyle.green)
    async def test1(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed=discord.Embed(title='test 1', color=discord.Color.random())
        await interaction.response.edit_message(embed=embed)
    
    @discord.ui.button(label="test 2", style=discord.ButtonStyle.red)
    async def test2(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed=discord.Embed(title='test 2', color=discord.Color.random())
        await interaction.response.edit_message(embed=embed)

# Old Quest Start
# @bot.command()
# async def quest_start(ctx):
#     """Begins a quest for the user.
#     """
#     biome = random.choice(biomes)
    
#     # TODO no trees right now, just nodes
#     quest_start_dialogues = dialogues['quest_start']
#     situation_node = SituationNode(reward=None, biome=biome, dialogue={Context.ENTER: Dialogue
#                                                                        (title="Start", message=random.choice(quest_start_dialogues), image_path=None)}, id='1')
#     # quest_start_tree = QuestTree(situation_node)
#     quest_start_embed = situation_node.return_dialogue()
    
#     investigate_dialogues = dialogues['investigate']
#     situation_node = SituationNode(reward=None, biome=biome, dialogue={Context.ENTER: Dialogue
#                                                                        (title="Investigate", message=random.choice(investigate_dialogues), image_path=None)}, id='2')
#     # investigate_tree = QuestTree(situation_node)
#     # quest_start_tree.add_path(investigate_tree)
#     investigate_embed = situation_node.return_dialogue()

#     if biome == Biome.TEMPERATE:
#         previews_dialogues = dialogues['temperate_previews']
#     elif biome == Biome.FRIGID:
#         previews_dialogues = dialogues['frigid_previews']
#     elif biome == Biome.TROPICAL:
#         previews_dialogues = dialogues['tropical_previews']
#     elif biome == Biome.ARID:
#         previews_dialogues = dialogues['arid_previews']
#     elif biome == Biome.URBAN:
#         previews_dialogues = dialogues['urban_previews']
#     situation_node = SituationNode(None, biome, {Context.ENTER: Dialogue(title="Preview", message=random.choice(previews_dialogues), image_path=None)}, id="4")
#     preview_embed = situation_node.return_dialogue()
    
#     if biome == Biome.TEMPERATE:
#         entry_dialogues = dialogues['temperate_entry']
#     elif biome == Biome.FRIGID:
#         entry_dialogues = dialogues['frigid_entry']
#     elif biome == Biome.TROPICAL:
#         entry_dialogues = dialogues['tropical_entry']
#     elif biome == Biome.ARID:
#         entry_dialogues = dialogues['arid_entry']
#     elif biome == Biome.URBAN:
#         entry_dialogues = dialogues['urban_entry']
#     situation_node = SituationNode(None, biome, {Context.ENTER: Dialogue(title="Entry", message=random.choice(entry_dialogues), image_path=None)}, id='3')
#     entry_embed = situation_node.return_dialogue()

#     if biome == Biome.TEMPERATE:
#         leave_dialogues = dialogues['temperate_entry']
#     elif biome == Biome.FRIGID:
#         leave_dialogues = dialogues['frigid_entry']
#     elif biome == Biome.TROPICAL:
#         leave_dialogues = dialogues['tropical_entry']
#     elif biome == Biome.ARID:
#         leave_dialogues = dialogues['arid_entry']
#     elif biome == Biome.URBAN:
#         leave_dialogues = dialogues['urban_entry']
#     situation_node = SituationNode(None, biome, {Context.ENTER: Dialogue(title="Leave", message=random.choice(leave_dialogues), image_path=None)} , '3')
#     leave_embed = situation_node.return_dialogue()
    
#     # TODO change so rewards fit certain biome
#     # if biome == Biome.TEMPERATE:
#     #     possible_rewards = dialogues['temperate_entry']
#     # elif biome == Biome.FRIGID:
#     #     possible_rewards = dialogues['frigid_entry']
#     # elif biome == Biome.TROPICAL:
#     #     possible_rewards = dialogues['tropical_entry']
#     # elif biome == Biome.ARID:
#     #     possible_rewards = dialogues['arid_entry']
#     # elif biome == Biome.URBAN:
#     #     possible_rewards = dialogues['urban_entry']
#     possible_rewards = dialogues['possible_reward_cat'] + dialogues['possible_reward_item']
#     situation_node = SituationNode(None, biome, {Context.ENTER: Dialogue(title="Reward", message=random.choice(possible_rewards), image_path=None)}, '8')
#     reward_embed = situation_node.return_dialogue()

#     quest_end_dialogues = dialogues['quest_end']
#     situation_node = SituationNode(None, biome, {Context.ENTER: Dialogue(title="End", message=random.choice(quest_end_dialogues), image_path=None)}, '9')
#     quest_end_embed = situation_node.return_dialogue()
    
#     contents = [quest_start_embed, investigate_embed, preview_embed, entry_embed, leave_embed, reward_embed, quest_end_embed]
#     pages = 7
#     curr_page = 1
#     message = await ctx.send(embed=contents[0])
#     await message.add_reaction("◀️")
#     await message.add_reaction("▶️")

#     def check(reaction, user):
#             # This makes sure nobody except the command sender can interact with the "menu"
#             return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]

#     while True:
#         try:
#             reaction, user = await bot.wait_for("reaction_add", timeout=60, check=check)
#             # waiting for a reaction to be added - times out after 60 seconds
#             if str(reaction.emoji) == "▶️" and curr_page != pages:
#                 curr_page += 1
#                 await message.edit(embed=contents[curr_page])
#                 await message.remove_reaction(reaction, user)
#                 if curr_page == pages - 1:
#                     await message.clear_reactions()
#                     break

#             elif str(reaction.emoji) == "◀️" and curr_page > 1:
#                 curr_page -= 1
#                 await message.edit(embed=contents[curr_page])
#                 await message.remove_reaction(reaction, user)

#             else:
#                 # removes reactions if the user tries to go forward on the last page or backwards on the first page
#                 await message.remove_reaction(reaction, user)
#         except asyncio.TimeoutError:
#             await message.delete()
#             break
#             # ending the loop if user doesn't react after 60 seconds
    
    
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
    
    
bot.run('MTA4MzI1MDc2NzI1MjY5MzA1NQ.GCxC67.wsHqq-2DviqNqHWl7nxmzuh3OQDTbPOCjR7fxg')
