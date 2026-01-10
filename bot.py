import telebot
import time
import random
import os
from flask import Flask
from threading import Thread
from telebot.apihelper import ApiTelegramException

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
TOKEN = "8577050959:AAHGB2kDNHJBvOhU0Vk3AMIITX-frckqfXM" 
bot = telebot.TeleBot(TOKEN)

FROM_CHAT = "@mgkyawgyi555"  # ချန်နယ်အဟောင်း username
TO_CHAT = "@mgkyawgyi666"    # ချန်နယ်အသစ် username
START_ID = 988               # စမယ့် message id

def get_media_group_messages(message_id):
    """Media Group ရှိ မက်ဆေ့ဂျာအားလုံးကို ရယူခြင်း"""
    media_group_messages = []
    current_id = message_id
    
    try:
        # ပထမမက်ဆေ့ကို ရယူ
        first_msg = bot.copy_message(TO_CHAT, FROM_CHAT, current_id)
        if hasattr(first_msg, 'media_group_id'):
            media_group_id = first_msg.media_group_id
            media_group_messages.append(first_msg)
            
            # Media Group ရှိ ကျန်မက်ဆေ့များကို ရှာဖွေ
            next_id = current_id + 1
            while True:
                try:
                    msg = bot.copy_message(TO_CHAT, FROM_CHAT, next_id)
                    if hasattr(msg, 'media_group_id') and msg.media_group_id == media_group_id:
                        media_group_messages.append(msg)
                        next_id += 1
                    else:
                        break
                except Exception:
                    break
        else:
            media_group_messages.append(first_msg)
            
    except Exception as e:
        print(f"Error getting media group: {e}")
    
    return media_group_messages

def start_forwarding():
    video_count = 0        # အပုဒ် ၂၀၀ စစ်ဖို့
    total_batch_count = 0  # အပုဒ် ၂၀၀၀ စစ်ဖို့
    current_id = START_ID

    print("Bot စတင် အလုပ်လုပ်နေပါပြီ...")

    while True:
        try:
            # Media Group မက်ဆေ့များကို ရယူ
            messages = get_media_group_messages(current_id)
            
            if messages:
                # Media Group ရှိ မက်ဆေ့အရေအတွက်
                group_size = len(messages)
                
                # ကောင်းမွန်စွာ ကူးယူပြီးကြောင်း ရော့ပို့
                for i, msg in enumerate(messages):
                    print(f"ID {current_id + i} ကို ပို့ပြီးပါပြီ။ (Media Group: {group_size} items)")
                
                video_count += group_size
                total_batch_count += group_size
                
                # နောက် Media Group သို့ ခုန်ရန် ID ကို update
                current_id += group_size
                
                print(f"Media Group အောင်မြင်စွာ ပို့ပြီးပါပြီ။ (စုစုပေါင်း: {total_batch_count})")
                
                # ခဏနားခြင်း (Media Group အရွယ်အစားပေါ်မူတည်)
                if group_size > 5:
                    sleep_time = random.randint(10, 15)
                else:
                    sleep_time = random.randint(5, 8)
                    
                time.sleep(sleep_time)
                
            else:
                # တစ်ခုတည်းသော မက်ဆေ့ဖြစ်ပါက
                bot.copy_message(TO_CHAT, FROM_CHAT, current_id)
                
                video_count += 1
                total_batch_count += 1
                print(f"ID {current_id} ကို ပို့ပြီးပါပြီ။ (Single Message) (Batch: {total_batch_count})")
                
                current_id += 1
                time.sleep(random.randint(3, 5))

            # ၂၀၀၀ ပြည့်ရင် နာရီဝက် နားမယ်
            if total_batch_count >= 2000:
                print("ဗီဒီယို ၂၀၀၀ ပြည့်လို့ နာရီဝက် အကြာကြီးနားနေပါသည်...")
                time.sleep(1800)  # 30 မိနစ်
                total_batch_count = 0
                video_count = 0

        except ApiTelegramException as e:
            if "Too Many Requests" in str(e):
                print("Too Many Requests - ၁ မိနစ်ကြာ နားမည်...")
                time.sleep(60)
            else:
                print(f"Telegram API Error: {e}")
                time.sleep(10)
                current_id += 1
                
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)
            current_id += 1

if __name__ == "__main__":
    keep_alive() 
    start_forwarding()
