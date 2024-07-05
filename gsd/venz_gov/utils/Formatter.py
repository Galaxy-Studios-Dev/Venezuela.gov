
class Formatter:
    beginning = "```diff\n"
    ending = "\n```"

    def __init__(self):
        pass

    def formatDefaultData(self, file):
        lines = file.readlines()
        temp_dict = {}

        for line in lines:
            if line == "\n":
                pass
            else:
                key_values = line.split(":")
                temp_dict[key_values[0].replace("\n", "")] = key_values[1].replace("\n", "")

        return temp_dict

    def formatIds(self, ids):
        temp = ""
        count = 1

        for id in ids:
            if id == " " or id == "":
                pass
            else:
                id_number = "Id" + str(count)
                temp = temp + id_number + ": " + id + "\n"
                count = count + 1

        return f"{self.beginning}{temp}{self.ending}"
