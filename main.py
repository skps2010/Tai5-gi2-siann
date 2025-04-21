import discord
from dotenv import load_dotenv
import os
import requests
import io
import re
from discord.ext import commands
from pysondb import db
import copy

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='$', intents=intents)
database = db.getDb("database.json")
log = db.getDb("log.json")
DEFAULT_SETTING = {
    'gid': -1,
    'keyword': '[\[「\'"\(（][台臺]語[\)）\]」\'"]$',
    'detect_tone': True,
}
tailo_r = re.compile(
    r'[áàâǎāéèêěēíìîǐīóòôǒōúùûǔū]|ḿ|m̀|m̂|m̌|m̄|ń|ǹ|n̂|ň|n̄|ⁿ|a̍|e̍|ı̍|o̍|u̍',
    flags=re.IGNORECASE)


def get_sound_file(s: str):
    json = {'taibun': s}
    r = requests.post(f'https://hokbu.ithuan.tw/tau', data=json)
    taibun = r.json()['KIP']
    r = requests.get(f'https://hapsing.ithuan.tw/bangtsam?taibun={taibun}')
    return io.BytesIO(r.content)


def main():
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    client.run(TOKEN)


@client.command()
async def taigi(ctx: commands.Context, *args):
    if len(args) == 0 or args[0] == 'help':
        await ctx.send(
            '$taigi [ help | rule | set_keyword [regex] | set_detect_tone [bool] | reset ]',
            reference=ctx.message)
        return
    cmd = args[0]
    gid = ctx.guild.id
    servers = database.getByQuery({"gid": gid})
    is_found = len(servers) > 0
    server = servers[0] if is_found else DEFAULT_SETTING

    if cmd == 'rule':
        await ctx.send(
            f'keyword: {server["keyword"]}\ndetect_tone: {server["detect_tone"]}',
            reference=ctx.message)

    elif cmd == 'set_keyword' and len(args) > 1 and args[1] != '':
        if is_found:
            database.updateById(server['id'], {"keyword": args[1]})
        else:
            setting = copy.deepcopy(DEFAULT_SETTING)
            setting['gid'] = gid
            setting['keyword'] = args[1]
            database.add(setting)
        await ctx.send('修改成功', reference=ctx.message)

    elif cmd == 'set_detect_tone' and len(args) > 1 and args[1] in ('True',
                                                                    'False'):
        if is_found:
            database.updateById(server['id'],
                                {"detect_tone": args[1] == 'True'})
        else:
            setting = copy.deepcopy(DEFAULT_SETTING)
            setting['gid'] = gid
            setting['detect_tone'] = args[1] == 'True'
            database.add(setting)
        await ctx.send('修改成功', reference=ctx.message)

    elif cmd == 'reset':
        if is_found:
            database.deleteById(server['id'])
        await ctx.send('修改成功', reference=ctx.message)

    else:
        await ctx.send(
            '$taigi [ help | rule | set_keyword [regex] | set_detect_tone [bool] | reset ]',
            reference=ctx.message)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    await client.process_commands(message)

    gid = message.guild.id
    servers = database.getByQuery({"gid": gid})
    server = servers[0] if len(servers) > 0 else DEFAULT_SETTING

    taigi_r = re.compile(server['keyword'])
    content = message.content

    if not (server['detect_tone']
            and tailo_r.search(content)) and not taigi_r.search(content):
        return

    log.add({
        'gid': gid,
        'name': message.guild.name,
        'uid': message.author.id,
        'username': message.author.name,
        'content': content,
        'timestamp': message.created_at.timestamp(),
    })

    content = taigi_r.sub('', content)

    content_list = content.split()
    new_content_list = []
    for ku in content_list:
        if '@' in ku:
            continue
        new_content_list.append(ku)
    content = ' '.join(new_content_list)

    file = discord.File(get_sound_file(content), 'taigi.mp3')
    await message.channel.send(None, file=file, reference=message)


if __name__ == '__main__':
    main()
