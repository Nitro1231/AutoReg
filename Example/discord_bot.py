import discord
from AutoReg import AutoReg
from discord.ext import commands, tasks


TOKEN       = 'YOUR_DISCORD_BOT_TOKEN'
LOOP_TIME   = 20
CHANNEL_ID  = 000000000000000000 # Put your target channel id here.
USER_ID     = 000000000000000000 # Put your user id to ping.
COURSE_ID   = ['35870', '35880'] # Put course ids that you are looking for.


intents=discord.Intents.all()
client = commands.Bot(command_prefix=',', intents=intents)


@tasks.loop(seconds=LOOP_TIME)
async def called_once_a_day():
    message_channel = client.get_channel(CHANNEL_ID)
    text = AutoReg().getCourseInfo(COURSE_ID)

    if 'OPEN' in text:
        await message_channel.send(f'There is an open spot! <@{USER_ID}>')
        await message_channel.send(text)
    else:
        print("Not exisit.")


@called_once_a_day.before_loop
async def before():
    await client.wait_until_ready()
    print("Finished waiting")


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    called_once_a_day.start()

client.run(TOKEN)
