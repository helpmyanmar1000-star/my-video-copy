import telebot
import time
import os
from flask import Flask
from threading import Thread

# --- CONFIGURATION ---
TOKEN = os.getenv("8577050959:AAGG3qQ71Hhm-26FhjN-DkKVcRhVVAUHEFw")
FROM_CHAT = "@mghlamyo666"
TO_CHAT = "@mghlamyo777"
START_ID = 5  # စတင်လိုသော ID ကို ဤနေရာတွင် ပြင်ပါ

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

    print("Bot is starting to forward in Albums...")

    while True:
        try:
            # ဗီဒီယိုကို တစ်ပုဒ်ချင်း ဆွဲယူစစ်ဆေးခြင်း
            msg = bot.forward_message(chat_id=TO_CHAT, from_chat_id=FROM_CHAT, message_id=current_id)
            
            # ဗီဒီယို ဖြစ်/မဖြစ် စစ်ဆေး (ဗီဒီယိုမဟုတ်ရင် ဖျက်ပြီး ကျော်သွားမယ်)
            if msg.content_type == 'video':
                # အခုလောလောဆယ် bot.copy_message ထက် Album စုဖို့ ပြင်ရမှာမို့
                # media_queue ထဲမှာ ID တွေကို စုမယ်
                media_queue.append(telebot.types.InputMediaVideo(msg.video.file_id))
                bot.delete_message(TO_CHAT, msg.message_id) # Forward လုပ်ထားတဲ့ တစ်ပုဒ်ချင်းစီကို ပြန်ဖျက်
                
                # ၁၀ ခုပြည့်ရင် Album အနေနဲ့ ပို့မယ်
                if len(media_queue) >= 10:
                    bot.send_media_group(TO_CHAT, media_queue)
                    video_count += 10
                    media_queue = []
                    print(f"Sent an album of 10 videos. Total: {video_count}")
                    
                    # ၉၅ ခု (သို့မဟုတ် ၁၀၀ နား) ရောက်ရင် ၅ မိနစ်နားမယ်
                    if video_count >= 90:
                        print("Reached limit, resting for 5 minutes...")
                        time.sleep(300)
                        video_count = 0
            else:
                bot.delete_message(TO_CHAT, msg.message_id) # ဗီဒီယိုမဟုတ်ရင် ဖျက်ပစ်

            current_id += 1
            time.sleep(2) # Telegram Flood ကာကွယ်ရန်

        except Exception as e:
            # Album ထဲမှာ ကျန်နေတာရှိရင် ပို့လိုက်မယ် (ဥပမာ ၇ ခုပဲ ကျန်တော့ချိန်)
            if media_queue:
                try:
                    bot.send_media_group(TO_CHAT, media_queue)
                    video_count += len(media_queue)
                    media_queue = []
                except:
                    pass
            
            print(f"Waiting for new content at ID: {current_id}")
            time.sleep(30) # ဗီဒီယိုအသစ် ထပ်တက်လာမယ့်အချိန် စောင့်ခြင်း
