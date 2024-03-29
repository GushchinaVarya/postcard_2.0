from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CallbackContext
import numpy as np
import pandas as pd
import datetime

from buttons import *
from logger_debug import *
from config import HOUR_REMINDER, MINUTE_REMINDER, HAPPYBIRTHDAY_PHOTO

logger = getLogger(__name__)

@debug_request
def alarm(context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton(BUTTON2_MAKE, callback_data=CALLBACK_BUTTON2_MAKE)],
    ]
    job = context.job
    context.bot.send_message(
        job.context,
        text='Ваш день рождения уже совсем скоро! Пришлашаем создать вишлист!',
        reply_markup=InlineKeyboardMarkup(keyboard, one_time_keyboard=True)
    )
    logger.info(f'successfully reminded for {job.context}. Now is {str(datetime.datetime.today())}')

@debug_request
def happybday(context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton(BUTTON3_SHOW, callback_data=CALLBACK_BUTTON3_SHOW)],
        [InlineKeyboardButton(BUTTON2_MAKE, callback_data=CALLBACK_BUTTON2_MAKE)],
    ]
    job = context.job
    context.bot.sendPhoto(
        chat_id=job.context,
        photo=open(HAPPYBIRTHDAY_PHOTO, 'rb'),
        reply_markup=InlineKeyboardMarkup(keyboard, one_time_keyboard=True)
    )
    logger.info(f'successfully congratulated for {job.context}. Now is {str(datetime.datetime.today())}')

@debug_request
def show_jobs_by_name(update: Update, context: CallbackContext) -> bool:
    """Test."""
    name = context.args[0]
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        logger.info(f'no jobs for {name}')
    else:
        logger.info(f'jobs for {name}')
        for job in current_jobs:
            logger.info(f'{job.name} {job.context}')
    return True

@debug_request
def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

