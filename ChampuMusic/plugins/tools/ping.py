import logging
from datetime import datetime

from pyrogram import filters
from pyrogram.types import Message

from config import BANNED_USERS, PING_IMG_URL
from ChampuMusic import app
from ChampuMusic.core.call import Champu
from ChampuMusic.utils import bot_sys_stats
from ChampuMusic.utils.decorators.language import language
from ChampuMusic.utils.inline import support_group_markup

# Logger Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default Image Fallback
DEFAULT_PING_IMG = "https://te.legra.ph/file/71ac5c314d1af0d00a128-13be9eae02043dbd3f.jpg"  # Change this if needed

@app.on_message(filters.command(["ping", "alive"]) & ~BANNED_USERS)
@language
async def ping_com(client, message: Message, _):
    try:
        logger.info("Ping command received!")

        # Ensure PING_IMG_URL is valid
        image_url = PING_IMG_URL if PING_IMG_URL else DEFAULT_PING_IMG

        # Send initial response with image
        response = await message.reply_photo(
            photo=image_url,
            caption=_["ping_1"].format(app.mention),
        )
        logger.info("Ping image sent successfully!")

        # Measure response time
        start = datetime.now()
        pytgping = await Champu.ping()
        UP, CPU, RAM, DISK = await bot_sys_stats()
        resp = (datetime.now() - start).microseconds / 1000

        # Update the message with stats
        await response.edit_text(
            _["ping_2"].format(
                resp,
                app.mention,
                UP,
                RAM,
                CPU,
                DISK,
                pytgping,
            ),
            reply_markup=support_group_markup(_),
        )
        logger.info("Ping response edited successfully!")

    except Exception as e:
        logger.error(f"Error in /ping command: {e}")
        await message.reply_text(f"Error: {e}")  # Send error message for debugging
