from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CallbackContext
import numpy as np
import pandas as pd
import datetime
from logger_debug import *
from config import *
from telegram.error import Unauthorized
from buttons import *
from timer import *

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


@debug_request
def reset_all_timers_admin(update: Update, context: CallbackContext) -> None:
    if update.message.chat_id == ADMIN_ID:
        user_id_df_bday = pd.read_csv(USER_IDS_FILE_BDAY, index_col=0)
        chat_id_s = user_id_df_bday.user_id.values
        bday_s = user_id_df_bday.bday.values
        for i in range(user_id_df_bday.shape[0]):
            try:
                chat_id = int(chat_id_s[i])
                dateofbirth = str(bday_s[i])
                dayofbirth = int(dateofbirth.split('.')[0])
                monthofbirth = int(dateofbirth.split('.')[1])
                yearcurrent = datetime.datetime.today().year

                if (datetime.datetime(yearcurrent, monthofbirth, dayofbirth, HOUR_REMINDER, MINUTE_REMINDER) - datetime.timedelta(days=2) - datetime.datetime.today()).days < 0:
                    due = datetime.datetime(yearcurrent + 1, monthofbirth, dayofbirth, HOUR_REMINDER, MINUTE_REMINDER) - datetime.timedelta(days=2)

                elif (datetime.datetime(yearcurrent, monthofbirth, dayofbirth, HOUR_REMINDER, MINUTE_REMINDER) - datetime.timedelta(days=2) - datetime.datetime.today()).days >= 0:
                    due = datetime.datetime(yearcurrent, monthofbirth, dayofbirth, HOUR_REMINDER, MINUTE_REMINDER) - datetime.timedelta(days=2)
                else:
                    logger.info(f'error setting timer for chat_id {chat_id} with birthday {dateofbirth}. Now is {str(datetime.datetime.today())}')

                job_removed = remove_job_if_exists(str(chat_id), context)
                if job_removed:
                    logger.info(f'old {chat_id} timer was removed')
                context.job_queue.run_once(alarm, when=due, context=chat_id, name=str(chat_id))
                logger.info(f'admin successfully set timer for {chat_id} on {str(due)}. Now is {str(datetime.datetime.today())}')

            except (IndexError, ValueError):
                logger.info(f'problem with setting timer for {chat_id}')

    else:
        update.message.reply_text('Неверная команда')
