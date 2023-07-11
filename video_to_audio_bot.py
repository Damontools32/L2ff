import os
import tempfile
import subprocess
from telegram import InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

def convert_video_to_audio(video_path, audio_path, audio_quality=3):
    command = f'ffmpeg -i {video_path} -vn -c:a libopus -b:a {audio_quality}k {audio_path}'
    subprocess.call(command, shell=True)

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

    # ارسال فایل صوتی به کاربر
    with open(audio_path, 'rb') as audio_file:
        context.bot.send_audio(chat_id=update.effective_chat.id, audio=InputFile(audio_file))

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

if __name__ == '__main__':
    main()
