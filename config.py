# config.py

class Config:
    # Data bot
    BOT_TOKEN = '7429042824:AAG_4iwiO15vYqOCxr9Cn9ygnAG-1vNSzys'
    
    # Data owner
    OWNER_ID = 6109394253  # Ganti dengan ID Telegram Anda
    
    # Pesan start
    START_MESSAGE = "Halo! Saya adalah bot untuk mendapatkan ID channel/grup dari pesan yang diteruskan.\n\n" \
                    "Cara penggunaan:\n" \
                    "1. Bergabung dengan channel kami.\n" \
                    "2. Kirim pesan yang diteruskan dari channel/grup yang ingin Anda ketahui ID-nya."
    
    # Pesan force subs
    FORCE_SUBS_MESSAGE = "Silakan bergabung dengan channel kami untuk menggunakan bot ini: {channel_link}"
    
    # ID channel untuk force subs (jika ada)
    FORCE_SUBS_CHANNEL_ID = '@AlteregoNetwork'  # Ganti dengan ID channel Anda (opsional)
