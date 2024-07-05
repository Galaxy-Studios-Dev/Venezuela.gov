import random

# noinspection PyInterpreter
import settings
import discord

from discord.ext import commands

from gsd.venz_gov.classes.embeds.AccountEmbed import AccountEmbed
from gsd.venz_gov.classes.embeds.CountryEmbed import CountryEmbed
from gsd.venz_gov.classes.embeds.MemberLogEmbed import MemberLogEmbed
from gsd.venz_gov.utils.DiscordInfo import RoleIds, ChannelIds
from gsd.venz_gov.utils.FileHandler import FileHandler
from gsd.venz_gov.utils.MiscMethods import validTarget

file_handler = FileHandler()
discord_roles = RoleIds()
channel_ids = ChannelIds()

class VenezuelaGov:
    guild = ""

    data = {} # Temporary : Will be reassigned at initiation
    member_data = {}
    bank = "" # Temporary : Will be reassigned at initiation

    file_handler = file_handler
    path_handler = file_handler.path_handler
    id_handler = file_handler.id_handler
    formatter = file_handler.formatter

    member_ids = id_handler.getIds(path_handler.MEMBERS)

    def __init__(self, loaded_data):
        self.data = loaded_data

        self.member_data = self.data[self.id_handler.MEMBER]
        self.bank = self.data[self.id_handler.TREASURY]

    def run(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        bot = commands.Bot(command_prefix="!", intents=intents)

        self.guild = bot.get_guild(1224539944803110963)

        @bot.event
        async def on_ready():
            print("Started up!")

        @bot.command(
            aliases=["mbrs"]
        )
        async def membership(ctx, *args):
            leader_role = ctx.author.guild.get_role(discord_roles.PRESIDENT)
            citizen_role = ctx.author.guild.get_role(discord_roles.CITIZEN)

            members_reports = ctx.author.guild.get_channel(channel_ids.MEMBERSHIPLOG)

            if leader_role in ctx.author.roles:
                if args[0] == "view":
                    if args[1] == "ids":
                        dm_channel = await ctx.author.create_dm()

                        ids = self.id_handler.getIds(self.path_handler.MEMBERS)
                        await dm_channel.send(self.formatter.formatIds(ids))
                    elif args[1] == "members":
                        target = args[2]

                        ids = self.id_handler.getIds(self.path_handler.MEMBERS)

                        for id in ids:
                            if target == self.member_data[id].ign or target == self.member_data[id].discord or target == self.member_data[id].id:
                                print("Valid Target")
                            else:
                                print("Invalid Target")
                elif args[0] == "register" or args[0] == "r":
                    if ctx.author.name == args[2]:
                        pass
                    else:
                        if self.file_handler.hasMemberFile(args[2]):
                            await ctx.send(f"It seems that {args[2]} is already a registered member of Venezuela!")
                            return
                        else:
                            print("Creating new member file!")

                            details = (args[1], args[2])
                            pin = random.randint(1000, 9999)

                            log_embed = MemberLogEmbed("r", details)

                            async for member in ctx.author.guild.fetch_members():
                                if member.name == args[2]:
                                    self.file_handler.createMemberFile(details, pin)
                                    self.file_handler.loadMemberData()

                                    await member.add_roles(citizen_role)
                                    await members_reports.send(embed=log_embed.embed)
                                    return

                elif args[0] == "unregister" or args[0] == "ur":
                    for x in range(len(self.member_ids)):
                        print(self.member_ids[x])
                        if self.member_ids[x] == "":
                            pass
                        else:
                            current = self.member_ids[x]

                            current_member = self.member_data[current]

                            if ctx.author.name == self.member_data[current].discord_name:
                                pass
                            elif args[1] == current_member.id or args[1] == current_member.ign or current_member.discord_name:
                                log_embed = MemberLogEmbed("ur", (current_member.discord_name, args[2]))
                                async for member in ctx.author.guild.fetch_members():
                                    if member.name == args[1]:
                                        self.file_handler.deleteMemberFile(current_member)

                                        await member.remove_roles(citizen_role)
                                        await members_reports.send(embed=log_embed.embed)
                                        return

                elif args[0] == "update" or args[0] == "u":
                    pass
            else:
                pass

        @bot.command(
            aliases=["t"]
        )
        async def treasury(ctx, *args):
            president = ctx.author.guild.get_role(discord_roles.PRESIDENT)
            vice_president = ctx.author.guild.get_role(discord_roles.VP)
            treasury_dept = ctx.author.guild.get_role(discord_roles.TREASURER)

            citizen = ctx.author.guild.get_role(discord_roles.CITIZEN)

            if president in ctx.author.roles or vice_president in ctx.author.roles:
                if args[0] == "sieze":
                    pass
                elif args[0] == "freeze":
                    target = args[1]
                    report_channel = ctx.guild.get_channel(1252472884333379645)

                    for x in range(len(self.member_ids)):
                        if self.member_ids[x] == "":
                            pass
                        else:
                            current = self.member_ids[x]

                            if validTarget(current, ctx.author, self.member_data, target):
                                bank_account = self.member_data[current].bank_account

                                if bank_account.frozen == "True":
                                    bank_account.frozen = False

                                    account_details = (bank_account.account_number,
                                                       bank_account.pin,
                                                       bank_account.balance,
                                                       bank_account.frozen)
                                    self.file_handler.saveBankFile(account_details)
                                    await report_channel.send(f"Account owned by {self.member_data[current].discord_name} has been unfrozen!")
                                    return
                                elif bank_account.frozen == "False":
                                    bank_account.frozen = True

                                    account_details = (bank_account.account_number,
                                                           bank_account.pin,
                                                           bank_account.balance,
                                                           bank_account.frozen)
                                    self.file_handler.saveBankFile(account_details)
                                    await report_channel.send(f"Account owned by {self.member_data[current].discord_name} has been frozen!")
                                    return
                            else:
                                await ctx.send("I'm sorry but I'm afraid you can't target yourself with that command!")
                                return
                elif args[0] == "account" or args[0] == "act":
                    for value in self.member_data.values():
                        if ctx.author.name == value.discord_name.lower():
                            account_number = self.member_data[value.id].bank_account.account_number
                            bank_account = self.bank.accounts[account_number]

                            embed_image = discord.File(f"{self.path_handler.IMAGES}bank_thumbnail.png", filename="bank_thumbnail.png")

                            dm = await ctx.author.create_dm()

                            embed = AccountEmbed(self.bank, bank_account)

                            await dm.send(file=embed_image, embed=embed.embed)
                        else:
                            pass
                elif args[0] == "country" or args[0] == "c":
                    treasury_channel = ctx.guild.get_channel(1252456343445438499)

                    embed_image = discord.File(f"{self.path_handler.IMAGES}bank_thumbnail.png", filename="bank_thumbnail.png")
                    embed = CountryEmbed()

                    await treasury_channel.send(file=embed_image, embed=embed.embed)
            elif treasury_dept in ctx.author.roles:
                if args[0] == "freeze":
                    pass
            elif citizen in ctx.author.roles:
                if args[0] == "account" or args[0] == "act":
                    for x in range(len(self.member_ids)):
                        current = self.member_ids[x]

                        if current == "":
                            pass
                        else:
                            if ctx.author.name == self.member_data[current].discord_name:
                                bank_account = self.member_data[current].bank_account

                                embed_image = discord.File(f"{self.path_handler.IMAGES}bank_thumbnail.png", filename="bank_thumbnail.png")

                                dm = await ctx.author.create_dm()

                                embed = AccountEmbed(self.bank, bank_account)

                                await dm.send(file=embed_image, embed=embed.embed)
                elif args[0] == "country" or args[0] == "c":
                    treasury_channel = ctx.author.guild.get_channel(channel_ids.TREASURYLOG)

                    embed_image = discord.File(f"{self.path_handler.IMAGES}bank_thumbnail.png", filename="bank_thumbnail.png")
                    embed = CountryEmbed(self.bank)

                    await treasury_channel.send(file=embed_image, embed=embed.embed)
                elif args[0] == "pay":
                    sender = ctx.author
                    target = args[1]
                    amount = args[2]

                    for x in range(len(self.member_ids)):
                        if self.member_ids[x] == "":
                            pass
                        else:
                            current = self.member_ids[x]

                            if validTarget(current, sender, self.member_data, target):
                                target = self.member_data[current]
                                target.id = current

                                for y in range(len(self.member_ids)):
                                    if self.member_ids[y] == "":
                                        pass
                                    else:
                                        current = self.member_ids[y]

                                        if sender.name == self.member_data[current].discord_name:
                                            sender = self.member_data[current]
                                            print(f"Sender: {sender.discord_name}, Reciever: {target.discord_name}")

                                            sender_bank = sender.bank_account
                                            target_bank = target.bank_account

                                            sender_bank.balance = amount

                                            if sender_bank.balance >= amount:
                                                sender_bank.balance = int(sender_bank.balance) - int(amount)
                                                target_bank.balance = int(target_bank.balance) + int(amount)

                                                self.file_handler.saveBankFile((sender_bank.account_number,
                                                                                sender_bank.pin, sender_bank.balance,
                                                                                sender_bank.frozen))
                                                self.file_handler.saveBankFile((target_bank.account_number,
                                                                                target_bank.pin, target_bank.balance,
                                                                                target_bank.frozen))

                                                await ctx.send(f"Sender New Balance:{sender_bank.balance}, Target New Balance:{target_bank.balance}")
                                                return
                                            else:
                                                await ctx.send(f"You don't have enough funds to send {amount} to {target.discord_name}!")
                                                return

                            else:
                                await ctx.send("I'm sorry but I'm afraid you can't target yourself with that command!")
                                return


            else:
                pass

        bot.run(settings.DISCORD_API_SECRET)


if __name__ == "__main__":
    gov_bot = VenezuelaGov(file_handler.loadData())

    gov_bot.run()
