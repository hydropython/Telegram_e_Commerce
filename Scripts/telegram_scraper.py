from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChannel

# Replace 'your_api_id' and 'your_api_hash' with your actual values
api_id = '23671049'
api_hash = 'd3d1665096a70acd7461c155901cbc2c'
phone_number ='+251911694939'

# Create the client and connect
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    # Start the client
    await client.start()

    # Replace 'your_channel_username' with the actual channel username or ID
    channel = '@ZemenExpress'
    
    # Get the channel
    entity = await client.get_entity(channel)

    # Fetch the last 100 messages
    messages = await client(GetHistoryRequest(
        peer=entity,
        limit=100,
        offset_id=0,
        offset_date=None,
        add_offset=0,
        hash=0,
        max_id = 1,  # End day (exclusive)
        min_id = 8  # End month
    ))

    # Print the messages
    with open('messages.txt', 'a', encoding='utf-8') as f:  # Append mode
        f.write(f"\nMessages from {channel}:\n")
        for message in messages.messages:
            f.write(f"{message.sender_id}: {message.message}\n")

# Run the main function
with client:
    client.loop.run_until_complete(main())
