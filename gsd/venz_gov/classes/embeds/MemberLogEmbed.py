import datetime

import discord

class MemberLogEmbed:
    embed = ""

    def __init__(self, log_type, details):
        if log_type == "r":
            self.embed = discord.Embed()
            self.embed.title = "Venezuela Registration Office"

            self.newMemberFields(details)
        elif log_type == "ur":
            self.embed = discord.Embed()
            self.embed.title = "Venezuela Registration Office"

            self.unregisterFields(details)
        elif log_type == "u":
            pass

    def newMemberFields(self, details):
        date_time = datetime.datetime.now()
        self.embed.add_field(name="Type", value="Register\n", inline=True)
        self.embed.add_field(name="Ign", value=details[0] + "\n", inline=True)
        self.embed.add_field(name="Discord_Name", value=details[1] + "\n", inline=True)
        self.embed.add_field(name="Date", value=date_time.date(), inline=True)

    def unregisterFields(self, details):
        date_time = datetime.datetime.now()
        self.embed.add_field(name="Type", value="Unregister\n", inline=True)
        self.embed.add_field(name="Discord_Name", value=details[0] + "\n", inline=True)
        self.embed.add_field(name="Reason", value=details[1] + "\n", inline=True)
        self.embed.add_field(name="Date", value=date_time.date(), inline=True)

    def updateFields(self):
        pass