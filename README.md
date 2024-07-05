# Venezuela.Gov (NG Discord Bot) ![](https://github.com/Galaxy-Studios-Dev/Venezuela.gov/blob/main/venz_gov.png)

# Commands
## Key
```diff
 "aliases=" : This is the shortened version of the command, You may type this instead of the full thing! Ex. instead of using !treasury we can use !t same with country, We can use c making the command !t c instead of !treasury country!

 "sub_commands=" : This is all the arguements that can be provided to do seperate things. Ex. !membership view ids will return a Discord Embed containing a list of ids of all the members. These Ids are used to gather data from files. As where !membership view members shows a Discord Embed containing a list of Member names (Generally IGNames)

 "target=" : This is generally the discord name of whomever you want the command to be ran on!

 "*details" : This stands for multiple arguements to give, Make sure you take a look at the format in the bot to match up the details, If you need any help ask! Ex. !membership update [*details] would look like !membership update [ign=blah] [target=discord_name]

 "[]" : Anything in brackets is meant to be changed with whatever data you are providing! Ex. !treasury freeze kwstasgamer55 or !membership register test_ign test_discord
```

## Membership Commands 
### aliases = "mbrs"
```diff
 !membership view(sub_commands=["ids", "members"]) # NOTE: Leadership Roles, Display the saved ids : All members in Country.
 !membership register(aliases=["r"]) [arg1=ign] [arg2=discord_name] # NOTE: Leadership Roles, Registers a new save file for data and bank account for given member!
 !membership unregister(aliases=["ur"]) [target=discord_name] # NOTE: Leadership Roles
 !membership update(aliases="u") [target=discord_name] [*details_to_change] # NOTE: Leadership Roles
```

## Treasury Commands 
### aliases = "t"

```diff
 !treasury account(aliases=["act"]) # NOTE: All Roles
 !treasury country(aliases=["c"]) # NOTE: All Roles
 !treasury pay [amount] [target=discord_name] # NOTE: All Roles
 !treasury freeze [target=discord_name] # NOTE: PRESIDENT, VP and HEAD_TREASURER Roles
```
