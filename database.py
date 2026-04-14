import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# .env faylini yuklash
load_dotenv()

# ===================== DATABASE CONFIG =====================
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DB_CONFIG = {
        "host":     os.getenv("DB_HOST", "localhost"),
        "port":     int(os.getenv("DB_PORT", 5432)),
        "database": os.getenv("DB_NAME", "telegram_bot_db"),
        "user":     os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", "")
    }
# ===========================================================

def get_connection():
    """PostgreSQL ga ulanish"""
    if DATABASE_URL:
        return psycopg2.connect(DATABASE_URL)
    return psycopg2.connect(**DB_CONFIG)


def create_tables():
    """Jadvallarni yaratish (agar mavjud bo'lmasa)"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id          SERIAL PRIMARY KEY,
            telegram_id BIGINT UNIQUE NOT NULL,
            username    VARCHAR(100),
            full_name   VARCHAR(200),
            joined_at   TIMESTAMP DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS messages (
            id          SERIAL PRIMARY KEY,
            telegram_id BIGINT NOT NULL,
            content     TEXT NOT NULL,
            sent_at     TIMESTAMP DEFAULT NOW(),
            FOREIGN KEY (telegram_id) REFERENCES users(telegram_id)
        );

        CREATE TABLE IF NOT EXISTS dizim (
            id          SERIAL PRIMARY KEY,
            telegram_id BIGINT NOT NULL,
            ism         VARCHAR(100),
            familiya    VARCHAR(100),
            telefon     VARCHAR(20),
            izoh        TEXT,
            qoshilgan   TIMESTAMP DEFAULT NOW()
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("[OK] Jadvallar muvaffaqiyatli yaratildi!")


def save_user(telegram_id: int, username: str, full_name: str):
    """Foydalanuvchini saqlash yoki yangilash"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (telegram_id, username, full_name)
        VALUES (%s, %s, %s)
        ON CONFLICT (telegram_id)
        DO UPDATE SET username = EXCLUDED.username, full_name = EXCLUDED.full_name;
    """, (telegram_id, username, full_name))
    conn.commit()
    cur.close()
    conn.close()


def save_message(telegram_id: int, content: str):
    """Xabarni saqlash"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO messages (telegram_id, content) VALUES (%s, %s);
    """, (telegram_id, content))
    conn.commit()
    cur.close()
    conn.close()


def add_to_dizim(telegram_id: int, ism: str, familiya: str, telefon: str, izoh: str = ""):
    """Dizimga yangi yozuv qo'shish"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO dizim (telegram_id, ism, familiya, telefon, izoh)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
    """, (telegram_id, ism, familiya, telefon, izoh))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return new_id


def get_all_dizim():
    """Barcha dizim yozuvlarini olish"""
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        SELECT d.id, d.ism, d.familiya, d.telefon, d.izoh,
               u.username, d.qoshilgan
        FROM dizim d
        LEFT JOIN users u ON u.telegram_id = d.telegram_id
        ORDER BY d.qoshilgan DESC;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_user_dizim(telegram_id: int):
    """Foydalanuvchining o'z yozuvlarini olish"""
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        SELECT * FROM dizim WHERE telegram_id = %s ORDER BY qoshilgan DESC;
    """, (telegram_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def delete_dizim(record_id: int):
    """Dizimdan yozuvni o'chirish"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM dizim WHERE id = %s;", (record_id,))
    conn.commit()
    cur.close()
    conn.close()


def get_stats():
    """Statistika"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users;")
    users_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM dizim;")
    dizim_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM messages;")
    msg_count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return users_count, dizim_count, msg_count
