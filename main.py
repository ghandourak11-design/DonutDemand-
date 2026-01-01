
import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
import pytz

TOKEN = "SIGMA"

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

timezones = {}

@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Bot is online")

@bot.tree.command(name="set", description="Set your timezone")
async def set_timezone(interaction: discord.Interaction, timezone: str):
    if timezone not in pytz.all_timezones:
        await interaction.response.send_message(
            "❌ Invalid timezone. Example: `US/Eastern`",
            ephemeral=True
        )
        return

    timezones[interaction.user.id] = timezone
    await interaction.response.send_message(
        f"✅ Timezone set to **{timezone}**",
        ephemeral=True
    )

@bot.tree.command(name="time", description="See someone else's time")
async def get_time(interaction: discord.Interaction, user: discord.User):
    if user.id not in timezones:
        await interaction.response.send_message(
            "❌ That user has not set a timezone.",
            ephemeral=True
        )
        return

    tz = pytz.timezone(timezones[user.id])
    now = datetime.now(tz).strftime("%I:%M %p")

    await interaction.response.send_message(
        f"🕒 **{user.name}**'s time: **{now}** ({timezones[user.id]})"
    )

bot.run(TOKEN)

