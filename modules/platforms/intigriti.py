import json
from modules.platforms.functions import find_program, generate_program_key, get_resource, save_data
from modules.notifier.discord import send_notification


# checking intigriti
def check_intigriti(tmp_dir, mUrl, first_time, db, config):
    json_programs_key = []
    notifications = config['notifications']
    get_resource(tmp_dir, config['url'], "intigriti")
    intigriti = open(f"{tmp_dir}intigriti.json")
    intigriti = json.load(intigriti)
    for program in intigriti:
        programName = program["name"]
        logo = f"https://api.intigriti.com/file/api/file/{program['logoId']}"
        programURL = f"https://app.intigriti.com/programs/{program['companyHandle']}/{program['handle']}"
        data = {"programName": programName, "programType": "", "programURL": programURL,
                "logo": logo, "platformName": "Intigriti","isRemoved": False, "isNewProgram": False, "color": 10858237}
        dataJson = {"programName": programName,
                    "programURL": programURL, "programType": "", "scope": {}, "reward": {}}
        programKey = generate_program_key(programName, programURL)
        json_programs_key.append(programKey)
        watcherData = find_program(db, 'intigriti', programKey)

        if watcherData is None:
            data["isNewProgram"] = True
            watcherData = {"programName": programName,
                           "programURL": programURL, "programType": "", "scope": {}, "reward": {}}

        for target in program['domains']:
            if target['description'] is not None:
                dataJson['scope'][target['id']
                                  ] = f"{target['endpoint']}\n{target['description']}\n"
            else:
                dataJson['scope'][target['id']] = f"{target['endpoint']}\n"
        # checking vdp or rdp
        if program["maxBounty"]["value"] > 0:
            dataJson["programType"] = "rdp"
            bounty = {
                "min": f"{program['minBounty']['value']} {program['minBounty']['currency']}",
                "max": f"{program['maxBounty']['value']} {program['maxBounty']['currency']}"
            }
            dataJson["reward"] = bounty
            data["programType"] = "rdp"

        else:
            dataJson["programType"] = "vdp"
            data["programType"] = "vdp"
        # Checking for changes
        hasChanged = False

        scopeId = {prop for prop in dataJson["scope"]}
        dbScopeId = {prop for prop in watcherData["scope"]}
        newScope = scopeId - dbScopeId
        removedScope = dbScopeId - scopeId
        scopeId = scopeId - newScope
        data["newScope"] = []
        data["changedScope"] = []
        data["removedScope"] = []
        data["newProgramType"] = []
        data["newReward"] = []
        hasChanged = False
        send_notifi = False
        if newScope:
            notifi_status = notifications['new_scope']
            for i in newScope:
                if notifi_status:
                    data["newScope"].append(dataJson["scope"][i])
                    send_notifi = True
                watcherData["scope"][i] = dataJson["scope"][i]
            hasChanged = True
        if removedScope:
            notifi_status = notifications['removed_scope']
            for i in removedScope:
                if notifi_status:
                    data["removedScope"].append(watcherData["scope"][i])
                    send_notifi = True
                del watcherData["scope"][i]
            hasChanged = True
        if dataJson["programType"] != watcherData["programType"]:
            notifi_status = notifications['new_type']
            if notifi_status:
                data["newProgramType"] = dataJson["programType"]
                send_notifi = True
            watcherData["programType"] = dataJson["programType"]
            hasChanged = True
        if dataJson["reward"] != watcherData["reward"]:
            notifi_status = notifications['new_bounty_table']
            if notifi_status:
                data["newReward"] = dataJson["reward"]
                send_notifi = True
            watcherData["reward"] = dataJson["reward"]
            hasChanged = True

        notifi_status = notifications['changed_scope']
        for id in scopeId:
            if dataJson["scope"][id] != watcherData["scope"][id]:
                if notifi_status:
                    scope = {
                        "new": dataJson["scope"][id],
                        "old": watcherData["scope"][id],
                    }
                    data["changedScope"].append(scope)
                    send_notifi = True
                watcherData["scope"][id] = dataJson["scope"][id]
                hasChanged = True
        if hasChanged:
            save_data(db, "intigriti", programKey, watcherData)
            if not first_time and data['isNewProgram'] and notifications['new_program']:
                send_notification(data, mUrl)
            elif not first_time and send_notifi and not data['isNewProgram']:
                send_notification(data, mUrl)

    db_programs_key = db['intigriti'].distinct("programKey")
    removed_programs_key = set(db_programs_key) - set(json_programs_key)
    for program_key in removed_programs_key:
        program = find_program(db,'intigriti', program_key)
        data = {
            "color": 14584064,
            "logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTwToiI8YA0eLclDkd-vJ0xXs7bun5LdHfTrgJucvI&s",
            "platformName": "Intigriti",
            "isRemoved": True, 
            "programName": program["programName"],
            "programType": program["programType"]
        }
        if notifications['removed_program'] and not first_time:
            send_notification(data,mUrl)
        db['intigriti'].delete_many({"programKey": program_key})        
