import discord
TOKEN = "MTA5MzQ3NjU2ODMyOTg4MzcyOQ.Gfn6QJ.PDMGlZVKOXeBeTqwJFUyWiW3ypbGrPOsYgn7No"

def main():

    client = discord.Client(intents=discord.Intents.default())

    @client.event
    async def on_ready():
        print('Tick Tock... I am {0.user}'.format(client))

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith('&time'):
            await message.channel.send('Hello!')

    client.run(TOKEN)



if __name__ == "__main__":
    main()

