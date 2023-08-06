import json
from modules.platforms.functions import find_program, generate_program_key, get_resource, remove_elements, save_data, check_program_type
from modules.notifier.discord import send_notification


# checking yeswehack
def check_yeswehack(tmp_dir, mUrl, first_time, db, config):
    json_programs_key = []
    notifications = config['notifications']
    get_resource(tmp_dir, config['url'], "yeswehack")
    yeswehack = open(f"{tmp_dir}yeswehack.json")
    yeswehack = json.load(yeswehack)
    for program in yeswehack:
        programName = program['title']
        logo = program['thumbnail']['url']
        programURL = f"https://yeswehack.com/programs/{program['slug']}"
        data = {"programName": programName, "programType": "", "programURL": programURL,
                "logo": logo, "platformName": "YesWeHack","isRemoved": False, "isNewProgram": False, "color": 16270147}
        dataJson = {"programName": programName,
                    "programURL": programURL, "programType": "", "inScope": [], "reward": {}}
        programKey = generate_program_key(programName, programURL)
        json_programs_key.append(programKey)
        watcherData = find_program(db, 'yeswehack', programKey)

        if watcherData is None:
            data["isNewProgram"] = True
            watcherData = {"programName": programName,
                           "programURL": programURL, "programType": "", "inScope": [], "reward": {}}
        for target in program["scopes"]:
            dataJson['inScope'].append(target['scope'])
        if program["bounty"]:
            dataJson['programType'] = "rdp"
            data['programType'] = "rdp"
            currency = program['business_unit']['currency']
            bounty = {
                "min": f"{program['bounty_reward_min']} {currency}",
                "max": f"{program['bounty_reward_max']} {currency}"
            }
            dataJson['reward'] = bounty
        else:
            dataJson['programType'] = "vdp"
            data['programType'] = "vdp"

        newInScope = [i for i in dataJson["inScope"]
                      if i not in watcherData["inScope"]]
        removeInScope = [i for i in watcherData["inScope"]
                         if i not in dataJson["inScope"]]

        data["newType"] = []
        data["reward"] = []
        data["removeInScope"] = []
        data["newInScope"] = []
        hasChanged = False
        send_notifi = False
        if newInScope:
            watcherData["inScope"].extend(newInScope)
            notifi_status = notifications['new_inscope']
            if notifi_status:
                data["newInScope"] = newInScope
                send_notifi = True
            hasChanged = True
        if removeInScope:
            remove_elements(watcherData["inScope"], removeInScope)
            notifi_status = notifications['removed_inscope']
            if notifi_status:
                data["removeInScope"] = removeInScope
                send_notifi = True
            hasChanged = True
        if dataJson['reward'] != watcherData['reward']:
            watcherData["reward"] = dataJson['reward']
            notifi_status = notifications['new_bounty_table']
            if notifi_status:
                data["reward"] = dataJson['reward']
                send_notifi = True
            hasChanged = True
        if dataJson["programType"] != watcherData["programType"]:
            notifi_status = notifications['new_type']
            if notifi_status:
                data["newType"] = dataJson["programType"]
                send_notifi = True
            watcherData["programType"] = dataJson["programType"]
            hasChanged = True
        if hasChanged:
            save_data(db, "yeswehack", programKey, watcherData)
            if check_program_type(data,watcherData,notifications):
                if not first_time and data['isNewProgram'] and notifications['new_program']:
                    send_notification(data, mUrl)
                elif not first_time and send_notifi and not data['isNewProgram']:
                    send_notification(data, mUrl)

    db_programs_key = db['yeswehack'].distinct("programKey")
    removed_programs_key = set(db_programs_key) - set(json_programs_key)
    for program_key in removed_programs_key:
        program = find_program(db,'yeswehack', program_key)
        data = {
            "color": 14584064,
            "logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTwToiI8YA0eLclDkd-vJ0xXs7bun5LdHfTrgJucvI&s",
            "platformName": "YesWeHack",
            "isRemoved": True, 
            "programName": program["programName"],
            "programType": program["programType"]
        }
        if notifications['removed_program'] and not first_time:
            send_notification(data,mUrl)
        db['yeswehack'].delete_many({"programKey": program_key})        
