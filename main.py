import discord
from dotenv import load_dotenv
import os
import requests
import io
import re

client = discord.Client()


def get_sound_file(s):
    json = {'taibun': s}
    r = requests.post(f'https://hokbu.ithuan.tw/tau', data=json)
    taibun = r.json()['KIP']
    r = requests.get(f'https://hapsing.ithuan.tw/bangtsam?taibun={taibun}')
    return io.BytesIO(r.content)


def main():
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    client.run(TOKEN)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    tailo_r = re.compile(
        r'[áàâǎāéèêěēíìîǐīóòôǒōúùûǔ]|ḿ|m̀|m̂|m̌|m̄|ń|ǹ|n̂|ň|n̄|ⁿ|a̍|e̍|ı̍|o̍|u̍',
        flags=re.IGNORECASE)
    taigi_r = re.compile(r'[\(（][台臺]語[\)）]')
    content = message.content

    if not tailo_r.search(content) and not taigi_r.search(content):
        return

    if taigi_r.search(content):
        content = content[:-4]

    file = discord.File(get_sound_file(content), 'taigi.mp3')
    await message.channel.send(None, file=file, reference=message)


if __name__ == '__main__':
    main()
