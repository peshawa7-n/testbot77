import os
from pyrogram import Client
from pyrogram.types import Message

# Replace with your values
API_ID = int(os.getenv("APITELEGRAM_ID"))   # Your API ID
API_HASH = (os.getenv("APITELEGRAM_HASH"))
SESSION_NAME = "name1"
TARGET_CHANNEL = "@reng_tv" 
# Format: @channel_username or channel ID (int)


# Configuration
  # <-- Replace with your API HASH

SOURCE_CHAT_ID = (os.getenv("CHANNEL_ID"))  # <-- Source chat/channel ID
SOURCE_MESSAGE_ID = 2525           # ID of the video message you want to download       # <-- Video message ID to download
TARGET_CHANNEL = "@reng_tv"  # <-- Private channel username or ID

# Progress callback
def show_progress(current, total):
    percent = int(current * 100 / total)
    print(f"Progress: {percent}%", end="\r")

# Create client
app = Client(SESSION_NAME, API_ID, API_HASH)

# Start client
app.start()

# Fetch the message
msg: Message = app.get_messages(SOURCE_CHAT_ID, SOURCE_MESSAGE_ID)

if msg.video:
    print(f"Downloading video: {msg.video.file_name or 'Unnamed video'}")

    # Download video
    file_path = app.download_media(msg, progress=show_progress)
    print("\nDownload complete.")

    print("Sending to channel...")
    # Send video to channel
    app.send_video(
        TARGET_CHANNEL,
        video=file_path,
        caption="Forwarded Video",
        progress=show_progress
    )
    print("\nUpload complete.")

    # Delete file
    os.remove(file_path)
    print("Temporary file deleted.")

else:
    print("This message does not contain a video.")

# Stop client
app.stop()
