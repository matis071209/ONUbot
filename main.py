import discord
import random
import wavelink
from easy_pil import Editor,load_image_async, Font
from discord.ext import commands
bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Yo soy {bot.user}')
    bot.loop.create_task(on_node())
async def on_node():
    
    node: wavelink.Node=wavelink.Node(uri="https://lavalink.lexnet.cc:", password="lexn3tl@val!nk", secure=True)
    await wavelink.NodePool.connect(client=bot, nodes=[node])
    wavelink.Player.autoplay= True

@bot.tree.command(description="embed de prueba")
async def embed(interaction: discord.Interaction):
    embed=discord.Embed(title="Embed", description="embed de prueba", color=discord.Color.blurple())
    embed.add_field(name="esto es un field", value="a", inline=True)
    embed.add_field(name="esto es otro field",value="a", inline=False)
    embed.set_image(url="https://cdn.discordapp.com/app-icons/1086735812474982512/1dd5d65e2df0dcac07229b216e3a6a75.png?size=256")

    await interaction.response.send_message(embed=embed)

@bot.tree.command(description="Reproduce una cancion")
async def play(interaction: discord.Interaction, search:str):
    query = await wavelink.YouTubeTrack.search(search, return_first=True)
    destination = interaction.user.voice.channel

    if not interaction.guild.voice_client:
        vc: wavelink.Player = await destination.connect(cls=wavelink.Player)

    else:
        vc: wavelink.Player = interaction.guild.voice_client

    if vc.queue.is_empty and not vc.is_playing():
        await vc.play(query)
        embed=discord.Embed(title="Play🔊", color=discord.Color.blurple())
        embed.add_field(name="Play",value=f'Ahora reproduciendo {vc.current.title}')
        await interaction.response.send_message(embed=embed)
    else: 
        await vc.queue.put_wait(query)
        await interaction.response.send_message('La cancion fue añadida')


@bot.tree.command(description='Skipea a la siguiente cancion')
async def skip(interaction:discord.Interaction):
    vc: wavelink.Player = interaction.guild.voice_client
    embed=discord.Embed(title="Skip🔊", color=discord.Color.blurple())
    embed.add_field(name="skip",value='La cancion fue skipeada')
    await interaction.response.send_message(embed=embed)
    await vc.stop()


@bot.tree.command(description='Pausa la cancion')
async def pause(interaction: discord.Interaction):
    vc: wavelink.Player = interaction.guild.voice_client

    if vc.is_playing():
        await vc.pause()
        embed=discord.Embed(title="Pause🔊", color=discord.Color.blurple())
        embed.add_field(name="pause",value='La cancion fue pausada')
        await interaction.response.send_message(embed=embed)
    else:
        embed=discord.Embed(title="Pause🔊", color=discord.Color.blurple())
        embed.add_field(name="pause",value='La cancion fue pausada')
        await interaction.response.send_message(embed=embed)

@bot.tree.command(description="cuanto mide la banana de un usuario")
async def banana(interaction:discord.Interaction, member:discord.Member=None):
    if member == None:
        member = interaction.user

    porcentaje= random.randrange(start=1, stop=50,step=1)

    embed=discord.Embed(title="Banana", color=discord.Color.blurple())
    embed.add_field(name="Medicion", value=f"La banana de {member.mention} mide {porcentaje}cm")
    embed.set_image(url="https://images.emojiterra.com/google/android-12l/512px/1f34c.png")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(description="Cuanto es tu porcentaje de homosexualidad")
async def howgay(interaction: discord.Interaction, member:discord.Member=None):
    if member==None:
        member=interaction.user

    porcentaje= random.randrange(start=0,stop=100,step=1)

    if porcentaje > 0:
        embed=discord.Embed(title="Gay", description="Cuanto es tu porcentaje de homosexualidad", color=discord.Color.blurple())
        embed.add_field(name="porcentaje", value=f"{member.mention} Eres {porcentaje}% Gay 🤨🏳️‍🌈")
        await interaction.response.send_message(embed=embed)

    else:
        embed=discord.Embed(title="Gay", description="Cuanto es tu porcentaje de homosexualidad", color=discord.Color.blurple())
        embed.add_field(name="porcentaje", value=f"{member.mention} Felicidades, no eres gay! 😄")
        await interaction.response.send_message(embed=embed)