@debug_request
def set_timer_bday(update: Update, context: CallbackContext) -> None:
    """Add a job to the queue."""
    keyboard = [
        [InlineKeyboardButton(BUTTON2_MAKE, callback_data=CALLBACK_BUTTON2_MAKE)],
    ]
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the date format DD.MM for the timer in seconds
        dateofbirth = context.args[0]
        dayofbirth = int(dateofbirth.split('.')[0])
        monthofbirth = int(dateofbirth.split('.')[1])
        yearcurrent = datetime.datetime.today().year

        if (datetime.date(yearcurrent, monthofbirth, dayofbirth) - datetime.datetime.today().date()).days < 0:
            due = datetime.datetime(yearcurrent + 1, monthofbirth, dayofbirth, HOUR_REMINDER, MINUTE_REMINDER) - datetime.timedelta(days=2)
            due_bd = datetime.datetime(yearcurrent + 1, monthofbirth, dayofbirth, HOUR_REMINDER, MINUTE_REMINDER)
            update.message.reply_text('Спасибо! Мы напомним о создании вишлиста за 2 дня до вашего дня рождения!\nУдалить напоминание - /stopreminder\nВернуться в главное меню - /start')
        elif (datetime.date(yearcurrent, monthofbirth, dayofbirth) - datetime.datetime.today().date()).days == 0:
            update.message.reply_text(
                text='C днем рождения! Пришлашаем создать вишлист!',
                reply_markup=InlineKeyboardMarkup(keyboard, one_time_keyboard=True),
            )
            due = datetime.datetime(yearcurrent + 1, monthofbirth, dayofbirth, HOUR_REMINDER, MINUTE_REMINDER) - datetime.timedelta(days=2)
            due_bd = datetime.datetime(yearcurrent + 1, monthofbirth, dayofbirth, HOUR_REMINDER, MINUTE_REMINDER)
        elif (datetime.date(yearcurrent, monthofbirth, dayofbirth) - datetime.datetime.today().date()).days == 1:
            update.message.reply_text(
                text='Ваш день рождения уже завтра! Пришлашаем создать вишлист!',
                reply_markup=InlineKeyboardMarkup(keyboard, one_time_keyboard=True),
            )
            due = datetime.datetime(yearcurrent + 1, monthofbirth, dayofbirth, HOUR_REMINDER, MINUTE_REMINDER) - datetime.timedelta(days=2)
            due_bd = datetime.datetime(yearcurrent, monthofbirth, dayofbirth, HOUR_REMINDER, MINUTE_REMINDER)
        elif (datetime.date(yearcurrent, monthofbirth, dayofbirth) - datetime.datetime.today().date()).days == 2:
            update.message.reply_text(
                text='Ваш день рождения уже послезавтра! Пришлашаем создать вишлист!',
                reply_markup=InlineKeyboardMarkup(keyboard, one_time_keyboard=True),
            )
            due = datetime.datetime(yearcurrent + 1, monthofbirth, dayofbirth, HOUR_REMINDER, MINUTE_REMINDER) - datetime.timedelta(days=2)
            due_bd = datetime.datetime(yearcurrent, monthofbirth, dayofbirth, HOUR_REMINDER, MINUTE_REMINDER)
        elif (datetime.date(yearcurrent, monthofbirth, dayofbirth) - datetime.datetime.today().date()).days > 2:
            due = datetime.datetime(yearcurrent, monthofbirth, dayofbirth, HOUR_REMINDER, MINUTE_REMINDER) - datetime.timedelta(days=2)
            due_bd = datetime.datetime(yearcurrent, monthofbirth, dayofbirth, HOUR_REMINDER, MINUTE_REMINDER)
            update.message.reply_text('Спасибо! Мы напомним о создании вишлиста за 2 дня до вашего дня рождения!\nУдалить напоминание - /stopreminder\nВернуться в главное меню - /start')
        else:
            logger.info(f'!!!!warning!!!! setting timer for chat_id {chat_id} with birthday {dateofbirth}. Now is {str(datetime.datetime.today())}')
            due = datetime.datetime(yearcurrent+1, monthofbirth, dayofbirth, HOUR_REMINDER, MINUTE_REMINDER) - datetime.timedelta(days=2)
            due_bd = datetime.datetime(yearcurrent+1, monthofbirth, dayofbirth, HOUR_REMINDER, MINUTE_REMINDER)
            update.message.reply_text('Спасибо! Мы напомним о создании вишлиста за 2 дня до вашего дня рождения!\nУдалить напоминание - /stopreminder\nВернуться в главное меню - /start')

        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_once(alarm, when=due, context=chat_id, name=str(chat_id))
        context.job_queue.run_once(happybday, when=due_bd, context=chat_id, name=str(chat_id))

        user_id_df_bday = pd.read_csv(USER_IDS_FILE_BDAY, index_col=0)
        if chat_id not in user_id_df_bday.user_id.values:
            user_id_df_bday = pd.concat([user_id_df_bday, pd.DataFrame([{'user_id': chat_id, 'bday':np.array([dateofbirth])}])],
                                   ignore_index=True)
            user_id_df_bday.to_csv(USER_IDS_FILE_BDAY)
            logger.info('added to file of users birthdays chat_id: %s', chat_id)
        if chat_id in user_id_df_bday.user_id.values:
            user_id_df_bday.loc[[user_id_df_bday[user_id_df_bday.user_id == chat_id].index[0]], ['bday']] = dateofbirth
            user_id_df_bday.to_csv(USER_IDS_FILE_BDAY)
            logger.info('updated file of users birthdays chat_id: %s', chat_id)

        logger.info(f'{update.message.chat.id} successfully set reminder on {str(due)}. Now is {str(datetime.datetime.today())}')
        logger.info(f'{update.message.chat.id} successfully set congratulator on {str(due_bd)}. Now is {str(datetime.datetime.today())}')
        if job_removed:
            logger.info(f'old {update.message.chat.id} timer was removed')

    except (IndexError, ValueError):
        update.message.reply_text('Формат ввода /mybday DD.MM\nНапример /mybday 31.01')



@debug_request
def remove_timer_bday(update: Update, context: CallbackContext) -> None:
    """Remove reminder from file."""
    chat_id = update.message.chat_id
    user_id_df_bday = pd.read_csv(USER_IDS_FILE_BDAY, index_col=0)
    if chat_id not in user_id_df_bday.user_id.values:
        update.message.reply_text('Вы не создавали напоминание о создании вишлиста.\nСоздать напоминание - /mybday DD.MM\nВернуться в главное меню - /start')
    else:
        user_id_df_bday = user_id_df_bday.drop(user_id_df_bday[user_id_df_bday['user_id'] == chat_id].index).reset_index(drop=True)
        user_id_df_bday.to_csv(USER_IDS_FILE_BDAY)
        logger.info(f'removed {chat_id} from file of users birthdays')
        update.message.reply_text('Вы успешно удалили ваш день рождения из базы напоминаний.\nСоздать новое напоминание - /mybday DD.MM\nВернуться в главное меню - /start')

    job_removed = remove_job_if_exists(str(chat_id), context)
    if job_removed:
        logger.info(f'old {update.message.chat.id} reminder and congratulator were removed')