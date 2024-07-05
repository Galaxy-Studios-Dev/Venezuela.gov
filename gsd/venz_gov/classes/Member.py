from gsd.venz_gov.classes.banking.BankAccount import BankAccount


class Member:
    id = ""

    ign = ""
    discord_name = ""

    bank_account = ""

    def __init__(self, details, bank_details):
        self.ign = details["Ign"]
        self.discord_name = details["Discord"]
        self.bank_account = BankAccount(bank_details)
