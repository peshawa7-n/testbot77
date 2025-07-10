import os
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler
import asyncio

# Replace with your values
API_ID = int(os.getenv("APITELEGRAM_ID"))   # Your API ID
API_HASH = (os.getenv("APITELEGRAM_HASH"))
SESSION_NAME = "name1"
TARGET_CHANNEL = "@reng_tv"  # Format: @channel_username or channel ID (int)

# Progress callback
def progress(current, total):
    percent = int(current * 100 / total)
    print(f"Progress: {percent}%")

# Main logic
async def download_and_send_video(client: Client, msg: Message):
    if not msg.video:
        print("Not a video message. Skipping...")
        return

    print(f"Downloading: {msg.video.file_name or 'Unnamed Video'}")

    # Download the video
    file_path = await msg.download(progress=progress)
    print(f"Downloaded to: {file_path}")

    print(f"Sending to channel: {TARGET_CHANNEL}")
    await client.send_video(
        TARGET_CHANNEL,
        video=file_path,
        caption="Forwarded Video",
        progress=progress
    )
    print("Upload complete.")

    # Delete file to save space
    os.remove(file_path)
    print("File deleted.")

# Wrapper function to process one message
async def process_one_video(client: Client, chat_id: int, message_id: int):
    msg = await client.get_messages(chat_id, message_id)
    await download_and_send_video(client, msg)

# Entry point
async def main():
    async with Client(SESSION_NAME, API_ID, API_HASH) as app:
        # Example usage:
        source_chat_id = -1001234567890  # Change to the source chat/channel ID
        source_message_id = 42           # ID of the video message you want to download

        await process_one_video(app, source_chat_id, source_message_id)

# Run the script
if __name__ == "__main__":
    asyncio.run(main())
