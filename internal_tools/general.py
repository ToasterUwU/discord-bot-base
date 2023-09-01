import traceback
from typing import Union

import aiohttp
import nextcord

from internal_tools.configuration import CONFIG


async def error_webhook_send(txt_or_error: Union[str, Exception]):
    if isinstance(txt_or_error, Exception):
        error_text = "".join(traceback.format_exception(type(txt_or_error), txt_or_error, txt_or_error.__traceback__))  # type: ignore
        txt_or_error = f"Unpredicted Error:\n```\n{error_text}\n```"

    if CONFIG["GENERAL"]["ERROR_WEBHOOK_URL"]:
        async with aiohttp.ClientSession() as session:
            webhook = nextcord.Webhook.from_url(
                CONFIG["GENERAL"]["ERROR_WEBHOOK_URL"], session=session
            )

            await webhook.send(txt_or_error)