@bot.tree.command(description='Vuelve a reproducir la cancion')
async def resume(interaction: discord.Interaction):
    vc: wavelink.Player = interaction.guild.voice_client

    if vc.is_playing():
        await interaction.response.send_message('La cancion esta reproduciendose')
        await vc.resume()
    else:
        await interaction.response.send_message('La cancion se va a reanudar')
        await vc.resume()

@bot.tree.command(description='Desconecta al bot')
async def disconnect(interaction: discord.Interaction):
    vc: wavelink.Player = interaction.guild.voice_client

    if vc.is_playing():
        await vc.disconnect()
        await interaction.response.send_message('Ya se desconecto el bot')

    else:
        await interaction.response.send_message('El bot ya esta desconectado')
        await vc.disconnect
@bot.command()
async def ping(ctx):
    await ctx.send("pong!")

@bot.tree.command(description='Bloquea el acceso a los canales')
@commands.has_permissions(manage_channels=True)
async def lock(interaction:discord.Interaction, channel:discord.TextChannel=None):
    if channel ==None:
        channel= interaction.channel
    await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=False)
    await interaction.response.send_message(f"El canal {channel} ha sido bloqueado correctamente")


@bot.tree.command(description='vea el avatar de una persona')
async def avatar(interaction:discord.Interaction, member:discord.Member=None):
    if member == None:
        member = interaction.user
    await interaction.response.send_message(f'El avatar de {member.mention} es este: {member.avatar}')

@bot.tree.command(description='desbloquea el acceso a un canal')
@commands.has_permissions(manage_channels=True)
async def unlock(interaction:discord.Interaction, channel:discord.TextChannel=None):
    if channel == None:
        channel = interaction.channel
    await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=True)
    await interaction.response.send_message(f"El canal {channel} ha sido desbloqueado correctamente")

@bot.tree.command(name='ping', description='te responde con pong')
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong!")

@bot.tree.command(name='prueba', description='prueba')
async def prueba(interactions: discord.Interaction):
    await interactions.response.send_message('prueba 123')
@bot.tree.command(description='te remea')
async def echo(interaction: discord.Interaction, input: str):
    await interaction.response.send_message(f'{input}')
@bot.tree.command(description='kickea')
@commands.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, miembro:discord.Member, razon:str=None):
    if razon == None:
        razon = 'sin razon definida'
    await interaction.guild.kick(miembro)
    await interaction.response.send_message(f'Has kickeado al usuario {miembro} por la siguiente razon: {razon}')

@bot.tree.command(description='banea')
@commands.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, miembro:discord.Member, razon:str=None):
    if razon == None:
        razon = 'sin razon definida'
    await interaction.guild.ban(miembro)
    await interaction.response.send_message(f'Has baneado al miembro {miembro} por la siguiente razon: {razon}')

@bot.tree.command(description='desbanea')
@commands.has_permissions(ban_members=True)
async def unban(interaction: discord.Interaction, miembro: discord.User):
    await interaction.guild.unban(miembro)
    await interaction.response.send_message(f'Has desbaneado a {miembro} satisfactoriamente')

@bot.tree.command(description='elimina texto')
@commands.has_permissions(manage_channels=True)
async def purge(interaction: discord.Interaction, cantidad:int):
    await interaction.channel.purge(limit=cantidad)
@bot.command()
async def echo(ctx, *args):
    arguments = " ".join(args)
    await ctx.send(f'{arguments}')
@bot.command()
async def sincronizar(ctx):
    await bot.tree.sync()
    await ctx.send("listo")

bot.run('MTA4NjczNTgxMjQ3NDk4MjUxMg.GPfIcx.FjGILtwBf6vUmTUTVvPw56j8TW_tXY16PXCxfg')    