import os
import random


class IdHandler:
    MEMBER = "Members"
    TREASURY = "Treasury"

    member_ids = {}

    def generateId(self, id_type):
        if id_type == "Members":
            random_number = random.randint(000000000, 999999999)
            return str(random_number)

        elif id_type == "Treasury":
            random_number = random.randint(000000000000000, 999999999999999)
            return str(random_number)

    def getIds(self, path):
        temp_ids = os.listdir(path)
        temp = ""

        for temp_id in temp_ids:
            id = temp_id.split(".")[0]
            temp = temp + ":" + id

        return temp.split(":")