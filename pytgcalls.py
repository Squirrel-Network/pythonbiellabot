from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped

api_id = 123456789
api_hash = ""

client = Client("client", api_id, api_hash)

app = PyTgCalls(client)


@client.on_message(filters.command("play"))
async def play_handler(_, m):
    await app.join_group_call(
        m.chat.id,
        AudioPiped(
            'http://docs.evostream.com/sample_content/assets/sintel1m720p.mp4',
        )
    )

app.run()
