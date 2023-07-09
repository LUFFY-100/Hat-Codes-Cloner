import discord
import asyncio
import random
import requests
from colorama import Fore, init, Style


class Clone:
    @staticmethod
    async def roles_delete(guild_to: discord.Guild):
        for role in guild_to.roles:
            try:
                if role.name != "@everyone":
                    await role.delete()
                    print_delete(
                        f"The role {Fore.YELLOW}{role.name}{Fore.BLUE} has been deleted"
                    )
                    await asyncio.sleep(random.randint(0.15, 0.10))
            except discord.Forbidden:
                print_error(
                    f"Error deleting role: {Fore.YELLOW}{role.name}{Fore.RED} Insufficient permissions.{Fore.RESET}"
                )

            except discord.HTTPException as e:
                if e.status == 429:
                    print_warning(
                        f"Many requests were made. Waiting 60 seconds. Details: {e}"
                    )
                    await asyncio.sleep(60)

    @staticmethod
    async def roles_create(guild_to: discord.Guild, guild_from: discord.Guild):
        roles = []
        role: discord.Role
        for role in guild_from.roles:
            if role.name != "@everyone":
                roles.append(role)
        roles = roles[::-1]
        for role in roles:
            try:
                await guild_to.create_role(name=role.name,
                                           permissions=role.permissions,
                                           colour=role.colour,
                                           hoist=role.hoist,
                                           mentionable=role.mentionable)
                print_add(
                    f"O cargo {Fore.YELLOW}{role.name}{Fore.BLUE} Foi criado")
                await asyncio.sleep(random.uniform(0.3, 0.6))
            except discord.Forbidden:
                print_error(
                    f"Error creating role: {Fore.YELLOW}{role.name}{Fore.RED} Insufficient permissions.{Fore.RESET}"
                )
                await asyncio.sleep(random.randint(0.20, 0.40))
            except discord.HTTPException as e:
                if e.status == 429:
                    print_warning(
                        f"Many requests were made. Waiting 60 seconds. Details: {e}"
                    )
                    await asyncio.sleep(60)

    @staticmethod
    async def channels_delete(guild_to: discord.Guild):
        for channel in guild_to.channels:
            try:
                await channel.delete()
                print_delete(
                    f"The category {Fore.YELLOW}{channel.name}{Fore.BLUE} has been deleted"
                )
                await asyncio.sleep(0.6)
            except discord.Forbidden:
                print_error(
                    f"Error deleting category: {Fore.YELLOW}{channel.name}{Fore.RED} Insufficient permissions.{Fore.RESET}"
                )
                await asyncio.sleep(random.randint(2, 3))
            except discord.HTTPException as e:
                if e.status == 429:
                    print_warning(
                        f"Many requests were made. Waiting 60 seconds. Details: {e}"
                    )
                    await asyncio.sleep(60)
            except:
                print_error(
                    f"Unable to delete channel {Fore.YELLOW}{channel.name}{Fore.RED} Unidentified error"
                )
                await asyncio.sleep(random.randint(9, 12))

    @staticmethod
    async def categories_create(guild_to: discord.Guild,
                                guild_from: discord.Guild):
        channels = guild_from.categories
        channel: discord.CategoryChannel
        new_channel: discord.CategoryChannel
        for channel in channels:
            try:
                overwrites_to = {}
                for key, value in channel.overwrites.items():
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    overwrites_to[role] = value
                new_channel = await guild_to.create_category(
                    name=channel.name, overwrites=overwrites_to)
                await new_channel.edit(position=channel.position)
                print_add(
                    f"The category {Fore.YELLOW}{channel.name}{Fore.BLUE} has been created"
                )
                await asyncio.sleep(random.randint(1, 3))
            except discord.Forbidden:
                print_error(
                    f"Error creating category: {Fore.YELLOW}{channel.name}{Fore.RED} Insufficient permissions.{Fore.RESET}"
                )
                await asyncio.sleep(random.randint(2, 3))
            except discord.HTTPException as e:
                if e.status == 429:
                    print_warning(
                        f"Many requests were made. Waiting 60 seconds. Details: {e}"
                    )
                    await asyncio.sleep(60)
            except:
                print_error(
                    f"Unable to create category {Fore.YELLOW}{channel.name}{Fore.RED} Unidentified error"
                )
                await asyncio.sleep(random.randint(9, 12))

    @staticmethod
    async def channels_create(guild_to: discord.Guild,
                              guild_from: discord.Guild):
        channel_text: discord.TextChannel
        channel_voice: discord.VoiceChannel
        category = None
        for channel_text in guild_from.text_channels:
            try:
                for category in guild_to.categories:
                    try:
                        if category.name == channel_text.category.name:
                            break
                    except AttributeError:
                        category = None
                        break

                overwrites_to = {}
                for key, value in channel_text.overwrites.items():
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    overwrites_to[role] = value
                try:
                    new_channel = await guild_to.create_text_channel(
                        name=channel_text.name,
                        overwrites=overwrites_to,
                        position=channel_text.position,
                        topic=channel_text.topic,
                        slowmode_delay=channel_text.slowmode_delay,
                        nsfw=channel_text.nsfw)
                except:
                    new_channel = await guild_to.create_text_channel(
                        name=channel_text.name,
                        overwrites=overwrites_to,
                        position=channel_text.position)
                if category is not None:
                    await new_channel.edit(category=category)
                print_add(
                    f"The text channel {Fore.YELLOW}{channel_text.name}{Fore.BLUE} has been created"
                )
                await asyncio.sleep(0.59)
            except discord.Forbidden:
                print_error(
                    f"Error creating text channel: {channel_text.name}")
                await asyncio.sleep(random.randint(8, 10))
            except discord.HTTPException as e:
                if e.status == 429:
                    print_warning(
                        f"Many requests were made. Waiting 60 seconds. Details: {e}"
                    )
                    await asyncio.sleep(60)
                    new_channel = await guild_to.create_text_channel(
                        name=channel_text.name,
                        overwrites=overwrites_to,
                        position=channel_text.position)
                if category is not None:
                    await new_channel.edit(category=category)
                print_add(
                    f"The channel {Fore.YELLOW}{channel_text.name}{Fore.BLUE} has been created"
                )
            except:
                print_error(
                    f"Error creating text channel: {channel_text.name}")
                await asyncio.sleep(random.randint(9, 12))

        category = None
        for channel_voice in guild_from.voice_channels:
            try:
                for category in guild_to.categories:
                    try:
                        if category.name == channel_voice.category.name:
                            break
                    except AttributeError:
                        print_warning(
                            f"Voice channel {channel_voice.name} has no category!"
                        )
                        category = None
                        break

                overwrites_to = {}
                for key, value in channel_voice.overwrites.items():
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    overwrites_to[role] = value
                try:
                    new_channel = await guild_to.create_voice_channel(
                        name=channel_voice.name,
                        overwrites=overwrites_to,
                        position=channel_voice.position,
                        bitrate=channel_voice.bitrate,
                        user_limit=channel_voice.user_limit,
                    )
                except:
                    new_channel = await guild_to.create_voice_channel(
                        name=channel_voice.name,
                        overwrites=overwrites_to,
                        position=channel_voice.position)
                if category is not None:
                    await new_channel.edit(category=category)
                print_add(
                    f"The voice channel {Fore.YELLOW}{channel_voice.name}{Fore.BLUE} has been created"
                )
                await asyncio.sleep(0.48)
            except discord.Forbidden:
                print_error(
                    f"Error creating voice channel: {channel_voice.name}")
                await asyncio.sleep(random.randint(6, 7))
            except discord.HTTPException as e:
                if e.status == 429:
                    print_warning(
                        f"Many requests were made. Waiting 60 seconds. Details: {e}"
                    )
                    await asyncio.sleep(60)
                    new_channel = await guild_to.create_voice_channel(
                        name=channel_voice.name,
                        overwrites=overwrites_to,
                        position=channel_voice.position)
                if category is not None:
                    await new_channel.edit(category=category)
                print_add(
                    f"The voice channel {Fore.YELLOW}{channel_voice.name}{Fore.BLUE} has been created"
                )
            except:
                print_error(
                    f"Error creating voice channel: {channel_voice.name}")

    @staticmethod
    async def emojis_create(guild_to: discord.Guild,
                            guild_from: discord.Guild):
        emojis = guild_from.emojis
        if not emojis:
            print_warning("No emoji found.")
            return
        for emoji in guild_from.emojis:
            try:
                existing_emoji = discord.utils.get(guild_to.emojis,
                                                   name=emoji.name)
                if existing_emoji:
                    print_add(
                        f"An emoji with the name {Fore.YELLOW}{emoji.name}{Fore.BLUE} already exists on the server."
                    )
                else:
                    emoji_url = str(emoji.url)
                    response = requests.get(emoji_url)
                    emoji_image = response.content
                    await guild_to.create_custom_emoji(name=emoji.name,
                                                       image=emoji_image)
                    print_add(
                        f"O emoji {Fore.YELLOW}{emoji.name}{Fore.BLUE} foi criado."
                    )
                    await asyncio.sleep(1)
            except discord.Forbidden:
                print_error(
                    f"Error creating emoji: {Fore.YELLOW}{emoji.name}{Fore.RED} Insufficient permissions.{Fore.RESET}"
                )
                await asyncio.sleep(random.uniform(2, 3))
            except discord.HTTPException as e:
                if e.status == 429:
                    print_warning(
                        f"Many requests were made. Waiting 10 seconds. Details: {e}"
                    )
                    await asyncio.sleep(10)
                    await guild_to.create_custom_emoji(name=emoji.name,
                                                       image=emoji_image)
            except Exception:
                print_warning(f"An error occurred on {emoji.name}")
            except asyncio.TimeoutError:
                print_error(f"An error occurred in {emoji.name} TimeOut")

    @staticmethod
    async def guild_edit(guild_to: discord.Guild, guild_from: discord.Guild):
        try:
            try:
                icon_content = requests.get(guild_from.icon_url).content
            except requests.exceptions.RequestException:
                print_error(
                    f"Unable to download icon from {guild_from.name}")
                icon_content = None
            await guild_to.edit(name=guild_from.name)
            if icon_content is not None:
                try:
                    await guild_to.edit(icon=icon_content)
                    print_add(f"ÍChanged group icon: {guild_to.name}")
                except:
                    print_error(
                        f"Error changing group icon: {guild_to.name}")
        except discord.LoginFailure:
            print(
                "Unable to authenticate to account. Check that the token is correct."
            )
        except discord.Forbidden:
            print_error(f"Error changing group icon: {guild_to.name}")


def print_add(message):
    print(f'{Style.BRIGHT}{Fore.CYAN} {message}{Fore.RESET}')


def print_delete(message):
    print(f'{Style.BRIGHT}{Fore.CYAN} {message}{Fore.RESET}')


def print_warning(message):
    print(f'{Style.BRIGHT}{Fore.YELLOW} {message}{Fore.RESET}')
