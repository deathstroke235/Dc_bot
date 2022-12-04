import discord
from discord.ext import commands
import keys
import googletrans
from help_cog import help_cog
from music_cog import music_cog

intents = discord.Intents.all()
client = discord.Client(intents=intents)
client = commands.Bot(command_prefix="-p ",intents=intents)
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
    if not message.content.startswith('-p '):
        return

    # Process command
    async with message.channel.typing():
        await client.process_commands(message)

client.remove_command('help')

#register the class with the bot
client.add_cog(help_cog(client))
client.add_cog(music_cog(client))


@client.command(aliases=['tr'])
async def translate(ctx, lang_to, *args):
    """
    Translates the given text to the language `lang_to`.
    The language translated from is automatically detected.
    """

    lang_to = lang_to.lower()
    if lang_to not in googletrans.LANGUAGES and lang_to not in googletrans.LANGCODES:
        raise commands.BadArgument("Invalid language to translate text to")

    text = ' '.join(args)
    translator = googletrans.Translator()
    text_translated = translator.translate(text, dest=lang_to).text
    await ctx.send(text_translated)

@client.command(aliases=['youHaveBeenTerminated'])
@commands.is_owner()
async def terminate(ctx):
    await ctx.send("Terminating...")
    await client.close()

if __name__ == "__main__":
    client.run(keys.TOKEN)
