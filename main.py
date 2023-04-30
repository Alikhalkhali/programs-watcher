import yaml


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
