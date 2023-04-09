import discord
from discord.ext import commands
from .botFunc import getTime, getWeather
from dotenv import dotenv_values

secrets=dotenv_values('.env')
TOKEN = secrets['TOKEN']

#Intents
intents=discord.Intents.default()
intents.message_content = True

def main():
    
    #Bot Constructor
    bot = commands.Bot(command_prefix ='&', intents=intents)

    #On Launch
    @bot.event
    async def on_ready():
        print(f'Tick Tock.... Hi, I am {bot.user}')
    
    #Basic Hello!, Command using @bot.command. (time is the command, 
    #prefix not needed as already stated)
    '''@bot.command()
    async def time(ctx, args):
        await ctx.send(getTime(args))'''

    @bot.command()
    async def time(ctx, args):
        name = bot.user.display_name
        dp = bot.user.display_avatar
        (currentTime, targetLoc) = getTime(args)

        embed = discord.Embed(title = "Pendulum", colour = discord.Colour.random())
        embed.add_field(name='The Time Is Currently: ',value = f'{currentTime} at {targetLoc}')

        await ctx.send(embed=embed)

    @bot.command()
    async def liveWeather(ctx, args):

        embed = discord.Embed(title = "Pendulum", colour = discord.Colour.random())
        embed.add_field(name=f'The weather is: ',value = getWeather(args))

        await ctx.send(embed=embed)

    #Running Bot
    bot.run(TOKEN)



if __name__ == "__main__":
    main()

