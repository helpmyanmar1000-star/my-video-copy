import telebot
import time
import os
from flask import Flask
from threading import Thread

# --- CONFIGURATION ---
TOKEN = os.getenv("8577050959:AAGG3qQ71Hhm-26FhjN-DkKVcRhVVAUHEFw")
FROM_CHAT = "@mghlamyo666"
TO_CHAT = "@mghlamyo777"
START_ID = 5  # ပို့ချင်တဲ့ ID ကို ပြင်ပါ

bot = telebot.TeleBot(TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def keep_alive():
    app.run(host='0.0.0.0', port=8080)

def start_forwarding():
    current_id = START_ID
    video_count = 0
    media_queue = []
    last_mime_type = None

    print("Bot is starting to forward with smart formatting...")

    while True:
        try:
            # ဗီဒီယိုကို တစ်ပုဒ်ချင်း စစ်ဆေးခြင်း
            msg = bot.forward_message(chat_id=TO_CHAT, from_chat_id=FROM_CHAT, message_id=current_id)
            
            if msg.content_type == 'video':
                current_mime = msg.video.mime_type # ဖိုင်အမျိုးအစား စစ်ဆေးခြင်း (ဥပမာ video/mp4)
                
                # Format ပြောင်းသွားရင် သို့မဟုတ် ၁၀ ခုပြည့်ရင် အရင်ပို့မယ်
                if (last_mime_type and current_mime != last_mime_type) or len(media_queue) >= 10:
                    if media_queue:
                        bot.send_media_group(TO_CHAT, media_queue)
                        video_count += len(media_queue)
                        media_queue = []
                        print(f"Sent album. Total videos sent: {video_count}")

                # Queue ထဲထည့်မယ်
                media_queue.append(telebot.types.InputMediaVideo(msg.video.file_id))
                last_mime_type = current_mime
                
                # Forward လုပ်ထားတဲ့ မူရင်းကို ချက်ချင်းပြန်ဖျက် (Album အနေနဲ့ပဲ ကျန်ခဲ့အောင်)
                bot.delete_message(TO_CHAT, msg.message_id)

                # ၉၀ ကျော်ရင် ၅ မိနစ်နားမယ်
                if video_count >= 90:
                    print("Reached 90+ limit. Resting 5 minutes...")
                    time.sleep(300)
                    video_count = 0
            else:
                # ဗီဒီယိုမဟုတ်ရင် ဖျက်မယ်
                bot.delete_message(TO_CHAT, msg.message_id)

            current_id += 1
            time.sleep(1.5) # Flood ရှောင်ရန်

        except Exception as e:
            # Error တက်ရင် (သို့မဟုတ် ဗီဒီယို ကုန်သွားရင်) ကျန်နေတဲ့ Album ကို ပို့လိုက်မယ်
            if media_queue:
                try:
                    bot.send_media_group(TO_CHAT, media_queue)
                    video_count += len(media_queue)
                    media_queue = []
                    last_mime_type = None
                except:
                    pass
            print(f"Waiting for ID {current_id}...")
            time.sleep(20)

# Thread စတင်ခြင်း
t = Thread(target=keep_alive)
t.start()
start_forwarding()

