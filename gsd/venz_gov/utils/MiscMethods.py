
def validTarget(id, sender, member_data, target):
    if target == member_data[id].discord_name:
        if sender.name == target:
            return False
        else:
            print(f"{target} is a valid target!")
            return True