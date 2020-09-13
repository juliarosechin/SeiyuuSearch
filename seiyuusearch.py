# seiyuusearch.py
import os
import pprint
from dotenv import load_dotenv
from discord.ext import commands
from jikanpy import Jikan

jikan = Jikan()
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# emojis 1 thru 10 that will be used to navigate search results, indexed from 0
emojis = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟']

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# user searches for a series, then bot returns the seiyuus for the characters in that series
@bot.command(name='anime', help='Look up the seiyuus in a certain anime.')
async def anime_search(ctx, query):
    # searches with the user's query
    results = jikan.search('anime', query)
    # pprint.pprint(results)

    # creates array of results with title and mal_id only
    shortresults = []
    animes = results.get("results")
    for a in animes:
        anime = {"mal_id": a.get("mal_id"), "title": a.get("title")}
        shortresults.append(anime)
    
    # creates list of top ten search results to return to user
    index = 0
    resultstr = ""
    for result in shortresults: # in case there are fewer than 10 results
        if index == 10:
            break
        index += 1
        resultstr += str(index) + ". " + result.get("title") + "\n"

    tosend = "**Here are the top " + str(index) + " search results:**\n" + resultstr + "\nPlease react with the emoji that corresponds to the series you'd like to learn more about."
    searchresults = await ctx.send(tosend) # searchresults is of type Message

    for emoji in emojis: # adds emojis 1-10 to the search results message
        await searchresults.add_reaction(emoji)

    def check(reaction, user): # checks to see if the user reacted with one of the emojis 1-10
        return (str(reaction.emoji) in emojis) and (user != searchresults.author)

    reaction, user = await bot.wait_for('reaction_add', check = check)
    #await ctx.send(str(user) + " reacted with " + str(reaction.emoji)) # test to make sure it's getting the right reaction
    mal_id = shortresults[emojis.index(str(reaction.emoji))].get('mal_id')
    animeinfo = jikan.anime(mal_id, extension='characters_staff')
    pprint.pprint(animeinfo)

    # list out all seiyuus
    allchars = animeinfo.get("characters")
    formattedchars = ""
    for char in allchars:
        charname = char.get("name")
        role = char.get("role")
        seiyuus = ""
        for va in char.get("voice_actors"):
            if seiyuus != "":
                seiyuus += ", "
            name = va.get("name")
            lang = va.get("language")
            seiyuus += name + " (" + lang + ")"
        formattedchars += "     - " + charname + " (" + role + "): " + seiyuus + "\n"
    
    tosend = "**Here are the seiyuus for " + shortresults[emojis.index(str(reaction.emoji))].get("title") + ":**\n" + formattedchars
    await ctx.send(tosend)
    
# error messages
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send('Please specify a search query.')

bot.run(TOKEN)