import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import feedparser
import asyncio
from datetime import datetime, timedelta
import html

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Simpan data berita yang sudah dikirim (untuk mencegah duplikasi)
sent_news = set()

# Daftar RSS feeds dari berbagai sumber berita
NEWS_SOURCES = {
    'teknologi': 'https://www.techinasia.com/feed',
    'global': 'http://feeds.bbci.co.uk/news/rss.xml',
    'bisnis': 'https://www.cnbc.com/id/100003114/device/rss/rss.html'
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /start"""
    welcome_message = """<b>Selamat datang di News Bot!</b>

Bot ini akan mengirimkan berita terbaru secara otomatis.

<b>Command yang tersedia:</b>
/start - Mulai bot
/news - Dapatkan berita terbaru
/auto_on - Aktifkan pengiriman otomatis (setiap 30 menit)
/auto_off - Matikan pengiriman otomatis
/sources - Lihat sumber berita yang tersedia
/help - Bantuan

Gunakan /auto_on untuk mulai menerima berita otomatis!"""
    await update.message.reply_text(welcome_message, parse_mode='HTML')


async def get_latest_news(category='global', limit=5):
    """Ambil berita terbaru dari RSS feed"""
    try:
        feed_url = NEWS_SOURCES.get(category, NEWS_SOURCES['global'])
        feed = feedparser.parse(feed_url)

        if not feed.entries:
            logger.error(f"No entries found for category: {category}")
            return []

        news_items = []
        for entry in feed.entries[:limit]:
            news_item = {
                'title': entry.get('title', 'No title'),
                'link': entry.get('link', '#'),
                'published': entry.get('published', 'N/A'),
                'summary': entry.get('summary', 'Tidak ada ringkasan')[:200]
            }
            news_items.append(news_item)

        return news_items
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        return []


async def news_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /news"""
    await update.message.reply_text("Mengambil berita terbaru...")

    # Ambil kategori dari argument (default: global)
    category = context.args[0] if context.args else 'global'

    if category not in NEWS_SOURCES:
        await update.message.reply_text(
            "Kategori tidak ditemukan. Gunakan /sources untuk melihat kategori yang tersedia."
        )
        return

    news_items = await get_latest_news(category, limit=5)

    if not news_items:
        await update.message.reply_text("Tidak dapat mengambil berita saat ini. Coba lagi nanti.")
        return

    message = f"<b>Berita Terbaru - {category.upper()}</b>\n\n"

    for i, item in enumerate(news_items, 1):
        title = html.escape(item['title'])
        link = item['link']
        published = html.escape(item['published'])

        message += f"<b>{i}. {title}</b>\n"
        message += f"<a href='{link}'>Baca selengkapnya</a>\n"
        message += f"Tanggal: {published}\n\n"

    await update.message.reply_text(message, parse_mode='HTML', disable_web_page_preview=True)


async def send_auto_news(context: ContextTypes.DEFAULT_TYPE):
    """Kirim berita otomatis ke semua user yang subscribe"""
    job_data = context.job.data
    chat_id = job_data['chat_id']
    category = job_data.get('category', 'global')

    news_items = await get_latest_news(category, limit=3)

    if not news_items:
        return

    # Filter berita yang belum pernah dikirim
    new_items = []
    for item in news_items:
        if item['link'] not in sent_news:
            new_items.append(item)
            sent_news.add(item['link'])

    if not new_items:
        return

    message = f"<b>Update Berita Otomatis - {category.upper()}</b>\n\n"

    for i, item in enumerate(new_items, 1):
        title = html.escape(item['title'])
        link = item['link']

        message += f"<b>{i}. {title}</b>\n"
        message += f"<a href='{link}'>Baca selengkapnya</a>\n\n"

    try:
        await context.bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode='HTML',
            disable_web_page_preview=True
        )
    except Exception as e:
        logger.error(f"Error sending auto news: {e}")


async def auto_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Aktifkan pengiriman berita otomatis"""
    chat_id = update.effective_chat.id

    # Cek apakah sudah ada job yang aktif
    current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    if current_jobs:
        await update.message.reply_text("Pengiriman otomatis sudah aktif!")
        return

    # Ambil kategori dari argument (default: global)
    category = context.args[0] if context.args else 'global'

    if category not in NEWS_SOURCES:
        await update.message.reply_text(
            "Kategori tidak valid. Gunakan /sources untuk melihat kategori yang tersedia."
        )
        return

    # Buat job untuk mengirim berita setiap 30 menit
    context.job_queue.run_repeating(
        send_auto_news,
        interval=1800,  # 30 menit dalam detik
        first=10,  # Kirim pertama kali setelah 10 detik
        data={'chat_id': chat_id, 'category': category},
        name=str(chat_id)
    )

    await update.message.reply_text(
        f"Pengiriman berita otomatis diaktifkan!\n"
        f"Kategori: <b>{category}</b>\n"
        f"Berita akan dikirim setiap 30 menit.\n\n"
        f"Gunakan /auto_off untuk menonaktifkan.",
        parse_mode='HTML'
    )


async def auto_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Matikan pengiriman berita otomatis"""
    chat_id = update.effective_chat.id

    current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))

    if not current_jobs:
        await update.message.reply_text("Pengiriman otomatis tidak aktif.")
        return

    for job in current_jobs:
        job.schedule_removal()

    await update.message.reply_text("Pengiriman berita otomatis dinonaktifkan.")


async def sources_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tampilkan daftar sumber berita"""
    message = "<b>Sumber Berita yang Tersedia:</b>\n\n"

    for category in NEWS_SOURCES.keys():
        message += f"- {category}\n"

    message += "\n<b>Cara menggunakan:</b>\n"
    message += "- /news teknologi - Berita teknologi\n"
    message += "- /auto_on bisnis - Auto berita bisnis\n"

    await update.message.reply_text(message, parse_mode='HTML')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /help"""
    help_text = """<b>Panduan Penggunaan News Bot</b>

<b>Command Dasar:</b>
/start - Mulai menggunakan bot
/news [kategori] - Dapatkan 5 berita terbaru
/sources - Lihat semua kategori berita

<b>Pengiriman Otomatis:</b>
/auto_on [kategori] - Aktifkan (setiap 30 menit)
/auto_off - Nonaktifkan

<b>Contoh:</b>
/news teknologi - Berita teknologi terbaru
/auto_on global - Auto berita global
/news - Berita global (default)

Butuh bantuan? Hubungi pembuat bot!"""
    await update.message.reply_text(help_text, parse_mode='HTML')


def main():
    """Fungsi utama untuk menjalankan bot"""
    # Token bot dari @BotFather
    TOKEN = "YOUR_BOT_TOKEN_HERE"

    # Buat aplikasi
    application = Application.builder().token(TOKEN).build()

    # Tambahkan command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("news", news_command))
    application.add_handler(CommandHandler("auto_on", auto_on))
    application.add_handler(CommandHandler("auto_off", auto_off))
    application.add_handler(CommandHandler("sources", sources_command))
    application.add_handler(CommandHandler("help", help_command))

    # Jalankan bot
    logger.info("Bot started!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()