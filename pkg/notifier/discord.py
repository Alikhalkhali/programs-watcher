from discord_webhook import DiscordWebhook, DiscordEmbed


def new_program_message(data):
    embed = DiscordEmbed(title=f"{data['programName']}",
                         description=f"** New program ** named** {data['programName']} ** added to platform!\n** Program type: ** {data['programType']}\n\n** Program page: ** [Click here]({data['programURL']})", color=data['color'])
    embed.set_thumbnail(url=data['logo'])
    embed.set_footer(text='Powered by Ali Khalkhali',
                     icon_url='https://cdn.discordapp.com/avatars/941457826662985808/488f3bcab0de041de57860b4e05e2e9f.webp')

    if data["platformName"] in ["HackerOne", "Intigriti"]:
        if data["platformName"] == "Intigriti":
            if data['newReward']:
                embed.add_embed_field(
                    name="Bounty Table:", value=f"```{data['newReward']['min']} -- {data['newReward']['max']}```", inline=False)
        if data["newScope"]:
            scope = ""
            for newScope in data["newScope"]:
                scope += f"{shorten_string(newScope)}\n"
            add_field(embed, scope, "Scope:")
    if data["platformName"] in ["Bugcrowd", "YesWeHack"]:
        if data['reward']:
            embed.add_embed_field(
                name="Bounty Table:", value=f"```{data['reward']['min']} -- {data['reward']['max']}```", inline=False)
        if data['newInScope']:
            inscope = '\n'.join(data['newInScope'])
            add_field(embed, inscope, "InScope:")
        if data["platformName"] == "Bugcrowd":
            if data['newOutOfScope']:
                newOutOfScope = '\n'.join(data['newOutOfScope'])
                add_field(embed, newOutOfScope, "Out of scope:")
    return embed



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
