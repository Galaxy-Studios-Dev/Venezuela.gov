import os

from gsd.venz_gov.classes.Bank import Bank
from gsd.venz_gov.classes.Member import Member
from gsd.venz_gov.classes.banking.BankAccount import BankAccount
from gsd.venz_gov.utils.Formatter import Formatter
from gsd.venz_gov.utils.IdHandler import IdHandler
from gsd.venz_gov.utils.PathHandler import PathHandler


class FileHandler:
    path_handler = PathHandler()
    id_handler = IdHandler()
    formatter = Formatter()

    member_ids = id_handler.getIds(path_handler.MEMBERS)

    bank_ext = ".bank"
    member_ext = ".member"

    member_data = {}
    treasury = {}

    def __init__(self):
        pass

    def idExists(self, generate, check, ids):
        checking = True

        while checking:
            if check in ids:
                check = self.id_handler.generateId(generate)
                print("exists")
            else:
                return check

    def hasMemberFile(self, target):
        member_files = os.listdir(self.path_handler.MEMBERS)

        for file in member_files:
            temp_file = open(self.path_handler.MEMBERS + file, "r")
            lines = temp_file.readlines()

            for line in lines:
                if target in line:
                    print("True")
                    return True
                else:
                    print("False")
                    return False

    def formatMemberData(self):
        pass
    def loadData(self):
        self.loadMemberData()
        self.loadTreasuryData()

        return {
            self.id_handler.MEMBER : self.member_data,
            self.id_handler.TREASURY : self.treasury
        }

    def loadMemberData(self):
        member_files = os.listdir(self.path_handler.MEMBERS)
        account_files = os.listdir(self.path_handler.ACCOUNTS)

        for file in member_files:
            member_file = open(self.path_handler.MEMBERS + file, "r")
            member_data = self.formatter.formatDefaultData(member_file)

            for act_file in account_files:
                check = act_file.split(".")[0]

                if member_data["Bank_Number"] == check:
                    account_file = open(self.path_handler.ACCOUNTS + act_file, "r")
                    bank_data = self.formatter.formatDefaultData(account_file)
                    bank_data["ActNumber"] = member_data["Bank_Number"]
                    member = Member(member_data, bank_data)
                    member.id = file.split(".")[0]

                    self.member_data[member.id] = member
                else:
                    pass

    def createMemberFile(self, member_details, pin):
        member_id = self.id_handler.generateId(self.id_handler.MEMBER)
        existent_member_ids = self.id_handler.getIds(self.path_handler.MEMBERS)

        good_member_id = self.idExists(self.id_handler.MEMBER, member_id, existent_member_ids)

        temp_file = open(self.path_handler.MEMBERS + f"{good_member_id}{self.member_ext}", "w")
        temp_file.write(f"Ign:{member_details[0]}\n")
        temp_file.write(f"Discord:{member_details[1]}\n")
        temp_file.write("\n")

        bank_id = self.id_handler.generateId(self.id_handler.TREASURY)
        existent_account_ids = self.id_handler.getIds(self.path_handler.ACCOUNTS)
        good_bank_id = self.idExists(self.id_handler.TREASURY, bank_id, existent_account_ids)

        temp_file.write(f"Bank_Number:{good_bank_id}")
        temp_file.close()

        self.createBankFile(good_bank_id, pin)

        new_member = Member({
                            "Ign":member_details[0],
                            "Discord":member_details[1]
                            },{
                                        "ActNumber":good_bank_id,
                                        "Pin":pin,
                                        "Balance":"500",
                                        "Frozen":"False"
                                        })
        self.member_data[new_member.id] = new_member

    def deleteMemberFile(self, member):
        member_file_path = f"{self.path_handler.MEMBERS}{member.id}{self.member_ext}"
        account_number = member.bank_account.account_number

        if os.path.exists(member_file_path):
            os.remove(member_file_path)
            self.deleteBankFile(account_number)


    def loadTreasuryData(self):
        file = open(self.path_handler.TREASURYFILE, "r")
        self.treasury = self.formatter.formatDefaultData(file)
        self.treasury["Accounts"] = self.loadBankAccounts()

        self.treasury = Bank(self.treasury)

    def loadBankAccounts(self):
        accounts = os.listdir(self.path_handler.ACCOUNTS)
        temp_dict = {}

        for account in accounts:
            account_id = account.split(".")[0]
            account_file = open(self.path_handler.ACCOUNTS + account, "r")
            account_details = self.formatter.formatDefaultData(account_file)
            account_details["ActNumber"] = account_id

            bank_account = BankAccount(account_details)
            temp_dict[account_id] = bank_account

        return temp_dict

    def createBankFile(self, bank_id, pin):
        temp_file = open(self.path_handler.ACCOUNTS + bank_id + self.bank_ext, "w")
        temp_file.write(f"Pin:{pin}\n")
        temp_file.write("\n")
        temp_file.write("Balance:500\n")
        temp_file.write("Frozen:False\n")
        temp_file.close()

    def saveBankFile(self, details):
        path = f"{self.path_handler.ACCOUNTS}{details[0]}{self.bank_ext}"

        temp_file = open(path, "w")
        temp_file.write(f"Pin:{details[1]}\n")
        temp_file.write("\n")
        temp_file.write(f"Balance:{details[2]}\n")
        temp_file.write(f"Frozen:{details[3]}\n")
        temp_file.close()

    def deleteBankFile(self, account_number):
        bank_account_path = self.path_handler.ACCOUNTS + account_number + self.bank_ext

        if os.path.exists(bank_account_path):
            os.remove(bank_account_path)
