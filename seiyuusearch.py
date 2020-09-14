# seiyuusearch.py
import os
from dotenv import load_dotenv
from discord.ext import commands
from jikanpy import Jikan

jikan = Jikan()
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# emojis 1 thru 10 that will be used to navigate search results, indexed from 0
emojis = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟']
# dictionary of category-specific search terms
categories = {'anime':'title', 'manga':'title', 'person':'name', 'character':'name'}

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# functions to make implementing future commands easier
async def pickresult(ctx, category, allresults, sender): # formats search results and sends them in a message
    # creates list of top ten search results to return to user
    results = allresults.get('results')
    index = 0
    resultstr = ""
    for result in results: # in case there are fewer than 10 results
        if index == 10:
            break
        index += 1
        resultstr += str(index) + ". " + result.get(categories.get(category)) + "\n"

    tosend = "**Here are the top " + str(index) + " search results:**\n" + resultstr + "\nPlease react with the emoji that corresponds to the " + category + " you'd like to learn more about."
    searchresults = await ctx.send(tosend) # searchresults is of type Message
    
    for x in range(index): # adds emojis 1-10 to the search results message
        await searchresults.add_reaction(emojis[x])

    def check(reaction, user): # checks to see if the person who send the command reacted with one of the emojis 1-10
        return (str(reaction.emoji) in emojis) and (emojis.index(str(reaction.emoji)) < index) and (user == sender)

    reaction, user = await bot.wait_for('reaction_add', check = check)
    #await ctx.send(str(user) + " reacted with " + str(reaction.emoji)) # test to make sure it's getting the right reaction
    return reaction

def shortenresults(category, allresults): # creates array of results with title and mal_id only
    shortresults = []

    results = allresults.get("results")
    for result in results:
        curr = {"mal_id": result.get("mal_id"), categories.get(category): result.get(categories.get(category))}
        shortresults.append(curr)
    
    return shortresults

# changes the bot command prefix
@bot.command(name='prefix', help='Changes the bot\'s prefix to a specified single character')
@commands.has_guild_permissions(administrator=True)
async def prefix(ctx, prefix):
    if len(prefix) != 1:
        await ctx.send('Please choose a single character as the new prefix.')
        return
    global bot
    old_prefix = ctx.prefix
    bot.command_prefix = prefix
    await ctx.send("Bot prefix has been changed from `" + old_prefix + "` to `" + prefix + "`")

# user searches for a series, then bot returns the seiyuus for the characters in that series
@bot.command(name='anime', help='Look up the Japanese and English seiyuus in a certain anime on MAL', aliases=['show', 'series'])
async def anime_search(ctx, query):
    sender = ctx.message.author
    results = jikan.search('anime', query) #TODO: add parameters to limit search results to 10 # searches with the user's query
    shortresults = shortenresults('anime', results)
    reaction = await pickresult(ctx, 'anime', results, sender)

    mal_id = shortresults[emojis.index(str(reaction.emoji))].get('mal_id')
    animeinfo = jikan.anime(mal_id, extension='characters_staff')

    # list out jp and eng seiyuus for all chars
    allchars = animeinfo.get("characters")
    formattedchars = ""
    for char in allchars:
        charname = char.get("name")
        role = char.get("role")
        seiyuus = ""
        for va in char.get("voice_actors"):
            if va.get('language') == 'English' or 'Japanese':
                if seiyuus != "":
                    seiyuus += "; "
                name = va.get("name")
                lang = va.get("language")
                seiyuus += name + " (" + lang + ")"

            formattedchars += "     - " + charname + " (" + role + "): " + seiyuus + "\n"
    
    tosend = "**Here are the English and Japanese seiyuus for " + shortresults[emojis.index(str(reaction.emoji))].get(categories.get('anime')) + ":**\n" + formattedchars
    await ctx.send(tosend)

# user searches for a seiyuu, then bot returns their 20 most recent roles
@bot.command(name='va', help='Look up the roles of a certain seiyuu on MAL', aliases=['seiyuu'])
async def va_search(ctx, query, series_prefix = ''):
    sender = ctx.message.author
    results = jikan.search('person', query) #TODO: add parameters to limit search results to 10 # searches with the user's query
    shortresults = shortenresults('person', results)
    reaction = await pickresult(ctx, 'person', results, sender)

    mal_id = shortresults[emojis.index(str(reaction.emoji))].get('mal_id')
    personinfo = jikan.person(mal_id)

    #TODO: format personinfo and send with ctx
    jobs = personinfo.get('voice_acting_roles')
    index = 0
    formatted = ""    
    for job in jobs:
        if index == 20:
            break
        anime = job.get('anime').get('name')
        char = job.get('character').get('name')
        role = job.get('role')
        if (anime.lower()).startswith(series_prefix):
            formatted += "     - " + char + " (" + role + ") in *" + anime + "*\n"
            index += 1
    
    if series_prefix == '':
        tosend = "**Here are " + shortresults[emojis.index(str(reaction.emoji))].get(categories.get('person')) + "'s first " + str(index) + " roles in alphabetical order:**\n" + formatted
    else:
        tosend = "**Here are " + shortresults[emojis.index(str(reaction.emoji))].get(categories.get('person')) + "'s first " + str(index) + " roles that start with " + series_prefix.capitalize() + ":**\n" + formatted
    await ctx.send(tosend)

# user searches for a character, then bot returns their vas
@bot.command(name='char', help='Look up the seiyuus for a certain character on MAL', aliases=['character'])
async def char_search(ctx, query):
    sender = ctx.message.author
    results = jikan.search('character', query) #TODO: add parameters to limit search results to 10 # searches with the user's query
    shortresults = shortenresults('character', results)
    reaction = await pickresult(ctx, 'character', results, sender)

    mal_id = shortresults[emojis.index(str(reaction.emoji))].get('mal_id')
    charinfo = jikan.character(mal_id)

    #TODO: format charinfo and send with ctx
    vas = charinfo.get("voice_actors")
    seiyuus = ""
    for va in vas:
        name = va.get("name")
        lang = va.get("language")
        seiyuus += "     - " + name + " (" + lang + ")\n"
    
    tosend = "**Here are the seiyuus for " + shortresults[emojis.index(str(reaction.emoji))].get(categories.get('character')) + ":**\n" + seiyuus
    await ctx.send(tosend)

# error messages
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument) and (ctx.command.name == 'prefix'):
        await ctx.send('Please specify a new prefix.')
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send('Please specify a search query.')

    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct permissions for this command.')

bot.run(TOKEN)