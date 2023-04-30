from discord_webhook import DiscordWebhook, DiscordEmbed

def send_notification(data, webhook_url):

    webhook = DiscordWebhook(
        url=webhook_url, username=data['platformName'], avatar_url=get_platform_profile(data['platformName']))
    if data["isNewProgram"]:
        embed = new_program_message(data)
    else:
        embed = changed_program_message(data)
    webhook.add_embed(embed)
    response = webhook.execute()
    if response.status_code != 200:
        print(data["programName"])
        print("Error sending message:", response.content)
