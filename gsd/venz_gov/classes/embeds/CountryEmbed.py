import discord

class CountryEmbed:
    embed = discord.Embed()

    def __init__(self, bank):
        self.embed.title = bank.name
        self.embed.set_thumbnail(url="attachment://bank_thumbnail.png")
        self.embed.set_image(url="")
        self.embed.add_field(name="Current Funds", value=bank.current_funds, inline=True)
        self.embed.add_field(name="Available Funds", value=bank.available_funds, inline=True)
        self.embed.add_field(name="Unavailable Funds", value=bank.unavailable_funds, inline=True)
