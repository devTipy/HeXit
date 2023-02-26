from discord.ext import commands
import discord
import aiohttp
import random
import os
import json
import shutil

LATEX_TEMPLATE = "template.tex"

HELP_MESSAGE = r"""
Hello! I"m the *HeXit* mathematics bot!

You can type mathematical *LaTeX* into the chat and I"ll automatically render it!
Simply use the `!tex` command.

**Examples**
`!tex x = 7`
`!tex \sqrt{a^2 + b^2} = c`
`!tex \int_0^{2\pi} \sin{(4\theta)} \mathrm{d}\theta`

**Notes**
Using the `\begin` or `\end` in the *LaTeX* will probably result in something failing.

"""

# Not actually necessary since we can just use discord.Client but the
# "commands" extension supports cogs which helps with structuring the bot.
class LatexBot(commands.Bot):
    def __init__(self):
        super().__init__(
            intents=discord.Intents.default(),
            command_prefix=commands.when_mentioned
        )

        if not os.path.isfile("settings.json"):
            shutil.copyfile("settings_default.json", "settings.json")
            print("Now you can go and edit `settings.json`.")
            print("See README.md for more information on these settings.")

        with open("settings.json") as settings_file:
            self.settings = json.load(settings_file)

        if "latex" not in self.settings:
            self.settings["latex"] = {
                "background-colour": "36393E",
                "text-colour": "DBDBDB",
                "dpi": "200",
            }

    async def setup_hook(self):
        self.http_session = aiohttp.ClientSession()
        await self.load_extension("features")

    async def on_ready(self):
        print(f"Logged in as {self.user.name}")

    async def close(self):
        if hasattr(self, "http_session"):
            await self.http_session.close()

        await super().close()

    def vprint(self, *args, **kwargs):
        if self.settings.get("verbose"):
            print(*args, **kwargs)


def main():
    bot = LatexBot()
    bot.run(bot.settings["token"])


if __name__ == "__main__":
    main()
