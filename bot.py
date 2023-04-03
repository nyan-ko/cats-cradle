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
        await cursor.execute('CREATE TABLE IF NOT EXISTS inventory (id INTEGER, cats TEXT)')
    await bot.db.commit()
    print("Database ready!")
    print('------')

# loading biomes dialogues, and cats
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
        data = await cursor.fetchall()
        print(data)
        if data is None:
            return None
        else:
            return data

@bot.tree.command(name='cats')
async def cats(interaction: discord.Interaction):
    cats = await view_inventory(interaction)
    if cats is None:
        embed = discord.Embed(title='You have no cats yet! Use /quest-start to begin adopting.')
    else:
        description = ''
        cat_count = {}
        for item in cats:
            for cat in item:
                if cat not in cat_count:
                    cat_count[cat] = 1
                else:
                    cat_count[cat] += 1
        for cat in cat_count:
            description += f'{cats_dict[cat]} {cat} Cat ⨯ {cat_count[cat]}\n'
        embed = discord.Embed(title=f'{interaction.user}\'s Cats!', description=description, color=discord.Color.random())
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
        embed=discord.Embed(title='Tree', color=discord.Color.random())
        await interaction.response.edit_message(embed=embed)
    

@bot.command()
async def meow(ctx):
    await ctx.send("Meow!")
    
    
bot.run('NzE5MDA4NDM3Mzg3Nzg4MzQ5.GaPlQm.i2oO2G46gefbbJNTQMWvYUtNWouDZ6PBcuHVec')
