import discord
from discord.ext import commands
from discord import app_commands
import csv
import random
import asyncio
import sqlite3
import aiosqlite

from quest_tree import SituationNode, QuestTree
from user_interaction import Dialogue
from constants import Biome, Context


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
    bot.db = await aiosqlite.connect(r"bot.db")
    async with bot.db.cursor() as cursor:
        await cursor.execute('CREATE TABLE IF NOT EXISTS inventory (id INTEGER, cats TEXT)')
    await bot.db.commit()
    print("Database ready!")
    print('------')

# loading biomes dialogues, and cats
biomes = [Biome.TEMPERATE, Biome.FRIGID, Biome.TROPICAL, Biome.ARID, Biome.URBAN]
dialogues = {}
with open(r'dialogues.csv') as csv_file:
    reader = csv.reader(csv_file)
    headings = next(reader)  
    for heading in headings:
        dialogues[heading] = []
    for row in reader:
        for heading, value in zip(headings, row):
            dialogues[heading].append(value)
cats_dict = {}
with open(r'cats.csv') as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        cats_dict[r'{}'.format(row[0])] = r'{}'.format(row[1])
print(cats_dict)
emotes_dict = {}
with open(r'cats.csv') as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        emotes_dict[r'{}'.format(row[0])] = r'{}'.format(row[2])
print(emotes_dict)

@bot.tree.command(name='quest-start')
async def quest_start(interaction: discord.Interaction):
    view = QuestPannel()
    # TODO: Implement the body of this function as a loop
    # I will assume that this quest_start returns a random cat
    await interaction.response.send_message("response", view=view)
    returned_cat_placeholder = random.choice(list(cats_dict))
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
        embed = discord.Embed(title='You have no cats yet! Use /quest-start to being adopting.')
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
            description += f'{emotes_dict[cat]} {cat} Cat ⨯ {cat_count[cat]}\n'
        embed = discord.Embed(title=f'{interaction.user}\'s Cats!', description=description, color=discord.Color.random())
    await interaction.response.send_message(embed=embed)


# attempt at creating buttons 
class QuestPannel(discord.ui.View):
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
        embed.set_image(url='https://cdn.discordapp.com/attachments/1084300711115882536/1092231850736492664/IMG_0248.png')
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

@bot.command()
async def meow(ctx):
    await ctx.send("Meow!")
    
    
bot.run('MTA4MzI1MDc2NzI1MjY5MzA1NQ.GCxC67.wsHqq-2DviqNqHWl7nxmzuh3OQDTbPOCjR7fxg')
