import os
import datetime
import aiohttp

def has_discord_role(author, role) -> bool:
    roles = [x.name.upper() for x in author.roles]
    match_role = role if not role == "BOT" else "ADC"
    if not any(x.startswith(match_role) for x in roles):
        return False
    return True


async def timeout_user(user: int, guild: int, until: int) -> None:
    headers = {"Authorization": f"Bot {os.environ['INHOUSE_BOT_TOKEN']}"}
    url = f"https://discord.com/api/v9/guilds/{guild}/members/{user}"
    timeout = (datetime.datetime.utcnow() + datetime.timedelta(seconds=until)).isoformat()
    async with aiohttp.ClientSession(raise_for_status=True).patch(url, json={"communication_disabled_until": timeout}, headers=headers) as session:
        pass
