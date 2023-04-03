"""CSC111 Winter 2023 Project: Cat's Cradle

This module contains classes and methods to represent the Discord side of the bot, such as embeds and buttons.

This file is copyright (c) 2023 by Edric Liu, Janet Fu, Nancy Hu, and Lily Meng.
"""
from __future__ import annotations

from quest_tree import QuestTree
from constants import Context
import bot
import random

from discord import Color, Embed, Interaction, ButtonStyle
from discord.ui import View, button, Button
from discord.ext.commands import Cog, Context

from discord.app_commands import command

import sys
sys.path.insert(1, r'cats-cradle')


class Quest(Cog):
    """A class representing the Quest object as a Cog. Stores the bot and the current QuestTree.
    
    Instance Attributes:
    - bot: Cats Cradle discord bot.
    - tree: the current QuestTree that is being used in gameplay.
    """
    bot: bot.CatsCradle
    tree: QuestTree

    def __init__(self, bot: bot.CatsCradle) -> None:
        """ Initializes the given bot with a random QuestTree from the premade trees.
        """
        super().__init__()

        self.bot = bot

        self.tree = bot.get_deserializer().get_random_tree([
            "data/tree/tropical-small.csv",
            "data/tree/arid-small.csv",
            "data/tree/frigid-small.csv",
            "data/tree/urban-small.csv",
            "data/tree/temperate-small.csv",
        ])

    @command(name="quest-start")
    async def quest_start(self, interaction: Interaction) -> None:
        """A user slash command. Type /quest-start in the discord chat to use this.
        Begins the quest.
        """
        if self.bot.get_user().started_quest():
            embed = Embed(title="Quest already started!",
                          description="You already have an ongoing quest. Finish it first!",
                          color=Color.blurple())
            await interaction.response.send_message(embed=embed, view=View())
        else:
            self.bot.get_user().set_position(self.tree)
            self.bot.biome_generator.update_traversal(self.tree.current_node.biome)

            embed = Embed(title="Quest started!",
                          description="Off you go on an exciting new quest. What wonders await you?",
                          color=Color.blurple())
            await interaction.response.send_message(embed=embed, view=StartView(self.bot))

    @command(name="cats")
    async def cats(self, interaction: Interaction) -> None:
        """Returns an imbeded list of the cats the user has collected so far.
        """
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
        """ Returns the embed of the user's inventory of cats.
        """
        async with self.bot.get_db().cursor() as cursor:
            await cursor.execute('SELECT cats FROM inventory WHERE id = ?', (interaction.user.id,))
            data = await cursor.fetchall()

        return data


class StartView(View):
    """Class for StartView. Represents a button (View) object that will allow the user to choose Next
    during a quest. This is the button corresponding to the initial dialogue message.
    This is an interactive item, and clicking on it will switch the user to an EntryView object.
    
    Instance Attributes:
    - _bot: Cats Cradle discord bot.
    """

    _bot: bot.CatsCradle

    def __init__(self, bot: bot.CatsCradle) -> None:
        """ Initializes the bot to begin the quest line.
        """

        super().__init__()

        self._bot = bot

    @button(label="Next", style=ButtonStyle.blurple)
    async def start(self, interaction: Interaction, button: Button):
        """Loads the Next button at the bottom of a bot message when called.
        """
        embed = self._bot.get_user().get_position().get_dialogue(Context.ENTER).embeddify(Color.blurple())
        await interaction.response.send_message(embed=embed, view=EntryView(self._bot))
        self.stop()


class EntryView(View):
    """Class for EntryView. Represents a button (View) object that will allow the user to choose Next
    during a quest. This is an interactive item, and clicking on it will switch the user to an InvestigateView object.
    
    Instance Attributes:
    - _bot: Cats Cradle discord bot.
    """

    _bot: bot.CatsCradle

    def __init__(self, bot: bot.CatsCradle) -> None:
        """ Initializes the bot to continue the quest line.
        """

        super().__init__()

        self._bot = bot

    @button(label="Next", style=ButtonStyle.blurple)
    async def enter(self, interaction: Interaction, button: Button):
        """Loads the Next button at the bottom of a bot message when called.
        """
        embed = self._bot.get_user().get_position().get_dialogue(Context.INVESTIGATE).embeddify(Color.blurple())
        await interaction.response.send_message(embed=embed, view=InvestigateView(self._bot))
        self.stop()


