# alldebrid.py
import aiohttp
import os
from urllib.parse import unquote
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

# Utiliser les variables d'environnement
api_key = os.getenv("ALLDEBRID_API_KEY")
agent_name = os.getenv("ALLDEBRID_AGENT")

async def debrid_link(link):
    url = "https://api.alldebrid.com/v4/link/unlock"
    params = {
        'agent': agent_name,
        'apikey': api_key,
        'link': link
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                if data['status'] == 'success':
                    return data['data']['link']
    return None

async def download_file(url, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    filename = os.path.basename(unquote(url))
    dest_path = os.path.join(dest_folder, filename)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open(dest_path, 'wb') as f:
                    f.write(await response.read())
    return dest_path