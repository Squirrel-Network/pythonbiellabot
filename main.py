#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork
from typing import Union
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message
from aiohttp import ClientSession


api_id = 123456789
api_hash = ""

client = Client("my_account", api_id, api_hash)

#Welcome
@client.on_message(filters.new_chat_members)
async def welcome_handler(_, m: Message):
    session = ClientSession()
    try:
        for member in m.new_chat_members:
            resp = await session.get(f"https://api.nebula.squirrel-network.online/v1/blacklist/{member.id}")
            response_json = (await resp.json())
            resp_user = await session.get(f"https://api.nebula.squirrel-network.online/v1/users/{member.id}")
            response_user_json = (await resp_user.json())

            if 'error' in response_user_json:
                await m.reply_text(f"Adding {member.mention} to the database...")
            else:
                await m.reply_text(f"{member.mention} is already in the database!")

            if 'error' in response_json:
                await m.reply_text(f"Welcome {member.mention}!")
            else:
                await kick_chat_member(m.chat.id, member.id)
                await m.reply_text(
                    f"Welcome {member.mention}! But you are blacklisted, so you have been kicked.\n"
                    f"Reason: {response_json['reason']}\n"
                    f"Banned from: <a href='tg://user?id={response_json['operator_id']}'>"
                    f"{response_json['operator_first_name']}</a>\n",
                    parse_mode=ParseMode.HTML
                )
    finally:
        await session.close()


@client.on_message(filters.command("kick"))
async def kick_handler(_, m: Message):
    user_ids = m.text.split()[1:]
    for user_id in user_ids:
        await kick_chat_member(m.chat.id, user_id)
    await m.reply_text(f"Kicked {len(user_ids)} users")

#Kick Command
async def kick_chat_member(chat_id: int, user_id: Union[int, str]):
    try:
        await client.ban_chat_member(chat_id, user_id)
        await client.unban_chat_member(chat_id, user_id)
    except Exception as e:
        print(e)

client.run()
