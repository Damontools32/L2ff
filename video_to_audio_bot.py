import os
import tempfile
import subprocess
from telegram import InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
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

def start(update, context):
    update.message.reply_text('لطفا ویدیویی که می‌خواهید به صوت تبدیل شود را ارسال کنید.')

def handle_video(update, context):
    video = update.message.video
    video_file = context.bot.getFile(video.file_id)

    # ذخیره ویدیوی دریافتی در یک فایل موقت
    with tempfile.NamedTemporaryFile(prefix='video_', suffix='.mp4', delete=False) as video_temp:
        video_file.download(video_temp.name)
        video_path = video_temp.name

    # تبدیل ویدیو به فایل صوتی و ذخیره آن در یک فایل موقت
    with tempfile.NamedTemporaryFile(prefix='audio_', suffix='.ogg', delete=False) as audio_temp:
        audio_path = audio_temp.name
        convert_video_to_audio(video_path, audio_path)

    # ذخیره فایل صوتی در سرور و ارسال لینک دانلود به کاربر
    download_url = save_audio_file(audio_path)
    update.message.reply_text(f'فایل صوتی آماده است. لینکدانلود:\n{download_url}')

    # پاک کردن فایل‌های موقت
    os.remove(video_path)
    os.remove(audio_path)

def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.video, handle_video))

    updater.start_polling()
    updater.idle()

if __name__ =='__main__':
    main()
