# Teligram-youtube-bot
# 📥 YouTube Downloader Telegram Bot  

A simple **Telegram Bot** to download YouTube videos & audios in multiple qualities and send them directly to Telegram.  
Powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp) & [Pyrogram](https://docs.pyrogram.org/).  

---

## 🚀 Features
- Download **YouTube Videos** in multiple resolutions (360p, 480p, 720p, 1080p).  
- Download **Audio (MP3/Opus)**.  
- Send files directly to Telegram chat.  
- Easy to deploy on **Koyeb (Free Hosting)**.  

---

## ⚙️ Setup

### 1. Clone this repo
```bash
git clone https://github.com/your-username/yt-telegram-bot.git
cd yt-telegram-bot
2. Create config.py

Inside repo, make a file config.py and add your details:

API_ID = 123456        # Your Telegram API ID (my.telegram.org से लो)
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"


---

3. Requirements

Install all dependencies:

pip install -r requirements.txt


---

4. Run Locally

chmod +x start.sh
./start.sh


☁️##Deploy on Koyeb

1. Fork this repo to your GitHub.


2. Go to Koyeb Dashboard.


3. Click New App → Deploy from GitHub.


4. Select your repo.


5. In Start command, put:

./start.sh


6. Deploy 🚀
