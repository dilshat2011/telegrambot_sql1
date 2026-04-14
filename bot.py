import os
import logging
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton,
    WebAppInfo, CallbackQuery, MenuButtonWebApp
)
from database import (
    create_tables, save_user, save_message,
    add_to_dizim, get_all_dizim,
    get_user_dizim, get_stats, delete_dizim
)

# ===================== .ENV YUKLASH =====================
load_dotenv()
BOT_TOKEN      = os.getenv("BOT_TOKEN")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "2011")
MINI_APP_URL   = os.getenv("MINI_APP_URL", "https://texnopark.github.io/tg-mini-app-test/")
# ========================================================

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN topilmadi! .env faylini tekshiring.")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp  = Dispatcher(storage=MemoryStorage())

# ─────────────── Message Saving Middleware ───────────────
@dp.message.outer_middleware()
async def save_every_message_middleware(handler, event: types.Message, data):
    if event.text:
        save_message(event.from_user.id, event.text)
    return await handler(event, data)


# ─────────────── FSM States ───────────────
class DizimState(StatesGroup):
    ism      = State()
    familiya = State()
    telefon  = State()
    izoh     = State()

class AdminState(StatesGroup):
    wait_password = State()
    is_admin      = State()


# ─────────────── Klaviaturalar ───────────────
def main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Dizimga qo'shish"),  KeyboardButton(text="📋 Mening yozuvlarim")],
            [KeyboardButton(text="📊 Statistika"),         KeyboardButton(text="🔑 Admin Panel")],
            [KeyboardButton(text="📱 Mini Appni ochish", web_app=WebAppInfo(url=MINI_APP_URL))],
        ],
        resize_keyboard=True
    )

def admin_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Barcha yozuvlar"), KeyboardButton(text="🗑 O'chirish rejimi")],
            [KeyboardButton(text="📊 Umumiy statistika"), KeyboardButton(text="🚪 Chiqish")],
        ],
        resize_keyboard=True
    )

def cancel_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Bekor qilish")]],
        resize_keyboard=True
    )


# ─────────────── /start Buyrug'i ───────────────
@dp.message(CommandStart())
async def cmd_start(msg: types.Message):
    user = msg.from_user
    save_user(user.id, user.username or "", user.full_name)

    await bot.set_chat_menu_button(
        chat_id=msg.chat.id,
        menu_button=MenuButtonWebApp(text="Mini App", web_app=WebAppInfo(url=MINI_APP_URL))
    )

    await msg.answer(
        f"👋 Salom, <b>{user.full_name}</b>!\n\n"
        "🗄️ Har bir yozgan xabaringiz endi PostgreSQL bazasiga saqlanadi.\n\n"
        "📌 Imkoniyatlar:\n"
        "• 📝 Dizimga qo'shish — ma'lumot kiritish\n"
        "• 📱 Mini App — bot ichidagi maxsus ilova\n"
        "• 🔑 Admin Panel — boshqaruv paneli\n",
        parse_mode="HTML",
        reply_markup=main_keyboard()
    )


# ─────────────── Admin Panel Kirish ───────────────
@dp.message(F.text == "🔑 Admin Panel")
async def admin_entry(msg: types.Message, state: FSMContext):
    await msg.answer("🔒 Admin parolini kiriting:", reply_markup=cancel_keyboard())
    await state.set_state(AdminState.wait_password)

@dp.message(AdminState.wait_password)
async def check_admin_password(msg: types.Message, state: FSMContext):
    if msg.text == "❌ Bekor qilish":
        await state.clear()
        await msg.answer("Bekor qilindi.", reply_markup=main_keyboard())
        return

    if msg.text == ADMIN_PASSWORD:
        await state.set_state(AdminState.is_admin)
        await msg.answer("✅ Xush kelibsiz, Admin! Bo'limni tanlang:", reply_markup=admin_keyboard())
    else:
        await msg.answer("❌ Parol noto'g'ri! Qayta urining.")


@dp.message(AdminState.is_admin, F.text == "🚪 Chiqish")
async def admin_logout(msg: types.Message, state: FSMContext):
    await state.clear()
    await msg.answer("Admin paneldan chiqildi.", reply_markup=main_keyboard())


@dp.message(AdminState.is_admin, F.text == "📋 Barcha yozuvlar")
async def admin_all_list(msg: types.Message):
    rows = get_all_dizim()
    if not rows:
        await msg.answer("📭 Bazada yozuv yo'q.")
        return

    text = f"📋 <b>Barcha yozuvlar ({len(rows)} ta):</b>\n\n"
    for r in rows:
        uname = r['username'] if r['username'] else "noma'lum"
        vaqt  = r['qoshilgan'].strftime('%d.%m.%Y %H:%M')
        text += (
            f"🆔 {r['id']} | <b>{r['ism']} {r['familiya']}</b>\n"
            f"📞 {r['telefon']} | @{uname}\n"
            f"🕐 {vaqt}\n\n"
        )
    await msg.answer(text, parse_mode="HTML")


