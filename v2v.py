import os
import tempfile
import subprocess
from telethon import TelegramClient, events, Button

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
API_ID = 1234567
API_HASH = "your_api_hash"

def convert_video_to_audio(video_path, audio_path, audio_quality=16):
    command = f'ffmpeg -y -i {video_path} -vn -c:a libopus -b:a {audio_quality}k {audio_path}'
    subprocess.call(command, shell=True)

def reduce_video_size(video_path, output_path, bitrate="500k"):
    command = f'ffmpeg -y -i {video_path} -vf "scale=-1:720" -c:v libx264 -preset veryslow -crf 24 -b:v {bitrate} {output_path}'
    subprocess.call(command, shell=True)

client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=TOKEN)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond('لطفا ویدیویی که می‌خواهید به صوت تبدیل شود یا حجم آن کاهش یابد را ارسال کنید.')

@client.on(events.NewMessage)
async def handle_video(event):
    if event.message.video:
        video = event.message.video
        video_path = await client.download_media(video)
        
        buttons = [Button.inline("تبدیل به صوت", b"audio"), Button.inline("کاهش حجم ویدیو", b"reduce_size")]
        await event.respond('چه عملیاتی را می‌خواهید انجام دهید؟', buttons=buttons)

@client.on(events.CallbackQuery(pattern=b'audio'))
async def handle_audio(event):
    video_path = event.data.decode('utf-8')
    with tempfile.NamedTemporaryFile(prefix='audio_', suffix='.ogg', delete=False) as audio_temp:
        audio_path = audio_temp.name
        convert_video_to_audio(video_path, audio_path)
        await client.send_file(event.chat_id, audio_path, caption="فایل صوتی آماده است.")
        os.remove(audio_path)

@client.on(events.CallbackQuery(pattern=b'reduce_size'))
async def handle_reduce_size(event):
    video_path = event.data.decode('utf-8')
    with tempfile.NamedTemporaryFile(prefix='reduced_', suffix='.mp4', delete=False) as reduced_temp:
        reduced_path = reduced_temp.name
        reduce_video_size(video_path, reduced_path)
        await client.send_file(event.chat_id, reduced_path, caption="ویدیو با حجم کمتر آماده است.")
        os.remove(reduced_path)

def main():
    print("Bot started...")
    client.run_until_disconnected()

if __name__ == '__main__':
    main()
