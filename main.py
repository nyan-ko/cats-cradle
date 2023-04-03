import bot
from user import User
from test_tree import p, r
from deserializer import TreeDeserializer
from biome_generator import BiomeGenerator

# bot.start(...)


b = bot.CatsCradle(User(), TreeDeserializer(p, r), BiomeGenerator())
b.run('MTA4MzI1MDc2NzI1MjY5MzA1NQ.Gs5xjl.iye3xFQcgFtslDBo1gFeecT6j78A2Ws0azwIq8')