class InvestigateView(View):
    """Class for InvestigateView. Represents a button (View) object that will allow the user to choose Next
    during a quest. This is an interactive item, and clicking on it will switch the user to an either a dead end
    embed or a reward embed.
    
    Instance Attributes:
    - _bot: Cats Cradle discord bot.
    """

    _bot: bot.CatsCradle

    def __init__(self, bot: bot.CatsCradle) -> None:
        """ Initializes the bot to continue the quest line.
        """

        super().__init__()

        self._bot = bot

    @button(label="Next", style=ButtonStyle.blurple)
    async def investigate(self, interaction: Interaction, button: Button):
        """Loads the Next button at the bottom of a bot message when called. Then, switches to either a
        nothing found page or a cat acquired page. Calls on the RewardView class.
        """
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
    """Class for RewardView. Represents a button (View) object that will allow the user to choose Next
    during a quest. This is an interactive item, and clicking on it will switch the user to an ExitView object.
    
    Instance Attributes:
    - _bot: Cats Cradle discord bot.
    """

    _bot: bot.CatsCradle

    def __init__(self, bot: bot.CatsCradle) -> None:
        """ Initializes the bot to continue the quest line.
        """

        super().__init__()

        self._bot = bot

    @button(label="Next", style=ButtonStyle.blurple)
    async def claim(self, interaction: Interaction, button: Button):
        """Loads the Next button at the bottom of a bot message when called.
        """
        position = self._bot.get_user().get_position()
        embed = position.get_dialogue(Context.EXIT).embeddify(Color.dark_blue())
        await interaction.response.send_message(embed=embed, view=ExitView(self._bot))
        self.stop()


class ExitView(View):
    """Class for ExitView. Represents a button (View) object that will allow the user to choose Next
    during a quest. This is an interactive item, and clicking on it will switch the user to a NextPathsView object.
    
    Instance Attributes:
    - _bot: Cats Cradle discord bot.
    """

    _bot: bot.CatsCradle

    def __init__(self, bot: bot.CatsCradle) -> None:
        """ Initializes the bot to continue the quest line.
        """

        super().__init__()

        self._bot = bot

    @button(label="Next", style=ButtonStyle.blurple)
    async def exit(self, interaction: Interaction, button: Button):
        """Loads the Next button at the bottom of a bot message when called.
        """
        position = self._bot.get_user().get_position()
        if len(position.paths) == 0:
            new_biome = self._bot.get_biome_gen().get_next_biome()

            size = random.choices(["small", "medium", "large"], [6, 3, 1])[0]
            extension = "-" + size + ".csv"

            file_name = str(new_biome)[6:].lower() + extension

            tree = self._bot.deserializer.deserialize_tree(f"data/tree/{file_name}")
            position.add_path(tree)
        first = list(position.paths.keys())[0]

        embed = position.paths[first].get_dialogue(Context.PREVIEW).embeddify(Color.blurple())
        await interaction.response.send_message(embed=embed, view=NextPathsView(self._bot))
        self.stop()


class NextPathsView(View):
    """Class for NextPathsView. Represents three button objects that will allow the user to choose back, select
    or next during a quest. This is an interactive item, and clicking on it will switch 
    the user to self or an EntryView object.
    
    Instance Attributes:
    - _curr_index: the position the bot is in.
    - _bot: Cats Cradle discord bot.
    - _ids: a list of the ids of the possible choices the user can make.
    """

    _curr_index: int
    _bot: bot.CatsCradle
    _ids: list[str]

    def __init__(self, bot: bot.CatsCradle) -> None:
        """
        """

        super().__init__()

        self._curr_index = 0
        self._bot = bot

        user = self._bot.get_user()
        self._ids = list(user.get_choices().keys())

    @button(label="Back", style=ButtonStyle.blurple)
    async def back(self, interaction: Interaction, button: Button):
        """Loads the Back button at the bottom of a bot message when called.
        """
        user = self._bot.get_user()
        paths = user.get_choices()

        self._curr_index = (self._curr_index - 1) % len(paths)

        curr_tree = paths[self._ids[self._curr_index]]
        embed = curr_tree.get_dialogue(Context.PREVIEW).embeddify(Color.blurple())
        embed.title = f"Choose a New Path! {self._curr_index + 1}/{len(paths)}"
        await interaction.response.edit_message(embed=embed, view=self)

    @button(label="Select", style=ButtonStyle.green)
    async def select(self, interaction: Interaction, button: Button):
        """Loads the Select button at the bottom of a bot message when called.
        """
        user = self._bot.get_user()

        choice = self._ids[self._curr_index]
        new_tree = user.make_choice(choice)
        self._bot.get_biome_gen().update_traversal(new_tree.current_node.biome)

        dialogue = new_tree.get_dialogue(Context.ENTER)
        embed = dialogue.embeddify(Color.blurple())
        await interaction.response.send_message(embed=embed, view=EntryView(self._bot))
        self.stop()

    @button(label="Next", style=ButtonStyle.blurple)
    async def next(self, interaction: Interaction, button: Button):
        """Loads the Next button at the bottom of a bot message when called.
        """
        user = self._bot.get_user()
        paths = user.get_choices()

        self._curr_index = (self._curr_index + 1) % len(paths)

        curr_tree = paths[self._ids[self._curr_index]]
        embed = curr_tree.get_dialogue(Context.PREVIEW).embeddify(Color.blurple())
        embed.title = f"Choose a New Path! {self._curr_index + 1}/{len(paths)}"
        await interaction.response.edit_message(embed=embed, view=self)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
    })
