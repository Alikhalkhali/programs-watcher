import json
from pkg.platforms.functions import find_program, generate_program_key, get_resource, remove_elements, save_data
from pkg.notifier.discord import send_notification


# checking bugcrowd
def check_bugcrowd(tmp_dir, mUrl, first_time, db, config):
    notifications = config['notifications']
    get_resource(tmp_dir, config['url'], "bugcrowd")
    bugcrowdFile = open(f"{tmp_dir}bugcrowd.json")
    bugcrowd = json.load(bugcrowdFile)
    bugcrowdFile.close()
    for program in bugcrowd:
        programName = program["name"]
        programURL = "https://bugcrowd.com"+program["program_url"]
        logo = program["logo"]
        data = {"programName": programName, "reward": {}, "newType": "", "newInScope": [], "removeInScope": [], "newOutOfScope": [], "removeOutOfScope": [], "programURL": programURL,
                "logo": logo, "platformName": "Bugcrowd", "isNewProgram": False, "color": 14584064}
        dataJson = {"programName": programName, "programURL": programURL, "programType": "",
                    "outOfScope": [], "inScope": [], "reward": {}}
        programKey = generate_program_key(programName, programURL)

        watcherData = find_program(db, 'bugcrowd', programKey)
        if watcherData is None:
            data["isNewProgram"] = True
            watcherData = {"programKey": programKey, "programName": programName, "programURL": programURL, "programType": "",
                           "outOfScope": [], "inScope": [], "reward": {}}
        for target in program["target_groups"]:
            if target["in_scope"] == False:
                for item in target["targets"]:
                    dataJson["outOfScope"].append(item["name"])

            else:
                for item in target["targets"]:
                    dataJson["inScope"].append((item["name"]))
        if "min_rewards" in program:
            bounty = {
                "min": program["min_rewards"],
                "max": program["max_rewards"]
            }
            dataJson["reward"] = bounty
            dataJson["programType"] = "rdp"
            data["programType"] = "rdp"
        else:
            dataJson["programType"] = "vdp"
            data["programType"] = "vdp"
            bounty = {}
        newInScope = [i for i in dataJson["inScope"]
                      if i not in watcherData["inScope"]]
        removeInScope = [i for i in watcherData["inScope"]
                         if i not in dataJson["inScope"]]
        removedOutOfScope = [i for i in watcherData["outOfScope"]
                             if i not in dataJson["outOfScope"]]
        newOutOfScope = [i for i in dataJson["outOfScope"]
                         if i not in watcherData["outOfScope"]]
        hasChanged = False
        send_notifi = False
        if newInScope:
            watcherData["inScope"].extend(newInScope)
            notifi_status = notifications['new_inscope']
            hasChanged = True
            if notifi_status:
                data["newInScope"] = newInScope
                send_notifi = True
        if removeInScope:
            remove_elements(watcherData["inScope"], removeInScope)
            hasChanged = True
            notifi_status = notifications['removed_inscope']
            if notifi_status:
                data["removeInScope"] = removeInScope
                send_notifi = True
        if newOutOfScope:
            watcherData["outOfScope"].extend(newOutOfScope)
            hasChanged = True
            notifi_status = notifications['new_out_of_scope']
            if notifi_status:
                data["newOutOfScope"] = newOutOfScope
                send_notifi = True
        if removedOutOfScope:
            remove_elements(watcherData["outOfScope"], removedOutOfScope)
            hasChanged = True
            notifi_status = notifications['removed_out_of_scope']
            if notifi_status:
                data["removeOutOfScope"] = removedOutOfScope
                send_notifi = True
        if dataJson["programType"] != watcherData["programType"]:
            watcherData["programType"] = dataJson["programType"]
            hasChanged = True
            notifi_status = notifications['new_type']
            if notifi_status:
                data["newType"] = dataJson["programType"]
                send_notifi = True
        if dataJson["reward"] != watcherData["reward"]:
            watcherData["reward"] = bounty
            hasChanged = True
            notifi_status = notifications['new_bounty_table']
            if notifi_status:
                data["reward"] = bounty
                send_notifi = True
        if hasChanged:
            save_data(db, "bugcrowd", programKey, watcherData)
            if not first_time and data['isNewProgram'] and notifications['new_program']:
                send_notification(data, mUrl)
            elif not first_time and send_notifi and not data['isNewProgram']:
                send_notification(data, mUrl)
