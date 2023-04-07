import discord
from discord.ext import commands
import botFunc

TOKEN = "MTA5MzQ3NjU2ODMyOTg4MzcyOQ.Gfn6QJ.PDMGlZVKOXeBeTqwJFUyWiW3ypbGrPOsYgn7No"

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
    @bot.command()
    async def time(ctx, args):
        await ctx.send(botFunc.getTime(args))

    @bot.command()
    async def timeEmbed(ctx, args):
        name = bot.user.display_name
        dp = bot.user.display_avatar

        embed = discord.Embed(title = "Pendulum", colour = discord.Colour.random())
        embed.add_field(name='The time is currently : ',value = f'{botFunc.getTime(args)} at {args}')

        await ctx.send(embed=embed)

    #Running Bot
    bot.run(TOKEN)



if __name__ == "__main__":
    main()

