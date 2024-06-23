# telegram_login.py

import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_api_id_hash(phone_number: str, code: str):
    try:
        with requests.Session() as req:
            logger.info("Mengirim permintaan OTP ke %s", phone_number)
            login0 = req.post('https://my.telegram.org/auth/send_password', data={'phone': phone_number})

            if 'Sorry, too many tries. Please try again later.' in login0.text:
                logger.error('Akun Anda diblokir sementara. Coba lagi dalam 8 jam.')
                return None, None, 'Akun Anda diblokir sementara. Coba lagi dalam 8 jam.'

            login_data = login0.json()
            random_hash = login_data['random_hash']

            login_data = {
                'phone': phone_number,
                'random_hash': random_hash,
                'password': code
            }

            logger.info("Masuk menggunakan OTP")
            login = req.post('https://my.telegram.org/auth/login', data=login_data)
            
            if 'Invalid' in login.text:
                logger.error('Kode OTP salah.')
                return None, None, 'Kode OTP salah. Silakan coba lagi.'

            logger.info("Mengambil halaman aplikasi")
            apps_page = req.get('https://my.telegram.org/apps')
            soup = BeautifulSoup(apps_page.text, 'html.parser')
            
            api_id = soup.find('label', string='App api_id:').find_next_sibling('div').select_one('span').get_text()
            api_hash = soup.find('label', string='App api_hash:').find_next_sibling('div').select_one('span').get_text()

            return api_id, api_hash, None
    except Exception as e:
        logger.error("Kesalahan saat mendapatkan API ID dan API Hash: %s", e)
        return None, None, str(e)
