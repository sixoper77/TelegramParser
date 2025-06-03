import os
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
import asyncio
from app.parser import *
load_dotenv()
api_id=os.getenv('API_ID')
api_hash=os.getenv('API_HASH')
phone=os.getenv('PHONE_NUMBER')
client=TelegramClient('oper_session',api_id,api_hash)
async def main(phone):
    await client.start()
    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        try:
            client.sign_in(phone, input('Code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))
    await pars(client)
if __name__=='__main__':
    asyncio.run(main(phone))