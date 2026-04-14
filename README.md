# 🤖 Telegram Bot — PostgreSQL + Mini App

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![aiogram](https://img.shields.io/badge/aiogram-3.7.0-green)](https://aiogram.dev)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue?logo=postgresql)](https://postgresql.org)

Aiogram 3 va PostgreSQL asosida qurilgan Telegram bot. Foydalanuvchilarni ro'yxatga olish, xabarlarni saqlash, admin panel va Telegram Mini App integratsiyasini o'z ichiga oladi.

---

## ✨ Imkoniyatlar

- 📝 **Dizimga qo'shish** — Ism, familiya, telefon va izoh kiritish
- 📋 **Mening yozuvlarim** — Har bir foydalanuvchi o'z yozuvlarini ko'radi
- 📊 **Statistika** — Foydalanuvchilar, xabarlar va yozuvlar soni
- 🔑 **Admin Panel** — Parolli kirish, barcha yozuvlarni ko'rish va o'chirish
- 📱 **Telegram Mini App** — Bot ichida web ilova
- 🗄️ **PostgreSQL** — Barcha xabarlar va ma'lumotlar bazaga saqlanadi

---

## 📁 Loyiha tuzilmasi

```
telegram-bot/
├── bot.py            # Asosiy bot fayli
├── database.py       # PostgreSQL bilan ishlash
├── setup.sql         # Bazani qo'lda sozlash uchun SQL
├── requirements.txt  # Kerakli paketlar
├── .env              # Maxfiy sozlamalar (gitga yuklanmaydi!)
└── .env.example      # .env uchun namuna
```

---

## 🚀 O'rnatish va ishga tushirish

### 1. Reponi klonlash

```bash
git clone https://github.com/username/telegram-bot.git
cd telegram-bot
```

### 2. Paketlarni o'rnatish (venv siz)

```bash
pip install -r requirements.txt
```

### 3. `.env` faylini sozlash

`.env.example` faylini nusxalab, `.env` nomini bering va to'ldiring:

```bash
copy .env.example .env
```

`.env` faylini oching va quyidagilarni to'ldiring:

```env
BOT_TOKEN=your_bot_token_here
ADMIN_PASSWORD=your_password
MINI_APP_URL=https://your-mini-app-url.com/

DB_HOST=localhost
DB_PORT=5432
DB_NAME=telegram_bot_db
DB_USER=postgres
DB_PASSWORD=your_db_password
```

### 4. PostgreSQL bazasini yaratish

```sql
-- psql da:
CREATE DATABASE telegram_bot_db;
```

Yoki `setup.sql` faylini ishga tushiring:

```bash
psql -U postgres -f setup.sql
```

### 5. Botni ishga tushirish

```bash
python bot.py
```

---

## ⚙️ Talablar

| Dastur | Versiya |
|--------|---------|
| Python | 3.10+   |
| PostgreSQL | 13+ |
| aiogram | 3.7.0 |
| psycopg2-binary | 2.9.9 |
| python-dotenv | 1.0.1 |

---

## 🔐 Xavfsizlik

- `.env` fayli `.gitignore` da — **hech qachon GitHub ga yuklanmaydi**
- Admin panelga kirish uchun parol kerak
- Token va parollarni hech qachon kodda qoldirmang

---

## 📸 Mini App

Bot Telegram Mini App bilan integratsiya qilingan. Mini App URL ni `.env` faylidagi `MINI_APP_URL` ga yozing.

---

## 👤 Muallif

**TexnoPark** — [@texnopark](https://t.me/texnopark)

---

## 📄 Litsenziya

MIT License
