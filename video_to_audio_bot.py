import os
import tempfile
import subprocess
from telethon import TelegramClient
from telethon.sync import events

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
API_ID = 1234567  # جایگزین کنید با API ID دریافتی
API_HASH = "your_api_hash"  # جایگزین کنید با API Hash دریافتی

AUDIO_FILES_DIR = '/var/www/audio-files'
SERVER_DOMAIN_OR_IP = 'your_server_domain_or_IP'

def convert_video_to_audio(video_path, audio_path, audio_quality=3):
    command = f'ffmpeg -i {video_path} -vn -c:a libopus -b:a {audio_quality}k {audio_path}'
    subprocess.call(command, shell=True)

def save_audio_file(file_path):
    file_name = os.path.basename(file_path)
    destination_path = os.path.join(AUDIO_FILES_DIR, file_name)
    os.rename(file_path, destination_path)
    return f'http://{SERVER_DOMAIN_OR_IP}/{file_name}'

client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=TOKEN)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond('لطفا ویدیویی که می‌خواهید به صوت تبدیل شود را ارسال کنید.')

@client.on(events.NewMessage)
async def handle_video(event):
    if event.message.video:
        video = event.message.video
        video_path = await client.download_media(video)

        # تبدیل ویدیو به فایل صوتی و ذخیره آن در یک فایل موقت
        with tempfile.NamedTemporaryFile(prefix='audio_', suffix='.ogg', delete=False) as audio_temp:
            audio_path = audio_temp.name
            convert_video_to_audio(video_path, audio_path)

        # ذخیره فایل صوتی در سرور و ارسال لینک دانلود به کاربر
        download_url = save_audio_file(audio_path)
        await event.respond(f'فایل صوتی آماده است. لینک دانلود:\n{download_url}')

        # پاک کردن فایل‌های موقت
        os.remove(video_path)
        os.remove(audio_path)

def main():
    print("Bot started...")
    client.run_until_disconnected()

if __name__ == '__main__':
    main()
