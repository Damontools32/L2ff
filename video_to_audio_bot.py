import os
import tempfile
from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'


def start(update: Update, context: CallbackContext):
    update.message.reply_text('لطفا ویدیویی که می‌خواهید به صوت تبدیل کنید را ارسال کنید.')


def convert_video_to_audio(update: Update, context: CallbackContext):
    video_file = update.message.video.get_file()
    with tempfile.TemporaryDirectory() as tmpdir:
        video_path = os.path.join(tmpdir, 'input_video.mp4')
        audio_path = os.path.join(tmpdir, 'output_audio.ogg')
        video_file.download(video_path)
        
        os.system(f'ffmpeg -i {video_path} -vn -c:a libopus {audio_path}')
        
        with open(audio_path, 'rb') as audio_file:
            context.bot.send_audio(chat_id=update.message.chat_id, audio=InputFile(audio_file))


def main():
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.video, convert_video_to_audio))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
