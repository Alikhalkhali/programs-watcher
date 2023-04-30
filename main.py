import yaml
from pymongo import MongoClient

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
