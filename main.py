import yaml
from pymongo import MongoClient
import os
import shutil
from modules.platforms.bugcrowd import check_bugcrowd
from modules.platforms.hackerone import check_hackerone
from modules.platforms.intigriti import check_intigriti
from modules.platforms.yeswehack import check_yeswehack
from modules.notifier.discord import send_startup_message


# load config file
with open("config.yml", "r") as ymlfile:
    cfg = yaml.full_load(ymlfile)
discord_webhook = cfg['discordWebhook']['programs_watcher']
platforms = {}
for platform in cfg['platforms']:
    platforms[platform['name']] = {
        'url': platform['url'],
        'notifications': platform['notifications'],
        'monitor': platform['monitor']
    }

# connect to MongoDB
client = MongoClient(cfg['mongoDB']['uri'])
dbName = cfg['mongoDB']['database']
db = client[dbName]
first_time = False
if dbName not in client.list_database_names():
    first_time = True

# Check ./tmp directory exists
tmp_dir = f"./tmp/"
if os.path.exists(tmp_dir):
    shutil.rmtree(tmp_dir)
    os.mkdir(tmp_dir)
else:
    os.mkdir(tmp_dir)

# checking bugcrowd
check_bugcrowd(tmp_dir, discord_webhook, first_time, db, platforms['bugcrowd'])

# checking hackerone
check_hackerone(tmp_dir, discord_webhook, first_time, db, platforms['hackerone'])

# checking intigriti
check_intigriti(tmp_dir, discord_webhook, first_time, db, platforms['intigriti'])

# checking yeswehack
check_yeswehack(tmp_dir, discord_webhook, first_time, db, platforms['yeswehack'])

# Clean up resources and remove tmp_dir
client.close()
shutil.rmtree(tmp_dir)

if first_time:
    send_startup_message(discord_webhook)
