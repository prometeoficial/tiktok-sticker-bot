import os, telebot, yt_dlp, subprocess, time
from flask import Flask
from threading import Thread

TOKEN = "8408940834:AAGiDRjbsYUz_0y17EZ41OdbFAQtzOn3ScQ"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home(): return "Bot activo"

def download_and_convert(url):
    video = "v.mp4"
    sticker = "s.webp"
    with yt_dlp.YoutubeDL({'format':'mp4','outtmpl':video,'quiet':True}) as ydl:
        ydl.download([url])
    subprocess.run(['ffmpeg','-y','-i',video,'-t','5','-vf',"scale=512:512:force_original_aspect_ratio=decrease,fps=12,pad=512:512:(ow-iw)/2:(oh-ih)/2:color=0x00000000",'-vcodec','libwebp','-lossless','0','-q:v','40','-loop','0','-an',sticker])
    return sticker

@bot.message_handler(func=lambda m: 'tiktok.com' in m.text)
def handle(m):
    msg = bot.reply_to(m, "⏳ Creando sticker...")
    try:
        s_file = download_and_convert(m.text)
        with open(s_file, 'rb') as s: bot.send_sticker(m.chat.id, s)
        bot.delete_message(m.chat.id, msg.message_id)
    except Exception as e: bot.edit_message_text(f"❌ Error: {e}", m.chat.id, msg.message_id)

if __name__ == "__main__":
    Thread(target=lambda: app.run(host="0.0.0.0", port=8080)).start()
    bot.polling(none_stop=True)
