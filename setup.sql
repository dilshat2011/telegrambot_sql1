-- PostgreSQL setup skripti
-- Parol: dilshat2011

-- 1. Bazani yaratish (psql da ishlating):
-- CREATE DATABASE telegram_bot_db;

-- 2. Bazaga ulanib, jadvallarni yaratish:
\c telegram_bot_db;

-- Foydalanuvchilar jadvali
CREATE TABLE IF NOT EXISTS users (
    id          SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    username    VARCHAR(100),
    full_name   VARCHAR(200),
    joined_at   TIMESTAMP DEFAULT NOW()
);

-- Xabarlar jadvali
CREATE TABLE IF NOT EXISTS messages (
    id          SERIAL PRIMARY KEY,
    telegram_id BIGINT NOT NULL,
    content     TEXT NOT NULL,
    sent_at     TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (telegram_id) REFERENCES users(telegram_id)
);

-- Dizim jadvali (asosiy jadval)
CREATE TABLE IF NOT EXISTS dizim (
    id          SERIAL PRIMARY KEY,
    telegram_id BIGINT NOT NULL,
    ism         VARCHAR(100),
    familiya    VARCHAR(100),
    telefon     VARCHAR(20),
    izoh        TEXT,
    qoshilgan   TIMESTAMP DEFAULT NOW()
);

-- Tekshirish
SELECT 'users jadvali yaratildi' AS status FROM information_schema.tables WHERE table_name = 'users';
SELECT 'messages jadvali yaratildi' AS status FROM information_schema.tables WHERE table_name = 'messages';
SELECT 'dizim jadvali yaratildi' AS status FROM information_schema.tables WHERE table_name = 'dizim';
