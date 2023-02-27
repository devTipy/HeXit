from discord.ext import commands
from discord import app_commands
from utils import (
    generate_image,
    generate_image_online,
    cleanup_output_files
)


class Features(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def check(channel):
        return True
    
    # Use a message command for syncing because syncing anywhere else is usually a bad idea.
    @commands.command()
    async def sync(self, ctx):
        await self.bot.tree.sync()
        await ctx.send("Synced commands.")

    @app_commands.command()
    async def render(self, interaction, latex: str):
        if not check(interaction.channel):
            return
        
        self.bot.vprint("Latex:", latex)

        num = str(random.randint(0, 2**31))

        if self.bot.settings["renderer"] == "external":
            fn = generate_image_online(latex)
        elif self.bot.settings["renderer"] == "local":
            fn = generate_image(latex, num)

        if fn and os.path.getsize(fn) > 0:
            await interaction.response.send_message(file=discord.File(fn))
            cleanup_output_files(num)
            self.bot.vprint("Success!")
        else:
            await interaction.response.send_message(
                "Something broke. Check the syntax of your message. :frowning:",
                ephemeral=True
            )
            cleanup_output_files(num)
            self.bot.vprint("Failure.")
        await interaction.response.send_message()


async def setup(bot):
    await bot.add_cog(Features(bot))
