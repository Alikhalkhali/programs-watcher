import json
from modules.platforms.functions import find_program, generate_program_key, get_resource, remove_elements, save_data, check_send_notification
from modules.notifier.discord import send_notification

# checking bugcrowd
def check_bugcrowd(tmp_dir, mUrl, first_time, db, config):
    json_programs_key = []
    notifications = config['notifications']
    monitor = config['monitor']
    get_resource(tmp_dir, config['url'], "bugcrowd")
    bugcrowdFile = open(f"{tmp_dir}bugcrowd.json")
    bugcrowd = json.load(bugcrowdFile)
    bugcrowdFile.close()
    for program in bugcrowd:
        programName = program["name"]
        programURL = "https://bugcrowd.com" + program["briefUrl"]
        logo = program["logoUrl"]
        data = {"programName": programName, "reward": {}, "isRemoved": False, "newType": "", "newInScope": [], "removeInScope": [], "newOutOfScope": [], "removeOutOfScope": [], "programURL": programURL,
                "logo": logo, "platformName": "Bugcrowd", "isNewProgram": False, "color": 14584064}
        dataJson = {"programName": programName, "programURL": programURL, "programType": "", "outOfScope": [], "inScope": [], "reward": {}}
        programKey = generate_program_key(programName, programURL)
        json_programs_key.append(programKey)
        watcherData = find_program(db, 'bugcrowd', programKey)
        if watcherData is None:
            data["isNewProgram"] = True
            watcherData = {"programKey": programKey, "programName": programName, "programURL": programURL, "programType": "", "outOfScope": [], "inScope": [], "reward": {}}
        for target in program["target_groups"]:
            if target["in_scope"] == False:
                for item in target["targets"]:
                    dataJson["outOfScope"].append(item["name"])
            else:
                for item in target["targets"]:
                    dataJson["inScope"].append((item["name"]))
            if "rewardSummary" in program and program["rewardSummary"]:
                min_reward = program["rewardSummary"]["minReward"]
                max_reward = program["rewardSummary"]["maxReward"]
                # Check if at least one reward is in money format
                is_money_format = min_reward.startswith('$') or max_reward.startswith('$')
            if is_money_format:
                    dataJson["programType"] = "rdp"
                    data["programType"] = "rdp"
            else:
                dataJson["programType"] = "vdp"
                data["programType"] = "vdp"
            if is_money_format:
                if min_reward == "Points":
                    min_reward = 0 ;
            else:
                min_reward = int(min_reward.replace('$', '').replace(',', ''))
            if isinstance(max_reward, str):
                max_reward = int(max_reward.replace('$', '').replace(',', ''))
        else:
            dataJson["programType"] = "noun"
            data["programType"] = "noun"
            min_reward = 0
            max_reward = 0
            bounty = {
                "min": min_reward,
                "max": max_reward
            }
            dataJson["reward"] = bounty
        newInScope = [i for i in dataJson["inScope"]
                      if i not in watcherData["inScope"]]
        removeInScope = [i for i in watcherData["inScope"]
                         if i not in dataJson["inScope"]]
        removedOutOfScope = [i for i in watcherData["outOfScope"]
                             if i not in dataJson["outOfScope"]]
        newOutOfScope = [i for i in dataJson["outOfScope"]
                         if i not in watcherData["outOfScope"]]
        hasChanged = False
        is_update = False
        if newInScope:
            watcherData["inScope"].extend(newInScope)
            notifi_status = notifications['new_inscope']
            hasChanged = True
            if notifi_status:
                data["newInScope"] = newInScope
                is_update = True
        if removeInScope:
            remove_elements(watcherData["inScope"], removeInScope)
            hasChanged = True
            notifi_status = notifications['removed_inscope']
            if notifi_status:
                data["removeInScope"] = removeInScope
                is_update = True
        if newOutOfScope:
            watcherData["outOfScope"].extend(newOutOfScope)
            hasChanged = True
            notifi_status = notifications['new_out_of_scope']
            if notifi_status:
                data["newOutOfScope"] = newOutOfScope
                is_update = True
        if removedOutOfScope:
            remove_elements(watcherData["outOfScope"], removedOutOfScope)
            hasChanged = True
            notifi_status = notifications['removed_out_of_scope']
            if notifi_status:
                data["removeOutOfScope"] = removedOutOfScope
                is_update = True
        if dataJson["programType"] != watcherData["programType"]:
            watcherData["programType"] = dataJson["programType"]
            hasChanged = True
            notifi_status = notifications['new_type']
            if notifi_status:
                data["newType"] = dataJson["programType"]
                is_update = True
        if dataJson["reward"] != watcherData["reward"]:
            watcherData["reward"] = bounty
            hasChanged = True
            notifi_status = notifications['new_bounty_table']
            if notifi_status:
                data["reward"] = bounty
                is_update = True
        if hasChanged:
            save_data(db, "bugcrowd", programKey, watcherData)
            if check_send_notification(first_time, is_update, data,watcherData, monitor, notifications):
                    send_notification(data, mUrl)
        
    db_programs_key = db['bugcrowd'].distinct("programKey")
    removed_programs_key = set(db_programs_key) - set(json_programs_key)
    for program_key in removed_programs_key:
        program = find_program(db,'bugcrowd', program_key)
        data = {
            "color": 14584064,
            "logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTwToiI8YA0eLclDkd-vJ0xXs7bun5LdHfTrgJucvI&s",
            "platformName": "Bugcrowd",
            "isRemoved": True, 
            "programName": program["programName"],
            "programType": program["programType"]
        }
        if notifications['removed_program'] and not first_time:
            send_notification(data,mUrl)
        db['bugcrowd'].delete_many({"programKey": program_key})
