import telebot
import time
import random
import os
from flask import Flask
from threading import Thread

# --- ၁။ Flask Server (Render အတွက်) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is Running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- ၂။ Bot Setup ---
# သင့်ရဲ့ Token ကို ဒီမှာထည့်ပါ (သို့မဟုတ် Render Settings ထဲမှာ ထည့်ပါ)
TOKEN = "8577050959:AAHGB2kDNHJBvOhU0Vk3AMIITX-frckqfXM" 
bot = telebot.TeleBot(TOKEN)

# @username သုံးရင် မျက်တောင်အဖွင့်အပိတ် " " ပါရပါမယ်
FROM_CHAT = "@mgkyawgyi555"  # ချန်နယ်အဟောင်း username
TO_CHAT = "@mgkyawgyi666"    # ချန်နယ်အသစ် username
START_ID = 988               # စမယ့် message id

def start_forwarding():
    video_count = 0        # အပုဒ် ၁၀၀ စစ်ဖို့
    total_batch_count = 0  # အပုဒ် ၁၀၀၀ စစ်ဖို့
    current_id = START_ID

    print("Bot စတင် အလုပ်လုပ်နေပါပြီ...")

    while True:
        try:
            # ဗီဒီယိုကို ကူးယူခြင်း
            bot.copy_message(TO_CHAT, FROM_CHAT, current_id)
            
            video_count += 100
            total_batch_count += 100
            print(f"ID {current_id} ကို ပို့ပြီးပါပြီ။ (Batch: {total_batch_count})")

            # တစ်ပုဒ်ချင်းစီကြား Random Delay (အကောင့်မပိတ်အောင် 3 စက္ကန့်မှ 4 စက္ကန့်)
            time.sleep(random.randint(5, 6))

            # ၂၀၀၀ ပြည့်ရင် နာရီဝက် နားမယ်
            if total_batch_count >= 2000:
                print("ဗီဒီယို ၂၀၀၀ ပြည့်လို့ နာရီဝက် အကြာကြီးနားနေပါသည်...")
                time.sleep(1800)
                total_batch_count = 0

        except Exception as e:
            # Message မရှိရင် (သို့) Video မဟုတ်ရင် ၅ စက္ကန့်နားပြီး နောက်တစ်ခုသွားမယ်
            time.sleep(3)
            pass
        
        current_id += 1

if __name__ == "__main__":
    keep_alive() 
    start_forwarding()
