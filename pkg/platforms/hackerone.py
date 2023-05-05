import json
from pkg.platforms.functions import find_program, generate_program_key, get_resource, save_data
from pkg.notifier.discord import send_notification


# checking hackerone
def check_hackerone(tmp_dir, mUrl, first_time, db, config):
    json_programs_key = []
    notifications = config['notifications']
    get_resource(tmp_dir, config['url'], "hackerone")
    hackeroneFile = open(f"{tmp_dir}hackerone.json")
    hackerone = json.load(hackeroneFile)
    hackeroneFile.close()
    for program in hackerone:
        programName = program["attributes"]["name"]
        logo = program["attributes"]["profile_picture"]
        if logo.startswith("https://hackerone-us-west-2-p"):
            logo = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTBmCle7j7K48bRZz483rDz52Nc6w0au28ASw&usqp=CAU"
        programURL = "https://hackerone.com/" + \
            program["attributes"]["handle"]+"?type=team"
        data = {"programName": programName, "programType": "", "programURL": programURL,
                "logo": logo, "platformName": "HackerOne", "isRemoved": False,"isNewProgram": False, "color": 16777215}
        dataJson = {"programName": programName,
                    "programURL": programURL, "programType": "", "scope": {}}
        programKey = generate_program_key(programName, programURL)
        json_programs_key.append(programKey)
        watcherData = find_program(db, 'hackerone', programKey)

        if watcherData is None:
            data["isNewProgram"] = True
            watcherData = {"programName": programName,
                           "programURL": programURL, "programType": "", "scope": {}}
        if program["attributes"]["offers_bounties"]:
            dataJson["programType"] = "rdp"
            data["programType"] = "rdp"
        else:
            dataJson["programType"] = "vdp"
            data["programType"] = "vdp"
        for target in program["relationships"]["structured_scopes"]["data"]:
            targetType = ""
            if target['attributes']['eligible_for_submission']:
                targetType = "(InScope)"
            else:
                targetType = "(OutOfScope)"
            if target['attributes']['instruction'] is not None:
                dataJson["scope"][target["id"]
                                  ] = f"{target['attributes']['asset_identifier']} {targetType}\n{target['attributes']['instruction']}\n"
            else:
                dataJson["scope"][target["id"]
                                  ] = f"{target['attributes']['asset_identifier']} {targetType}\n"

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
            save_data(db, "hackerone", programKey, watcherData)
            if not first_time and data['isNewProgram'] and notifications['new_program']:
                send_notification(data, mUrl)
            elif not first_time and send_notifi and not data['isNewProgram']:
                send_notification(data, mUrl)

    db_programs_key = db['hackerone'].distinct("programKey")
    removed_programs_key = set(db_programs_key) - set(json_programs_key)
    for program_key in removed_programs_key:
        program = find_program(db,'hackerone', program_key)
        data = {
            "color": 14584064,
            "logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTwToiI8YA0eLclDkd-vJ0xXs7bun5LdHfTrgJucvI&s",
            "platformName": "HackerOne",
            "isRemoved": True, 
            "programName": program["programName"],
            "programType": program["programType"]
        }
        if notifications['removed_program'] and not first_time:
            send_notification(data,mUrl)
        db['hackerone'].delete_many({"programKey": program_key})        
