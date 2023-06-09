import yaml
from pymongo import MongoClient
import os
import shutil
from pkg.platforms.bugcrowd import check_bugcrowd
from pkg.platforms.hackerone import check_hackerone
from pkg.platforms.intigriti import check_intigriti
from pkg.platforms.yeswehack import check_yeswehack


# load config file
with open("config.yml", "r") as ymlfile:
    cfg = yaml.full_load(ymlfile)
mUrl = cfg['discordWebhook']['programs_watcher']
platforms = {}
for platform in cfg['platforms']:
    platforms[platform['name']] = {
        'url': platform['url'],
        'notifications': platform['notifications']
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
check_bugcrowd(tmp_dir, mUrl, first_time, db, platforms['bugcrowd'])

# checking hackerone
check_hackerone(tmp_dir, mUrl, first_time, db, platforms['hackerone'])

# checking intigriti
check_intigriti(tmp_dir, mUrl, first_time, db, platforms['intigriti'])

# checking yeswehack
check_yeswehack(tmp_dir, mUrl, first_time, db, platforms['yeswehack'])

# Clean up resources and remove tmp_dir
client.close()
shutil.rmtree(tmp_dir)
