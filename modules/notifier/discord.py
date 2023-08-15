from discord_webhook import DiscordWebhook, DiscordEmbed
from modules.notifier.functions import generate_diff, split_text, get_platform_profile, shorten_string


def add_field(embed, data, message, diff=False):
    texts = split_text(data)
    isFirstTime = 0
    type = ""
    if diff:
        type = "diff\n"
    for text in texts:
        if isFirstTime == 0:
            embed.add_embed_field(
                name=message, value=f"```{type}{text}```", inline=False)
            isFirstTime = 1
        else:
            embed.add_embed_field(
                name=" ", value=f"```{type}{text}```", inline=False)


def changed_program_message(data):
    embed = DiscordEmbed(title=f"{data['programName']}",
                         description=f"** {data['programName']} ** has changed!\n** Program type: ** {data['programType']}\n\n** Program page: ** [Click here]({data['programURL']})", color=data['color'])
    embed.set_thumbnail(url=data['logo'])
    embed.set_footer(text='Powered by Ali Khalkhali',
                     icon_url='https://cdn.discordapp.com/avatars/941457826662985808/488f3bcab0de041de57860b4e05e2e9f.webp')
    if data["platformName"] in ["HackerOne", "Intigriti"]:
        if data["newProgramType"]:
            embed.add_embed_field(name="Program type changed:",
                                  value=f"```changed to {data['newProgramType']}```", inline=False)
        if data["platformName"] == "Intigriti":
            if data['newReward']:
                embed.add_embed_field(
                    name="Bounty Table changed:", value=f"```{data['newReward']['min']} -- {data['newReward']['max']}```", inline=False)
        if data["newScope"]:
            scope = '\n'.join(data['newScope'])
            add_field(embed, scope, "Following scope added:")
        if data["removedScope"]:
            removedScope = '\n'.join(data['removedScope'])
            add_field(embed, removedScope, "Following Scope removed:")
        if data["changedScope"]:
            for scope in data["changedScope"]:
                old = scope["old"]
                new = scope["new"]
                diff = generate_diff(old, new)
                add_field(embed, diff, "Following scope changed:", True)
    if data["platformName"] in ["Bugcrowd", "YesWeHack"]:
        if data['newType']:
            embed.add_embed_field(
                name="Program Type changed", value=f"```New Type: {data['newType']}```", inline=False)
        if data['reward']:
            embed.add_embed_field(name="Bounty Table changed:",
                                  value=f"```{data['reward']['min']} -- {data['reward']['max']}```", inline=False)
        if data['newInScope']:
            inscope = '\n'.join(data['newInScope'])
            add_field(embed, inscope, "Following inScope added:")
        if data['removeInScope']:
            removeInScope = '\n'.join(data['removeInScope'])
            add_field(embed, removeInScope, "Following Inscope removed:")

        if data["platformName"] == "Bugcrowd":
            if data['newOutOfScope']:
                newOutOfScope = '\n'.join(data['newOutOfScope'])
                add_field(embed, newOutOfScope,
                          "Following out of scope added:")
            if data['removeOutOfScope']:
                removeOutOfScope = '\n'.join(data['removeOutOfScope'])
                add_field(embed, removeOutOfScope,
                          "Following out of scope removed:")
    embed.add_embed_field(name=" ", value= "[Click here to Buy me a coffee ☕](https://www.buymeacoffee.com/alikhalkhali)", inline=False)
    return embed


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

    embed.add_embed_field(name=" ", value= "[Click here to Buy me a coffee ☕](https://www.buymeacoffee.com/alikhalkhali)", inline=False)
    return embed

def removed_program_message(data):
    embed = DiscordEmbed(title=f"{data['programName']}",
                         description=f"Program named ** {data['programName']} ** has removed from platform!\n** Program type: ** {data['programType']}", color=data['color'])
    embed.set_thumbnail(url=data['logo'])
    embed.set_footer(text='Powered by Ali Khalkhali',
                     icon_url='https://cdn.discordapp.com/avatars/941457826662985808/488f3bcab0de041de57860b4e05e2e9f.webp')

    embed.add_embed_field(name=" ", value= "[Click here to Buy me a coffee ☕](https://www.buymeacoffee.com/alikhalkhali)", inline=False)
    return embed

def send_notification(data, webhook_url):

    webhook = DiscordWebhook(
        url=webhook_url, username=data['platformName'], avatar_url=get_platform_profile(data['platformName']))
    if data["isRemoved"]:
        embed = removed_program_message(data)
    elif data["isNewProgram"]:
        embed = new_program_message(data)
    else:
        embed = changed_program_message(data)
    webhook.add_embed(embed)
    response = webhook.execute()
    if response.status_code != 200:
        print(data["programName"])
        print("Error sending message:", response.content)

def send_startup_message(webhook_url):
    webhook = DiscordWebhook(
        url=webhook_url, username="Programs Watcher", avatar_url="https://t3.ftcdn.net/jpg/00/91/64/62/360_F_91646202_b3K6ELfgM2E8QIwuNTlzco7K1r3mOJvp.jpg")
    embed = DiscordEmbed(title=f"🎉 Successful Start of Programs Watcher 🎉",
                         description= "Hi, welcome to ** Programs Watcher **! 🎉\nThe program has started successfully and is now waiting for a change. 🗼✨\n** Github page: ** https://github.com/Alikhalkhali/programs-watcher", color="23ff1f")
    embed.set_footer(text='Powered by Ali Khalkhali',
                     icon_url='https://cdn.discordapp.com/avatars/941457826662985808/488f3bcab0de041de57860b4e05e2e9f.webp')
    embed.add_embed_field(name=" ", value= "[Click here to Buy me a coffee ☕](https://www.buymeacoffee.com/alikhalkhali)", inline=False)

    webhook.add_embed(embed)
    response = webhook.execute()

    if response.status_code != 200:
       print("There was an error sending the Discord message")