@dp.message(AdminState.is_admin, F.text == "🗑 O'chirish rejimi")
async def admin_delete_mode(msg: types.Message):
    rows = get_all_dizim()
    if not rows:
        await msg.answer("📭 O'chirish uchun yozuv yo'q.")
        return

    for r in rows[:10]:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🗑 O'chirish", callback_data=f"del_{r['id']}")]
        ])
        await msg.answer(
            f"🆔 {r['id']} | {r['ism']} {r['familiya']}\n📞 {r['telefon']}",
            reply_markup=keyboard
        )

@dp.callback_query(F.data.startswith("del_"))
async def process_delete(callback: CallbackQuery, state: FSMContext):
    cur_state = await state.get_state()
    if cur_state != AdminState.is_admin:
        await callback.answer("❌ Ruxsat yo'q!", show_alert=True)
        return

    record_id = int(callback.data.split("_")[1])
    delete_dizim(record_id)
    await callback.message.edit_text(f"✅ ID: {record_id} o'chirildi.")
    await callback.answer("O'chirildi")


# ─────────────── Dizimga qo'shish ───────────────
@dp.message(F.text == "📝 Dizimga qo'shish")
async def start_dizim(msg: types.Message, state: FSMContext):
    await state.set_state(DizimState.ism)
    await msg.answer("1️⃣ Ismingizni kiriting:", reply_markup=cancel_keyboard())

@dp.message(DizimState.ism)
async def get_ism(msg: types.Message, state: FSMContext):
    if msg.text == "❌ Bekor qilish":
        await state.clear()
        await msg.answer("Bekor qilindi.", reply_markup=main_keyboard())
        return
    await state.update_data(ism=msg.text)
    await state.set_state(DizimState.familiya)
    await msg.answer("2️⃣ Familiyangizni kiriting:")

@dp.message(DizimState.familiya)
async def get_familiya(msg: types.Message, state: FSMContext):
    await state.update_data(familiya=msg.text)
    await state.set_state(DizimState.telefon)
    await msg.answer("3️⃣ Telefon raqamingizni kiriting:")

@dp.message(DizimState.telefon)
async def get_telefon(msg: types.Message, state: FSMContext):
    await state.update_data(telefon=msg.text)
    await state.set_state(DizimState.izoh)
    await msg.answer("4️⃣ Izoh yozing yoki '-' yuboring:")

@dp.message(DizimState.izoh)
async def get_izoh(msg: types.Message, state: FSMContext):
    izoh = "" if msg.text == "-" else msg.text
    data = await state.get_data()
    new_id = add_to_dizim(msg.from_user.id, data['ism'], data['familiya'], data['telefon'], izoh)
    await state.clear()
    await msg.answer(f"✅ Saqlandi! ID: {new_id}", reply_markup=main_keyboard())


# ─────────────── Statistika ───────────────
@dp.message(F.text == "📊 Statistika")
async def show_stats(msg: types.Message):
    users_count, dizim_count, msg_count = get_stats()
    await msg.answer(
        f"📊 <b>Statistika:</b>\n\n"
        f"👥 Foydalanuvchilar: <b>{users_count}</b>\n"
        f"📝 Dizim yozuvlari: <b>{dizim_count}</b>\n"
        f"💬 Xabarlar: <b>{msg_count}</b>",
        parse_mode="HTML"
    )


# ─────────────── Mening yozuvlarim ───────────────
@dp.message(F.text == "📋 Mening yozuvlarim")
async def my_records(msg: types.Message):
    rows = get_user_dizim(msg.from_user.id)
    if not rows:
        await msg.answer("📭 Sizda hali yozuv yo'q.")
        return

    text = f"📋 <b>Sizning yozuvlaringiz ({len(rows)} ta):</b>\n\n"
    for r in rows:
        vaqt = r['qoshilgan'].strftime('%d.%m.%Y %H:%M')
        text += (
            f"🆔 {r['id']} | <b>{r['ism']} {r['familiya']}</b>\n"
            f"📞 {r['telefon']}\n"
            f"🕐 {vaqt}\n\n"
        )
    await msg.answer(text, parse_mode="HTML")


# ─────────────── Botni ishga tushirish ───────────────
async def main():
    create_tables()
    logger.info("🤖 Bot ishlamoqda...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
