from telethon import TelegramClient
from telethon.tl.types import PeerChannel
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch,ChannelParticipantsRecent
from .to_sv import *
async def pars(client:TelegramClient):
    while True:
        channel = input('Link or ID of the channel (или "exit" для выхода): ')
        if channel=='exit':
            return 
        if channel.isdigit():
            entity = PeerChannel(int(channel))
        else:
            entity = channel

        users_id = []
        users_data = []
        offset = 0
        limit = 100
        all_participants = []
        try:
            my_channel = await client.get_entity(entity)
            result = await client(GetParticipantsRequest(
                my_channel, ChannelParticipantsRecent(), offset, 15, 0))

            if len(result.users)<15:
                print('Скорее всего, список участников скрыт.')
                limit_messages = int(input('Введите лимит на сообщения: '))

                async for message in client.iter_messages(my_channel, limit_messages):
                    sender = await message.get_sender()
                    if sender and not hasattr(sender, 'title'):
                        if sender.id not in users_id:
                            users_id.append(sender.id)
                            users_data.append({
                                'username': sender.username,'id': sender.id,'first_name': sender.first_name or '','last_name': sender.last_name or '', 'phone': sender.phone or '', 'bot': sender.bot or ''})
                save_to_excel(users_data)
            else:
                print("Пользователи доступны. Начинаю сбор...")
                while True:
                    participants = await client(GetParticipantsRequest(my_channel,  ChannelParticipantsSearch(''),  offset,  limit,hash=0))
                    if not participants.users:
                        break
                    all_participants.extend(participants.users)
                    offset += len(participants.users)
                    print(f"Собрано: {len(all_participants)} пользователей...")

                for participant in all_participants:
                    users_data.append({
                        'id': participant.id, 'first_name': participant.first_name,'last_name': participant.last_name,'bot': participant.bot, 'phone': participant.phone,'username': participant.username})

                save_to_excel(users_data)

        except Exception as e:
            print(f"\nОшибка при обработке канала: {e}")
            print("Попробуй снова.\n")
     
        

       