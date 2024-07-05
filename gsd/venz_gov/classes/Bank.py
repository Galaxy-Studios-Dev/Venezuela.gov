

class Bank:
    name = "Bank of Venezuela"
    current_funds = 0
    available_funds = 0
    unavailable_funds = 0

    accounts = {}

    def __init__(self, data):
        self.current_funds = data["Current_Funds"]
        self.available_funds = data["Available_Funds"]
        self.unavailable_funds = data["Unavailable_Funds"]
        self.accounts = data["Accounts"]
