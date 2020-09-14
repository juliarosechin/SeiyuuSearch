# SeiyuuSearch
 
#### Noun. seiyuu (plural seiyuu or seiyuus) A voice actor in a native-language version anime, a video game, a radio broadcast or an advertisement in Japan.

SeiyuuSearch is a Discord bot that gets information on seiyuus in anime. It gets all of its information from [MyAnimeList](http://myanimelist.net/).

[Add the bot](https://discord.com/api/oauth2/authorize?client_id=754163844699390093&permissions=8&scope=bot) to your Discord server!

## Installation

Here's what you can do if you'd like to run your own instance of SeiyuuSearch:

1. Clone the repo to your computer.
    ```shell
    $ git clone https://github.com/juliarosechin/SeiyuuSearch.git
    $ cd SeiyuuSearch
    ```
2. Install the required dependencies with pip.
    ```shell
    pip install -r requirements.txt
    ```
3. Get a Discord bot token from making a Bot User. [This tutorial](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token) should help.
4.  Create a file called `.env` in the repo directory.
5. Copy/paste the below into the file.
    ```ini
    DISCORD_TOKEN=your-bot-token
    ```
6. Put your tokens and key where it says to in the config. Do not put quotes around the tokens.
7. Run the bot.
    ```shell
    $ python seiyuusearch.py
    ```

## Commands

Do `!help` to get a list of commands from the bot.

The bot's default prefix is `!`, but this can be changed with the `!prefix` command if you have the Administrator permission on your Discord server.

| Command | Description | Usage |
| --- | --- | --- |
| anime, show, or series | Look up the Japanese and English seiyuus in a certain anime on MAL. | !anime `<query>` |
| char | Look up the seiyuus for a certain character on MAL. | !char `<query>` |
| va or seiyuu | Look up the roles of a certain seiyuu on MAL. Limited to showing the 20 first roles alphabetically, but you can use the third parameter to filter results to series that start with a certain prefix. | !va `<query> [series_prefix]` |
| prefix | Change the bot prefix to a different single character. Must have the Administrator permission to use. | !prefix `<prefix>` |


## Contributing
Contributions are greatly appreciated!

```shell
# 1. Fork the bot and clone it to your computer
$ git clone https://github.com/your-username/SeiyuuSearch.git
$ cd SeiyuuSearch

# 2. Connect your fork with this repo to stay up to date on any changes
$ git remote add upstream https://github.com/juliarosechin/SeiyuuSearch.git

# 3. Make your feature branch
$ git checkout -b new-feature

# 4. Add and commit the changes you made
$ git add .
$ git commit -m "Added new feature"

# 5. Push to your branch
$ git push origin new-feature

# 6. Create a pull request on GitHub
```

Alternatively, feel free to open an issue.


## Potential Features

- Make `help` command look nicer
- Have bot responses use embeds
- Let user go to different pages of search results


## Dependencies

Powered by [discord.py](https://github.com/Rapptz/discord.py) and [JikanPy](https://github.com/abhinavk99/jikanpy).
