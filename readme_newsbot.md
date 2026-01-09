# NewsHubBot - Telegram News Bot

Bot Telegram sederhana untuk mendapatkan berita terbaru secara otomatis dari berbagai sumber RSS feed.

## Deskripsi

NewsHubBot adalah project pembelajaran Python yang mendemonstrasikan cara membuat bot Telegram dengan fitur:
- Mengambil berita dari RSS feeds
- Scheduling otomatis untuk mengirim berita berkala
- Command handling untuk interaksi user
- Asynchronous programming dengan Python

## Fitur Utama

- **Multi Kategori Berita**: Teknologi, Global, Bisnis
- **Pengiriman Otomatis**: Berita dikirim setiap 30 menit
- **Command Interaktif**: User bisa request berita kapan saja
- **Duplikasi Prevention**: Berita yang sama tidak akan dikirim ulang
- **Mudah Dikustomisasi**: Tambah sumber berita dengan mudah

## Prasyarat

- Python 3.8 atau lebih baru
- Akun Telegram
- Koneksi internet

## Cara Membuat Bot Telegram

### 1. Buat Bot di Telegram

1. Buka aplikasi Telegram
2. Cari dan chat dengan [@BotFather](https://t.me/botfather)
3. Kirim command `/newbot`
4. Ikuti instruksi:
   - Masukkan nama bot (contoh: `My News Bot`)
   - Masukkan username bot (harus diakhiri dengan 'bot', contoh: `mynewsbot` atau `my_news_bot`)
5. BotFather akan memberikan **token** seperti ini:
   ```
   8227141991:AAFl8PbUroJn2puTRq5v5esw8gY70Fa_m0Q
   ```
6. **SIMPAN TOKEN INI dengan aman!** Token ini adalah kunci akses bot Anda.

### 2. Konfigurasi Tambahan Bot (Opsional)

Kirim command berikut ke @BotFather untuk kustomisasi:

- `/setdescription` - Set deskripsi bot
- `/setabouttext` - Set teks "About"
- `/setuserpic` - Upload foto profil bot
- `/setcommands` - Set list command yang muncul di menu

Contoh commands untuk `/setcommands`:
```
start - Mulai menggunakan bot
news - Dapatkan berita terbaru
auto_on - Aktifkan pengiriman otomatis
auto_off - Matikan pengiriman otomatis
sources - Lihat sumber berita
help - Panduan penggunaan
```

## Instalasi

### 1. Clone atau Download Project

```bash
git clone <repository-url>
cd NewsHubBot
```

### 2. Buat Virtual Environment (Sangat Disarankan)

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Atau install manual:
```bash
pip install python-telegram-bot==21.0 feedparser==6.0.11
```

### 4. Konfigurasi Token

Buka file `app.py` dan ganti token pada baris:
```python
TOKEN = "YOUR_BOT_TOKEN_HERE"
```

Dengan token yang Anda dapatkan dari BotFather.

## Cara Menjalankan Bot

### 1. Jalankan Bot

```bash
python app.py
```

### 2. Verifikasi Bot Berjalan

Jika berhasil, Anda akan melihat log seperti ini:
```
2026-01-09 15:56:26,860 - __main__ - INFO - Bot started!
2026-01-09 15:56:27,614 - telegram.ext.Application - INFO - Application started
```

### 3. Test Bot di Telegram

1. Cari bot Anda di Telegram dengan username yang telah dibuat
2. Kirim `/start`
3. Bot akan membalas dengan pesan welcome
4. Coba command lain seperti `/news` atau `/help`

## Command yang Tersedia

| Command | Deskripsi | Contoh |
|---------|-----------|--------|
| `/start` | Mulai menggunakan bot | `/start` |
| `/news [kategori]` | Dapatkan 5 berita terbaru | `/news teknologi` |
| `/auto_on [kategori]` | Aktifkan pengiriman otomatis | `/auto_on global` |
| `/auto_off` | Matikan pengiriman otomatis | `/auto_off` |
| `/sources` | Lihat kategori berita tersedia | `/sources` |
| `/help` | Panduan penggunaan lengkap | `/help` |

## Menambah Sumber Berita

Edit dictionary `NEWS_SOURCES` di file `app.py`:

```python
NEWS_SOURCES = {
    'teknologi': 'https://www.techinasia.com/feed',
    'global': 'http://feeds.bbci.co.uk/news/rss.xml',
    'bisnis': 'https://www.cnbc.com/id/100003114/device/rss/rss.html',
    'olahraga': 'https://rss.example.com/sports',  # Tambah disini
}
```

**Cara Mencari RSS Feed:**
1. Kunjungi website berita yang diinginkan
2. Cari link RSS (biasanya di footer atau header)
3. Atau tambahkan `/feed` atau `/rss` di akhir URL website
4. Gunakan tools seperti [RSS Feed Finder](https://www.feedspot.com/getrss)

## Hal-Hal yang Perlu Diperhatikan

### 1. Token Security

**PENTING:** Jangan upload token ke GitHub atau repository publik!

**Best Practice:**
- Gunakan environment variable
- Atau gunakan file `.env` dan tambahkan ke `.gitignore`

Contoh dengan environment variable:
```python
import os
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
```

Set di terminal:
```bash
export TELEGRAM_BOT_TOKEN="your_token_here"
```

### 2. Bot Instance

**CRITICAL:** Hanya jalankan 1 instance bot pada satu waktu!

Jika terjadi error `Conflict: terminated by other getUpdates request`:
```bash
# Cari process yang berjalan
ps aux | grep app.py

# Kill process
kill -9 <PID>

# Jalankan ulang
python app.py
```

### 3. Rate Limiting

Telegram membatasi jumlah request per detik:
- Maksimal 30 messages per detik ke user berbeda
- Maksimal 20 messages per menit ke user yang sama

**Solusi:** Tambahkan delay jika mengirim banyak pesan.

### 4. Error Handling

Bot sudah memiliki basic error handling, tapi untuk production:
- Log semua error ke file
- Implementasi retry mechanism
- Monitoring bot status
- Alert jika bot down

### 5. RSS Feed Reliability

Tidak semua RSS feed selalu available:
- Beberapa website bisa down
- Format RSS bisa berubah
- Feed bisa lambat load

**Solusi:** 
- Test semua RSS feed secara berkala
- Tambahkan timeout pada request
- Gunakan multiple sources untuk redundancy

### 6. Memory Management

Variable `sent_news` menyimpan link di memory:
- Untuk deployment jangka panjang, gunakan database (SQLite, PostgreSQL)
- Atau batasi jumlah entry dengan menghapus yang lama

### 7. Deployment

Untuk menjalankan bot 24/7:

**Option 1: VPS (DigitalOcean, Linode, AWS)**
```bash
# Gunakan screen atau tmux
screen -S newsbot
python app.py
# Ctrl+A, D untuk detach
```

**Option 2: systemd Service (Linux)**
Buat file `/etc/systemd/system/newsbot.service`:
```ini
[Unit]
Description=News Telegram Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/NewsHubBot
ExecStart=/path/to/.venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Start service:
```bash
sudo systemctl start newsbot
sudo systemctl enable newsbot
```

**Option 3: Docker**
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

**Option 4: Cloud Platform**
- Heroku (perlu Procfile)
- Railway
- Render
- PythonAnywhere

### 8. Monitoring

Track kesehatan bot:
- Jumlah user aktif
- Jumlah berita dikirim
- Error rate
- Uptime

Tools: Sentry, LogDNA, atau custom logging.

### 9. Database (untuk Production)

Untuk production, gunakan database untuk menyimpan:
- User preferences
- Sent news history
- Statistics
- Error logs

Contoh dengan SQLite:
```python
import sqlite3

def init_db():
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sent_news
                 (link TEXT PRIMARY KEY, sent_at TIMESTAMP)''')
    conn.commit()
    conn.close()
```

### 10. Backup

Backup secara berkala:
- Database
- Configuration files
- Logs

## Troubleshooting

### Bot tidak merespon

1. Cek apakah bot masih running
2. Cek koneksi internet
3. Cek logs untuk error
4. Verifikasi token masih valid

### Error "Conflict"

**Penyebab:** Ada 2+ instance bot berjalan

**Solusi:**
```bash
ps aux | grep app.py
kill -9 <PID>
python app.py
```

### Berita tidak muncul

1. Test RSS feed di browser: `https://rss-feed-url`
2. Cek apakah feedparser bisa parse: 
```python
import feedparser
feed = feedparser.parse('url')
print(feed.entries)
```
3. Ganti RSS feed jika bermasalah

### HTML parsing error

Jika ada karakter khusus di berita, sudah di-handle dengan `html.escape()`.

## Pengembangan Lebih Lanjut

Ide untuk improve bot:

1. **Database Integration**
   - Simpan user preferences
   - Track reading history
   - Analytics

2. **User Settings**
   - Pilih kategori favorit
   - Set jadwal custom
   - Filter keyword

3. **Rich Media**
   - Tampilkan thumbnail berita
   - Support video/audio
   - Inline buttons

4. **Multiple Languages**
   - Support i18n
   - Auto detect language

5. **AI Integration**
   - Summarize berita dengan AI
   - Sentiment analysis
   - Personalized recommendations

6. **Admin Panel**
   - Broadcast message
   - User statistics
   - Manage RSS sources

## Struktur Project

```
NewsHubBot/
│
├── app.py              # Main bot file
├── requirements.txt    # Python dependencies
├── README.md          # Dokumentasi ini
├── .gitignore         # Git ignore file
├── .env.example       # Template environment variables
│
└── .venv/             # Virtual environment (jangan di-commit)
```

## Lisensi

MIT License - Bebas digunakan untuk pembelajaran dan komersial.

## Kontribusi

Pull requests welcome! Untuk perubahan besar, buka issue terlebih dahulu untuk diskusi.

## Credits

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Library Telegram Bot
- [feedparser](https://github.com/kurtmckee/feedparser) - RSS Feed Parser

---

**Happy Coding!** 🚀

Jangan lupa star ⭐ repository ini jika bermanfaat!