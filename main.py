import os
import telebot
import yt_dlp
import subprocess
from flask import Flask
from threading import Thread

# --- CONFIGURACIÓN ---
TOKEN = "8408940834:AAGiDRjbsYUz_0y17EZ41OdbFAQtzOn3ScQ" 
bot = telebot.TeleBot(TOKEN)
app = Flask('')

@app.route('/')
def home(): return "Bot 24/7 Activo"

def run(): app.run(host='0.0.0.0', port=8000)

# Función para procesar el sticker
def video_to_sticker(url):
    video = "temp.mp4"
    sticker = "sticker.webp"
    ydl_opts = {'format': 'mp4', 'outtmpl': video, 'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    cmd = [
        'ffmpeg', '-y', '-i', video, '-t', '5',
        '-vf', "scale=512:512:force_original_aspect_ratio=decrease,fps=12,pad=512:512:(ow-iw)/2:(oh-ih)/2:color=0x00000000",
        '-vcodec', 'libwebp', '-lossless', '0', '-q:v', '30', '-loop', '0', '-an', sticker
    ]
    subprocess.run(cmd)
    return sticker

@bot.message_handler(func=lambda m: 'tiktok.com' in m.text)
def handle(m):
    aviso = bot.reply_to(m, "⏳ Procesando tu sticker...")
    try:
        archivo = video_to_sticker(m.text)
        with open(archivo, 'rb') as s:
            bot.send_sticker(m.chat.id, s)
        bot.delete_message(m.chat.id, aviso.message_id)
        os.remove("temp.mp4")
        os.remove("sticker.webp")
    except Exception as e:
        bot.edit_message_text(f"❌ Error: {e}", m.chat.id, aviso.message_id)

if __name__ == "__main__":
    Thread(target=run).start()
    bot.polling(none_stop=True)
