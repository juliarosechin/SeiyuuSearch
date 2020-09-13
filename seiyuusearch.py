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

# functions to make implementing future commands easier
async def pickresult(ctx, category, results, sender): # formats search results and sends them in a message
    categories = ['anime', 'manga', 'person', 'character']
    

    if category == categories[0]:
        # creates list of top ten search results to return to user
        animes = results.get('results')
        index = 0
        resultstr = ""
        for anime in animes: # in case there are fewer than 10 results
            if index == 10:
                break
            index += 1
            resultstr += str(index) + ". " + anime.get("title") + "\n"

    tosend = "**Here are the top " + str(index) + " search results:**\n" + resultstr + "\nPlease react with the emoji that corresponds to the " + category + " you'd like to learn more about."
    searchresults = await ctx.send(tosend) # searchresults is of type Message
    
    for emoji in emojis: # adds emojis 1-10 to the search results message
        await searchresults.add_reaction(emoji)

    def check(reaction, user): # checks to see if the person who send the command reacted with one of the emojis 1-10
        return (str(reaction.emoji) in emojis) and (user == sender)

    reaction, user = await bot.wait_for('reaction_add', check = check)
    #await ctx.send(str(user) + " reacted with " + str(reaction.emoji)) # test to make sure it's getting the right reaction
    return reaction

def shortenresults(category, results): # creates array of results with title and mal_id only
    categories = ['anime', 'manga', 'person', 'character']
    shortresults = []
    
    if category == categories[0]:
        animes = results.get("results")
        for a in animes:
            anime = {"mal_id": a.get("mal_id"), "title": a.get("title")}
            shortresults.append(anime)
    
    return shortresults
        

# changes the bot command prefix
@bot.command(name='prefix', help='Changes the bot\'s prefix to a different single character.')
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
@bot.command(name='anime', help='Look up the seiyuus in a certain anime.')
async def anime_search(ctx, query):
    sender = ctx.message.author
    results = jikan.search('anime', query) #TODO: add parameters to limit search results to 10 # searches with the user's query
    #pprint.pprint(results)
    shortresults = shortenresults('anime', results)
    reaction = await pickresult(ctx, 'anime', results, sender)

    mal_id = shortresults[emojis.index(str(reaction.emoji))].get('mal_id')
    animeinfo = jikan.anime(mal_id, extension='characters_staff')
    #pprint.pprint(animeinfo)

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
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct permissions for this command.')

bot.run(TOKEN)