from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CallbackContext
import numpy as np
import pandas as pd
import datetime
from logger_debug import *
from config import *
from telegram.error import Unauthorized

logger = getLogger(__name__)

@debug_request
def notify_all_users_admin(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    if chat_id == ADMIN_ID:
        user_id_df = pd.read_csv(USER_IDS_FILE, index_col=0)
        for chat_id in user_id_df.user_id.values:
            try:
                context.bot.send_message(
                    chat_id=int(chat_id),
                    text=UPDATE_TEXT,
                    parse_mode=ParseMode.HTML,
                    disable_notification=True
                )
                logger.info('notified chat_id: %s', chat_id)
            except Unauthorized:
                logger.info('Unauthorized chat_id: %s', chat_id)
            except:
                logger.info('Unknown ERROR chat_id: %s', chat_id)
    else:
        update.message.reply_text('Неверная команда')
