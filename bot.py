import discord
import os
import logging
import re
import asyncio
from dotenv import load_dotenv
from alldebrid import debrid_link, download_file
from keywords import blacklist

# Configuration de Logging
logging.basicConfig(level=logging.INFO, filename='/app/logs/bot_log.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

client = discord.Client(intents=intents)

# Charger les variables d'environnement depuis .env
load_dotenv()

# Utiliser le token depuis les variables d'environnement
token = os.getenv("DISCORD_TOKEN")
user_id = os.getenv("USER_ID")
download_folder = "/app/@anime_en_attente" #CHANGER LE @anime_en_attente, si vous n'avez pas le même nom
watch_channel_ids = os.getenv("WATCH_CHANNEL_IDS").split(',')

def contains_keyword(text, keywords):
    return any(keyword.lower() in text.lower() for keyword in keywords)

@client.event
async def on_ready():
    logging.info(f'Logged in as {client.user}!')

@client.event
async def on_message(message):
    if message.author == client.user or str(message.channel.id) not in watch_channel_ids:
        return

    user = await client.fetch_user(user_id)
    if not user:
        logging.error(f"User with ID {user_id} not found.")
        return

    # Envoyer le texte du message s'il y en a
    if message.content:
        await user.send(message.content)

    # Gérer les embeds
    for embed in message.embeds:
        await user.send(embed=embed)  # Envoyer l'embed original

        # Fonction pour rechercher un lien dans un texte
        def find_link_in_text(text):
            return re.search(r'https://1fichier\.com/\S+', text)

        # Analyser tous les champs de l'embed pour trouver un lien
        download_link = None
        fields_to_check = [
            embed.title,
            embed.description,
            embed.footer.text if embed.footer else None,
            embed.author.name if embed.author else None,
            embed.author.url if embed.author else None,
            embed.thumbnail.url if embed.thumbnail else None,
            embed.image.url if embed.image else None
        ]

        for field in fields_to_check:
            if field:
                url_match = find_link_in_text(field)
                if url_match:
                    download_link = url_match.group(0)
                    break

        if not download_link:
            for field in embed.fields:
                url_match = find_link_in_text(field.name)
                if url_match:
                    download_link = url_match.group(0)
                    break
                url_match = find_link_in_text(field.value)
                if url_match:
                    download_link = url_match.group(0)
                    break

        if download_link:
            embed_content = f"{embed.title} {embed.description} {embed.footer.text if embed.footer else ''} " \
                            f"{embed.author.name if embed.author else ''} {embed.author.url if embed.author else ''} " \
                            f"{embed.thumbnail.url if embed.thumbnail else ''} {embed.image.url if embed.image else ''} " \
                            f"{' '.join(field.value for field in embed.fields)}"

            if contains_keyword(embed_content, blacklist):
                await user.send("Blacklisted, voir fichier keywords.py")
                logging.info(f'Message from {message.channel.id} contains blacklisted keywords.')
            else:
                await user.send(f'Lien de téléchargement trouvé: {download_link}')
                await asyncio.sleep(45)  # Attendre 30 secondes avant de débrider le lien
                debrid_link_url = await debrid_link(download_link)
                if debrid_link_url:
                    await asyncio.sleep(15)  # Attendre 15 secondes avant de débrider le lien
                    downloaded_file_path = await download_file(debrid_link_url, download_folder)
                    await user.send(f'Fichier téléchargé et mit dans: {downloaded_file_path}')
                else:
                    message_fail = f'FAIL veuillez relancer ceci manuellement: {download_link}'
                    await user.send(message_fail)
                    await user.send(embed=embed)

client.run(token)
