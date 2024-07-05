import discord

class AccountEmbed:
    embed = discord.Embed()

    def __init__(self, bank, bank_account):
        self.embed.title = bank.name
        self.embed.set_thumbnail(url="attachment://bank_thumbnail.png")
        self.embed.add_field(name="Account Number", value=bank_account.account_number)
        self.embed.add_field(name="Pin", value=bank_account.pin)
        self.embed.add_field(name="", value="\n")
        self.embed.add_field(name="Balance", value=bank_account.balance)
        self.embed.add_field(name="", value="\n")
        self.embed.add_field(name="", value="\n")
        self.embed.add_field(name="Frozen", value=bank_account.frozen)