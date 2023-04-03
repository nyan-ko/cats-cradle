from __future__ import annotations
from typing import Optional

from discord import Color, Embed, Member, Interaction, ButtonStyle
from discord.app_commands import command
from discord.ui import View, button, Button
from discord.ext.commands import Bot, Cog, Context

from user import User as GameUser

from quest_tree import QuestTree
from constants import Context
import bot


class Quest(Cog):
    """
    """ 

    bot: bot.CatsCradle
    tree: QuestTree

    def __init__(self, bot: bot.CatsCradle) -> None:
        super().__init__()

        self.bot = bot

        self.tree = bot.get_deserializer().get_random_tree([
            "data/tree/tropical-small.csv" # TODO MORE
        ])

    @command(name="quest-start")
    async def quest_start(self, interaction: Interaction) -> None:
        """
        """

        if self.bot.get_user().started_quest():
            embed = Embed(title="Quest already started!",
                          description="You already have an ongoing quest. Finish it first! Or quit with /quest-leave.",
                          color=Color.blurple())
            await interaction.response.send_message(embed=embed, view=View())
        else:
            self.bot.get_user().start_quest(self.tree)

            embed = Embed(title="Quest started!",
                          description="Off you go on an exciting new quest. What wonders await you?",
                          color=Color.blurple())
            await interaction.response.send_message(embed=embed, view=StartView(self.bot))
        
    @command(name='cats')
    async def cats(self, interaction: Interaction) -> None:
        cats = await self._view_inventory(interaction)
        if cats is None:
            embed = Embed(title='You have no cats yet! Use /quest-start to begin adopting.')
        else:
            cats_dict = self.bot.get_deserializer().reward.emotes
            description = ''
            cat_count = {}
            for item in cats:
                for cat in item:
                    if cat not in cat_count:
                        cat_count[cat] = 1
                    else:
                        cat_count[cat] += 1
            for cat in cat_count:
                if cat in cats_dict:
                    description += f'{cats_dict[cat]} {cat} Cat ⨯ {cat_count[cat]}\n'
            embed = Embed(title=f'{interaction.user}\'s Cats!', description=description, color=Color.random())
        await interaction.response.send_message(embed=embed)

    async def _view_inventory(self, interaction: Interaction):
        async with self.bot.get_db().cursor() as cursor:
            await cursor.execute('SELECT cats FROM inventory WHERE id = ?', (interaction.user.id,))
            data = await cursor.fetchall()

        return data

class StartView(View):
    """
    """

    _bot: bot.CatsCradle

    def __init__(self, bot: bot.CatsCradle):
        """
        """

        super().__init__()

        self._bot = bot

    @button(label="Next", style=ButtonStyle.blurple)
    async def start(self, interaction: Interaction, button: Button):
        embed = self._bot.get_user().get_position().get_dialogue(Context.ENTER).embeddify(Color.blurple())
        await interaction.response.send_message(embed=embed, view=EntryView(self._bot))
        self.stop()

class EntryView(View):
    """
    """

    _bot: bot.CatsCradle

    def __init__(self, bot: bot.CatsCradle):
        """
        """

        super().__init__()

        self._bot = bot

    @button(label="Next", style=ButtonStyle.blurple)
    async def enter(self, interaction: Interaction, button: Button):
        embed = self._bot.get_user().get_position().get_dialogue(Context.INVESTIGATE).embeddify(Color.blurple())
        await interaction.response.send_message(embed=embed, view=InvestigateView(self._bot))
        self.stop()

class InvestigateView(View):
    """
    """

    _bot: bot.CatsCradle

    def __init__(self, bot: bot.CatsCradle):
        """
        """

        super().__init__()

        self._bot = bot

    @button(label="Next", style=ButtonStyle.blurple)
    async def investigate(self, interaction: Interaction, button: Button):
        position = self._bot.get_user().get_position()
        reward = position.current_node.reward

        if reward == "":
            embed = Embed(title="Nothing found...",
                          description="You didn't find anything here. Maybe next time.",
                          color=Color.blue())
        else:
            await self._bot.update_inventory(interaction.user.id, reward)

            embed = Embed(title="Cat acquired!",
                description=f"During your adventures, you picked up a {position.current_node.reward} cat!",
                color=Color.gold())

        await interaction.response.send_message(embed=embed, view=RewardView(self._bot))
        self.stop()

class RewardView(View):
    """
    """

    _bot: bot.CatsCradle

    def __init__(self, bot: bot.CatsCradle):
        """
        """

        super().__init__()

        self._bot = bot

    @button(label="Next", style=ButtonStyle.blurple)
    async def claim(self, interaction: Interaction, button: Button):
        position = self._bot.get_user().get_position()
        embed = position.get_dialogue(Context.EXIT).embeddify(Color.dark_blue())
        await interaction.response.send_message(embed=embed, view=ExitView(self._bot))
        self.stop()
        
class ExitView(View):
    """
    """

    _bot: bot.CatsCradle

    def __init__(self, bot: bot.CatsCradle):
        """
        """

        super().__init__()

        self._bot = bot

    @button(label="Next", style=ButtonStyle.blurple)
    async def exit(self, interaction: Interaction, button: Button):
        position = self._bot.get_user().get_position()
        if len(position.paths) == 0:
            new_biome = self._bot.get_biome_gen().get_next_biome()
            self._bot.deserializer.deserialize_tree

        embed = Embed(title="Choose a New Path!", color=Color.blue())
        await interaction.response.send_message(embed=embed, view=NextPathsView(self._bot))
        self.stop()

        
class NextPathsView(View):
    """
    """

    _curr_index: int
    _bot: bot.CatsCradle
    _ids: list[str]

    def __init__(self, bot: bot.CatsCradle):
        """
        """

        super().__init__()

        self._curr_index = 0
        self._bot = bot

        user = self._bot.get_user()
        self._ids = list(user.get_choices().keys())
            
    @button(label="Back", style=ButtonStyle.blurple)
    async def back(self, interaction: Interaction, button: Button):
        user = self._bot.get_user()
        paths = user.get_choices()
        
        self._curr_index = (self._curr_index - 1) % len(paths)

        curr_tree = paths[self._ids[self._curr_index]]
        embed = curr_tree.get_dialogue(Context.PREVIEW).embeddify(Color.blurple())
        embed.title = f"Choose a New Path! {self._curr_index + 1}/{len(paths)}"
        await interaction.response.edit_message(embed=embed, view=self)
    
    @button(label="Select", style=ButtonStyle.green)
    async def select(self, interaction: Interaction, button: Button):
        user = self._bot.get_user()
        
        choice = self._ids[self._curr_index]
        new_tree = user.make_choice(choice)
        dialogue = new_tree.get_dialogue(Context.ENTER)
        embed = dialogue.embeddify(Color.blurple())
        await interaction.response.send_message(embed=embed, view=EntryView(self._bot))
        self.stop()
        
    @button(label="Next", style=ButtonStyle.blurple)
    async def next(self, interaction: Interaction, button: Button):
        user = self._bot.get_user()
        paths = user.get_choices()
        
        self._curr_index = (self._curr_index + 1) % len(paths)

        curr_tree = paths[self._ids[self._curr_index]]
        embed = curr_tree.get_dialogue(Context.PREVIEW).embeddify(Color.blurple())
        embed.title = f"Choose a New Path! {self._curr_index + 1}/{len(paths)}"
        await interaction.response.edit_message(embed=embed, view=self)