from telethon import TelegramClient, events
import re
from datetime import datetime
import random
import names
from random_address import real_random_address

api_id = '21612966'
api_hash = '5bbd3c5d584a7f443e0f20625652a3ad'
source_chat_id = -1002152890891
target_user_id = -1002041615765  # Replace with actual target user ID

client = TelegramClient('user', api_id, api_hash)

MESSAGE_INTERVAL = 4 * 60
MAX_MESSAGES_PER_HOUR = 15
HOUR_LIMIT = 3600

last_sent_time = datetime.now()
message_count = 0
hour_start_time = datetime.now()

def generate_random_details(country, cc, mes, ano, cvv):
    addr = real_random_address(country=country) if country.lower() != 'united states of america' else real_random_address()

    fullinfo = (
        f"{cc}|{mes}|{ano}|{cvv}|{names.get_full_name()}|{addr['address1']}|"
        f"{addr['city']}|{addr['state']}|{addr['postalCode']}|"
        f"dob: {datetime.strftime(datetime(random.randint(1960, 2005), random.randint(1, 12), random.randint(1, 28)), '%Y-%m-%d')}|{country}"
    )
    return fullinfo

def extract_data(message_text):
    card_pattern = re.search(r'𝗖𝗮𝗿𝗱: (.+)', message_text)
    response_pattern = re.search(r'𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲: (.+)', message_text)
    gate_pattern = re.search(r'𝗚𝗮𝘁𝗲: (.+)', message_text)
    country_pattern = re.search(r'𝗖𝗼𝘂𝗻𝘁𝗿𝘆: (.+)', message_text)
    vbv_status_pattern = re.search(r'𝗩𝗕𝗩 𝗦𝘁𝗮𝘁𝘂𝘀: (.+)', message_text)
    vbv_response_pattern = re.search(r'𝗩𝗕𝗩 𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲: (.+)', message_text)

    card = card_pattern.group(1) if card_pattern else 'Null'
    response = response_pattern.group(1) if response_pattern else 'Null'
    gate = gate_pattern.group(1) if gate_pattern else 'Null'
    country = country_pattern.group(1) if country_pattern else 'Null'
    vbv_status = vbv_status_pattern.group(1) if vbv_status_pattern else 'Null'
    vbv_response = vbv_response_pattern.group(1) if vbv_response_pattern else 'Null'

    cc, mes, ano, cvv = card.split('|') if card != 'Null' else ('Null', 'Null', 'Null', 'Null')

    fullinfo = generate_random_details(country, cc, mes, ano, cvv)

    formatted_message = f"""
Dump Credit Card Approved ✅
-----------------------------
Credit Card -> {cc}|{mes}|{ano}|{cvv}
Response -> {response}
Gateway -> {gate}
Is VBV -> {vbv_status}
VBV Response -> {vbv_response}
------------------------------
Country -> {country}
Developer -> @SandeepKhadka7
Bot By -> @BlackHeadsOP
------------------------------
Additional Info -> {fullinfo}
"""
    return formatted_message

@client.on(events.NewMessage(chats=source_chat_id))
async def handler(event):
    global last_sent_time, message_count, hour_start_time

    current_time = datetime.now()
    elapsed_since_last_message = (current_time - last_sent_time).total_seconds()
    elapsed_since_hour_start = (current_time - hour_start_time).total_seconds()

    if elapsed_since_hour_start > HOUR_LIMIT:
        message_count = 0
        hour_start_time = current_time

    if message_count < MAX_MESSAGES_PER_HOUR and elapsed_since_last_message >= MESSAGE_INTERVAL:
        message_text = event.message.message
        formatted_message = extract_data(message_text)
        
        try:
            await client.send_message(target_user_id, formatted_message)
            last_sent_time = current_time
            message_count += 1
        except Exception as e:
            print(f"Failed to send message: {e}")
    elif message_count >= MAX_MESSAGES_PER_HOUR:
        pass
    else:
        pass

client.start()
client.run_until_disconnected()
