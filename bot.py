import discord
from discord.ext import commands
import keys

intents = discord.Intents.all()
client = discord.Client(intents=intents)
client = commands.Bot(command_prefix="-p",intents=intents)
is_client_running=False

@client.event
async def on_ready():
    global is_client_running

    if not is_client_running:
        is_client_running = True
        print(f"Bot initialising...")

@client.event
async def on_message(message):
    # Avoid the bot replying to bots
    if message.author.bot:
        return

    # Reply hello to hello messages
    if message.content.lower().startswith('hello'):
        await message.channel.send(f"Hello {message.author.mention}")
        return

    if not message.content.startswith('!'):
        return

    # Process command
    async with message.channel.typing():
        await client.process_commands(message)

@client.command(aliases=['youHaveBeenTerminated'])
@commands.is_owner()
async def terminate(ctx):
    await ctx.send("Terminating...")
    await client.close()

if __name__ == "__main__":
    client.run(keys.TOKEN)
