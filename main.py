import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Bot ayarları
API_TOKEN = '8573781291:AAH48WkzXkQVDfvtdS4FKXWNOT1IrEMzhqw' # Kendi tokeninizi buraya ekleyin
ADMIN_ID = 7878195855 # Kendi Telegram ID'nizi buraya ekleyin

# Logging yapılandırması
logging.basicConfig(level=logging.INFO)

# Bot ve Dispatcher başlatma
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Basit Veritabanı (Bellek içi - Kalıcı hale getirmek için SQLite/PostgreSQL kullanın)
db = {
    "users": set(),
    "videos": [],
    "stats": {}
}

# Klavyeler
def get_user_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("Wideo ugrat (Türkmençe)"))
    kb.add(KeyboardButton("Tötänle wideo gör (Türkmençe)"))
    return kb

def get_admin_kb():
    kb = get_user_kb()
    kb.add(KeyboardButton("Admin Paneli"))
    return kb

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    db["users"].add(user_id)
    
    welcome_text = (
        "Salam! Men Aýgül. 👋\n"
        "Meniň botuma hoş geldiňiz. Bu ýerde wideolary saklap we paýlaşyp bilersiňiz."
    )
    
    if user_id == ADMIN_ID:
        await message.reply(welcome_text, reply_markup=get_admin_kb())
    else:
        await message.reply(welcome_text, reply_markup=get_user_kb())

@dp.message_handler(lambda message: message.text == "Tötänle wideo gör (Türkmençe)")
async def send_random_video(message: types.Message):
    import random
    if not db["videos"]:
        await message.reply("Häzirlikçe wideo ýok.")
        return
    
    video_id = random.choice(db["videos"])
    await bot.send_video(message.chat.id, video_id)

@dp.message_handler(content_types=['video'])
async def handle_video(message: types.Message):
    video_id = message.video.file_id
    db["videos"].append(video_id)
    
    user_id = message.from_user.id
    db["stats"][user_id] = db["stats"].get(user_id, 0) + 1
    
    await message.reply("Wideo ýatda saklandy! Sag boluň.")

@dp.message_handler(lambda message: message.text == "Admin Paneli")
async def admin_panel(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    user_count = len(db["users"])
    video_count = len(db["videos"])
    
    stats_text = (
        "📊 **Bot Statistikasy**\n\n"
        f"Jemi ulanyjy: {user_count}\n"
        f"Jemi ýüklenen wideo: {video_count}\n\n"
        "Aktiýul ulanyjylar (Wideo ýükleýänler):\n"
    )
    
    for uid, count in db["stats"].items():
        stats_text += f"- ID: {uid}, Wideo sany: {count}\n"
        
    await message.reply(stats_text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
