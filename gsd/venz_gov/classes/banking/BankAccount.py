
class BankAccount:
    account_number = ""
    pin = ""

    balance = 0

    frozen = False

    def __init__(self, data):
        self.account_number = data["ActNumber"]
        self.pin = data["Pin"]
        self.balance = data["Balance"]
        self.frozen = data["Frozen"]
