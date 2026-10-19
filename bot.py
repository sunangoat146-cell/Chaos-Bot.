
import os
import discord
from discord import app_commands

TOKEN = os.environ["DISCORD_TOKEN"]

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@tree.command(name="repeat", description="Repite un mensaje una cantidad limitada de veces")
@app_commands.describe(
    mensaje="Texto que quieres enviar",
    cantidad="Número de repeticiones (máximo 5)"
)
async def repeat(
    interaction: discord.Interaction,
    mensaje: str,
    cantidad: app_commands.Range[int, 1, 5]
):
    await interaction.response.defer(ephemeral=True)

    canal = interaction.channel
    if canal is None:
        await interaction.followup.send("No encuentro el canal.", ephemeral=True)
        return

    enviados = 0
    for _ in range(cantidad):
        try:
            await canal.send(mensaje, allowed_mentions=discord.AllowedMentions.none())
            enviados += 1
        except discord.HTTPException:
            break

    await interaction.followup.send(
        f"Listo: enviados {enviados} mensajes.",
        ephemeral=True
    )


@tree.command(name="help", description="Muestra los comandos disponibles")
async def help_command(interaction: discord.Interaction):
    await interaction.response.send_message(
        "Comandos disponibles: /repeat y /help. "
        "/repeat permite de 1 a 5 mensajes y no activa menciones.",
        ephemeral=True
    )


@client.event
async def on_ready():
    await tree.sync()
    print(f"Conectado como {client.user}")


client.run(TOKEN)
