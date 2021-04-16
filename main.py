from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram.ext import CallbackContext, ConversationHandler
from telegram.error import Unauthorized
from telegram.utils.request import Request
from config import *
from db import *
from picture import write_wish, write_from
import os
from appearance_funtions import *
from telegram import InputMediaPhoto, InputFile
import numpy as np
import pandas as pd

from buttons import *
from logger_debug import *
from timer import alarm, remove_job_if_exists, set_timer_bday

from admin_functions import notify_all_users_admin

logger = getLogger(__name__)

NAME, CONFIRM, WELCOME_SPEECH, FOUNDATION_0, METHOD_0, FOUNDATION_1, METHOD_1, FOUNDATION_2, METHOD_2, N_FOUNDS, THANKS_SPEECH, WISH, FROM_WHOM, FOUND_WISHLIST, WISH_MODE, FROM_MODE, PIC_NUM, DELETE_MODE = range(18)


@debug_request
def start_buttons_handler(update: Update, context: CallbackContext):
    context.user_data[WISH_MODE] = 'False'
    context.user_data[FROM_MODE] = 'False'
    context.user_data[DELETE_MODE] = 'False'
    chat_id = update.message.chat.id
    user_id_df = pd.read_csv(USER_IDS_FILE, index_col=0)
    if chat_id not in user_id_df.user_id.values:
        user_id_df = user_id_df.append(pd.DataFrame({'user_id': np.array([chat_id])})).reset_index(drop=True)
        user_id_df.to_csv(USER_IDS_FILE)
        logger.info('added to file of unique users chat_id: %s', chat_id)
    keyboard = [
        [InlineKeyboardButton(BUTTON1_FIND, callback_data=CALLBACK_BUTTON1_FIND)],
        [InlineKeyboardButton(BUTTON2_MAKE, callback_data=CALLBACK_BUTTON2_MAKE)],
        [InlineKeyboardButton(BUTTON3_SHOW, callback_data=CALLBACK_BUTTON3_SHOW)],
    ]
    update.message.reply_text(
        text='''
*Привет! Это бот «Вместо открытки»*

Бот позволяет создать благотворительный вишлист: список организаций, в одну из которых ваши друзья могут сделать пожертвование в качестве подарка вам.
Также бот может найти уже созданный вишлист и отправить поздравительную открытку автору вишлиста. 

Подробнее о боте - /about
*Выберите режим:*''',
        reply_markup=InlineKeyboardMarkup(keyboard, one_time_keyboard=True),
        parse_mode=ParseMode.MARKDOWN
    )
    return ConversationHandler.END

@debug_request
def do_create(update: Update, context: CallbackContext):
    init = update.callback_query.data
    chat_id = update.callback_query.message.chat.id
    if init == CALLBACK_BUTTON1_FIND:
        context.user_data[WISH_MODE] = 'False'
        context.user_data[FROM_MODE] = 'False'
        context.user_data[DELETE_MODE] = 'False'
        update.callback_query.bot.send_message(
            chat_id=chat_id,
            text='Введите название вишлиста используя знак #\n\nпример #ДеньРожденияИванаИванова01Янв2021',
            reply_markup=ReplyKeyboardRemove()
        )

    if init == CALLBACK_BUTTON3_SHOW:
        context.user_data[WISH_MODE] = 'False'
        context.user_data[FROM_MODE] = 'False'
        context.user_data[DELETE_MODE] = 'False'
        wishlists = show_my_wishlists(user_id=chat_id, limit=10)
        if len(wishlists) == 0:
            update.callback_query.bot.send_message(
                chat_id=chat_id,
                text='Пока у вас нет вишлистов. Чтобы найти чей-то вишлист или создать ваш первый вишлист нажмите /start',
                reply_markup=ReplyKeyboardRemove()

            )
        else:
            keyboard = [
                [InlineKeyboardButton(BUTTON10_DELETE_WISHLIST, callback_data=CALLBACK_BUTTON10_DELETE_WISHLIST)],
            ]
            for wishlist_i in wishlists:
                update.callback_query.bot.send_message(
                    chat_id=chat_id,
                    text=print_wishlist_with_thanks(wishlist_i),
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True
                )
            update.callback_query.bot.send_message(
                chat_id=chat_id,
                text='''
Чтобы найти другой вишлист или создать новый нажмите /start 
Чтобы удалить один из этих вишлистов нажмите УДАЛИТЬ ВИШЛИСТ''',
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(keyboard, one_time_keyboard=True),
            )
    if init == CALLBACK_BUTTON2_MAKE:
        context.user_data[WISH_MODE] = 'False'
        context.user_data[FROM_MODE] = 'False'
        context.user_data[DELETE_MODE] = 'False'
        logger.info(f'{chat_id} started making wishlist')
        update.callback_query.bot.send_message(
            chat_id=chat_id,
            text='''
<b>Придумайте имя вашего вишлиста.</b>
Одно слово без пробелов и знаков. Пример ДеньРожденияИванаИванова01Янв2021
Чтобы создать вишлист для 8 марта начните название со слов "8марта". Пример 8мартаДляАнныСеменовой

Отменить создание вишлиста - /cancel''',
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=ParseMode.HTML
        )
        return NAME

    if init == CALLBACK_BUTTON4_GENERATE_POSTCARD:
        context.user_data[WISH_MODE] = 'False'
        context.user_data[FROM_MODE] = 'False'
        context.user_data[DELETE_MODE] = 'False'
        logger.info(f'{chat_id} started generating postcard')
        if context.user_data[FOUND_WISHLIST][:6] == '8марта':
            #update.callback_query.bot.send_message(
            #    chat_id=chat_id,
            #    text='Открытки для этого вишлиста будут доступны только с 5го марта. Введите другой вишлист или нажмите /start',
            #)
            keyboard = [
                [InlineKeyboardButton(BUTTON_PIC1, callback_data=CALLBACK_BUTTON_8MARCH_PIC1),
                 InlineKeyboardButton(BUTTON_PIC2, callback_data=CALLBACK_BUTTON_8MARCH_PIC2)]
            ]
            update.callback_query.bot.send_message(
                chat_id=chat_id,
                text=f'Выберите внешний вид открытки',
                reply_markup=InlineKeyboardMarkup(keyboard, one_time_keyboard=True),
                parse_mode=ParseMode.HTML
            )
            update.callback_query.bot.send_media_group(
                chat_id=chat_id,
                media=[InputMediaPhoto(open(PIC_FOLDER+PICTURE_NAMES_DEMO[2], 'rb')),
                       InputMediaPhoto(open(PIC_FOLDER+PICTURE_NAMES_DEMO[3], 'rb'))]
            )
        else:
            keyboard = [
                [InlineKeyboardButton(BUTTON_PIC1, callback_data=CALLBACK_BUTTON_PIC1),
                 InlineKeyboardButton(BUTTON_PIC2, callback_data=CALLBACK_BUTTON_PIC2)]
            ]
            update.callback_query.bot.send_message(
                chat_id=chat_id,
                text=f'Выберите внешний вид открытки',
                reply_markup=InlineKeyboardMarkup(keyboard, one_time_keyboard=True),
                parse_mode=ParseMode.HTML
            )
            update.callback_query.bot.send_media_group(
                chat_id=chat_id,
                media=[InputMediaPhoto(open(PIC_FOLDER+PICTURE_NAMES_DEMO[0], 'rb')),
                       InputMediaPhoto(open(PIC_FOLDER+PICTURE_NAMES_DEMO[1], 'rb'))]
            )

    if init == CALLBACK_BUTTON_PIC1:
        context.user_data[WISH_MODE] = 'True'
        context.user_data[FROM_MODE] = 'False'
        context.user_data[DELETE_MODE] = 'False'
        context.user_data[PIC_NUM] = 0
        logger.info(f'{chat_id} choose pic1')
        update.callback_query.bot.send_message(
            chat_id=chat_id,
            text=f'Введите небольшое (до {WISH_LIMIT} символов) пожелание\nнапример: Счастья здоровья',
            parse_mode=ParseMode.HTML
        )

    if init == CALLBACK_BUTTON_PIC2:
        context.user_data[WISH_MODE] = 'True'
        context.user_data[FROM_MODE] = 'False'
        context.user_data[DELETE_MODE] = 'False'
        context.user_data[PIC_NUM] = 1
        logger.info(f'{chat_id} choose pic2')
        update.callback_query.bot.send_message(
            chat_id=chat_id,
            text=f'Введите небольшое (до {WISH_LIMIT} символов) пожелание\nнапример: Счастья здоровья',
            parse_mode=ParseMode.HTML
        )

    if init == CALLBACK_BUTTON_8MARCH_PIC1:
        context.user_data[WISH_MODE] = 'True'
        context.user_data[FROM_MODE] = 'False'
        context.user_data[DELETE_MODE] = 'False'
        context.user_data[PIC_NUM] = 2
        logger.info(f'{chat_id} choose 8 march pic1')
        update.callback_query.bot.send_message(
            chat_id=chat_id,
            text=f'Введите небольшое (до {WISH_LIMIT} символов) пожелание\nнапример: Счастья здоровья',
            parse_mode=ParseMode.HTML
        )

    if init == CALLBACK_BUTTON_8MARCH_PIC2:
        context.user_data[WISH_MODE] = 'True'
        context.user_data[FROM_MODE] = 'False'
        context.user_data[DELETE_MODE] = 'False'
        context.user_data[PIC_NUM] = 3
        logger.info(f'{chat_id} choose 8 march pic2')
        update.callback_query.bot.send_message(
            chat_id=chat_id,
            text=f'Введите небольшое (до {WISH_LIMIT} символов) пожелание\nнапример: Счастья здоровья',
            parse_mode=ParseMode.HTML
        )

    if init == CALLBACK_BUTTON6_ADD_NAME:
        context.user_data[WISH_MODE] = 'False'
        context.user_data[FROM_MODE] = 'True'
        context.user_data[DELETE_MODE] = 'False'
        update.callback_query.bot.send_message(
            chat_id=chat_id,
            text='Введите подпись\nнапример: Oт твоей лучшей подруги',
            parse_mode=ParseMode.HTML
        )

    elif init == CALLBACK_BUTTON5_ANONYMOUS_SEND:
        context.user_data[FROM_MODE] = 'False'
        context.user_data[WISH_MODE] = 'False'
        context.user_data[DELETE_MODE] = 'False'
        keyboard = [
            [InlineKeyboardButton(BUTTON7_ADD_SCREENSHOT, callback_data=CALLBACK_BUTTON7_ADD_SCREENSHOT)],
            [InlineKeyboardButton(BUTTON8_NO_SCREENSHOT, callback_data=CALLBACK_BUTTON8_NO_SCREENSHOT)]
        ]
        pic_name = PIC_FOLDER+'wish_' + str(chat_id) + '_' +PICTURE_NAMES[context.user_data[PIC_NUM]]
        update.callback_query.bot.sendPhoto(
            chat_id=chat_id,
            photo=open(pic_name, 'rb'),
        )
        update.callback_query.bot.send_message(
            chat_id=chat_id,
            text=f"Предпросмотр открытки ⬆️ \n(Ваша открытка будет отправлена анонимно)",
            reply_markup=InlineKeyboardMarkup(keyboard, one_time_keyboard=True),
        )

    elif init == CALLBACK_BUTTON7_ADD_SCREENSHOT:
        context.user_data[FROM_MODE] = 'False'
        context.user_data[WISH_MODE] = 'False'
        context.user_data[DELETE_MODE] = 'False'
        update.callback_query.bot.send_message(
            chat_id=chat_id,
            text='Пришлите скриншот перевода'
        )

    elif init == CALLBACK_BUTTON8_NO_SCREENSHOT:
        context.user_data[WISH_MODE] = 'False'
        context.user_data[FROM_MODE] = 'False'
        context.user_data[DELETE_MODE] = 'False'
        wishlist = find_wishlist(namelowreg=(context.user_data[FOUND_WISHLIST]).lower(), limit=1)
        wishlist_author_user_id = wishlist[0][0]
        wishlist_thanks_message = wishlist[0][9]
        bot = update.callback_query.bot
        if os.path.exists(PIC_FOLDER+'from_' + str(chat_id) + '_' + PICTURE_NAMES[context.user_data[PIC_NUM]]):
            pic_name = PIC_FOLDER+'from_' + str(chat_id) + '_' + PICTURE_NAMES[context.user_data[PIC_NUM]]
        else:
            pic_name = PIC_FOLDER+'wish_' + str(chat_id) + '_' + PICTURE_NAMES[context.user_data[PIC_NUM]]
        bot.send_message(
            chat_id=wishlist_author_user_id,
            text=f'💌 ВАМ НОВАЯ ОТКРЫТКА!💌 \n\n\n',
        )
        bot.sendPhoto(
            chat_id=wishlist_author_user_id,
            photo=open(pic_name, 'rb'),
        )
        update.callback_query.bot.send_message(
            chat_id=chat_id,
            text=f'''
📤 Ваша открытка отправлена автору вишлиста 📤 \n\n
Сообщение от автора вишлиста: <b>{wishlist_thanks_message}</b>\n
Спасибо, что воспользовались ботом.
Чтобы найти другой вишлист или создать свой нажмите /start''',
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=ParseMode.HTML
        )
        logger.info(f'{chat_id} successfully sent postcard to user {wishlist_author_user_id}')
        os.system(f"(rm -rf {PIC_FOLDER+'from_' + str(chat_id) + '_' + PICTURE_NAMES[context.user_data[PIC_NUM]]})")
        os.system(f"(rm -rf {PIC_FOLDER+'wish_' + str(chat_id) + '_' + PICTURE_NAMES[context.user_data[PIC_NUM]]})")
        logger.info(f'all temporary data for {chat_id} was successfully deleted')

    elif init == CALLBACK_BUTTON9_READY:
        context.user_data[FROM_MODE] = 'False'
        context.user_data[WISH_MODE] = 'False'
        context.user_data[DELETE_MODE] = 'False'
        wishlist = find_wishlist(namelowreg=(context.user_data[FOUND_WISHLIST]).lower(), limit=1)
        wishlist_author_user_id = wishlist[0][0]
        wishlist_thanks_message = wishlist[0][9]
        if os.path.exists(PIC_FOLDER+'from_' + str(chat_id) + '_' + PICTURE_NAMES[context.user_data[PIC_NUM]]):
            pic_name = PIC_FOLDER+'from_' + str(chat_id) + '_' + PICTURE_NAMES[context.user_data[PIC_NUM]]
        else:
            pic_name = PIC_FOLDER+'wish_' + str(chat_id) + '_' + PICTURE_NAMES[context.user_data[PIC_NUM]]
        bot = update.callback_query.bot
        bot.send_message(
            chat_id=wishlist_author_user_id,
            text=f'💌 ВАМ НОВАЯ ОТКРЫТКА!💌 \n\n\n',
        )
        bot.sendPhoto(
            chat_id=wishlist_author_user_id,
            photo=open(pic_name, 'rb'),
        )
        bot.sendPhoto(
            chat_id=wishlist_author_user_id,
            photo=open(PIC_FOLDER+'screen_' + str(chat_id) + '.png', 'rb'),
        )
        bot.send_message(
            chat_id=chat_id,
            text=f'''
📤 Ваша открытка отправлена автору вишлиста 📤 \n\n
Сообщение от автора вишлиста: <b>{wishlist_thanks_message}</b>\n
Спасибо, что воспользовались ботом.
Чтобы найти другой вишлист или создать свой нажмите /start''',
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=ParseMode.HTML
        )
        logger.info(f'{chat_id} successfully sent postcard to user {wishlist_author_user_id}')
        os.system(f"(rm -rf {PIC_FOLDER+'screen_' + str(chat_id) + '.png'})")
        os.system(f"(rm -rf {PIC_FOLDER+'from_' + str(chat_id) + '_' + PICTURE_NAMES[context.user_data[PIC_NUM]]})")
        os.system(f"(rm -rf {PIC_FOLDER+'wish_' + str(chat_id) + '_' + PICTURE_NAMES[context.user_data[PIC_NUM]]})")
        logger.info(f'all temporary data for {chat_id} was successfully deleted')

    elif init == CALLBACK_BUTTON10_DELETE_WISHLIST:
        context.user_data[FROM_MODE] = 'False'
        context.user_data[WISH_MODE] = 'False'
        context.user_data[DELETE_MODE] = 'True'
        update.callback_query.bot.send_message(
            chat_id=chat_id,
            text=f"Введите название вишлиста который нужно удалить (просто имя без знака #)",
            reply_markup=ReplyKeyboardRemove(),
        )

@debug_request
def message_handler(update: Update, context: CallbackContext):
    text = update.message.text
    if text[0] == '#':
        if context.user_data[DELETE_MODE] == 'True':
            update.message.reply_text('Чтобы удалить вишлист введите его название без # . Вернуться в главное меню - /start')
        else:
            wishlistname = text[1:]
            wishlist = find_wishlist(namelowreg=wishlistname.lower(), limit=1)
            if wishlist:
                context.user_data[FOUND_WISHLIST] = wishlistname
                keyboard = [[InlineKeyboardButton(BUTTON4_GENERATE_POSTCARD, callback_data=CALLBACK_BUTTON4_GENERATE_POSTCARD)]]
                reply_text = print_wishlist(wishlist[0])
                update.message.reply_text(
                    text=f'Вишлист найден!✔️\n\n\n{reply_text}\n\n\nТеперь вы знаете что хочет получить автор вишлиста.\nМожете пожертвовать в одну их этих организаций и сгенерировать открытку. Бот отправит ее автору. Чтобы вернуться в начало нажмите /start',
                    reply_markup=InlineKeyboardMarkup(keyboard, one_time_keyboard=True),
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True
                )
            else:
                update.message.reply_text(
                    text='Вишлист c таким именем не найден. Введите другой вишлист.',
                    reply_markup=ReplyKeyboardRemove()
                )

    else:
        if (context.user_data[WISH_MODE] == 'True'):
            wishtext = text
            if len(wishtext) > WISH_LIMIT:
                update.message.reply_text(
                    text="Слишком длинное пожелание"
                )
            else:
                context.user_data[WISH] = wishtext
                logger.info('user_data: %s', context.user_data)
                keyboard = [
                    [InlineKeyboardButton(BUTTON5_ANONYMOUS_SEND, callback_data=CALLBACK_BUTTON5_ANONYMOUS_SEND)],
                    [InlineKeyboardButton(BUTTON6_ADD_NAME, callback_data=CALLBACK_BUTTON6_ADD_NAME)],
                ]
                pic_name = PIC_FOLDER+'wish_'+str(update.message.chat.id)+'_'+PICTURE_NAMES[context.user_data[PIC_NUM]]
                write_wish(text=wishtext, pic_number=context.user_data[PIC_NUM], pic_name=PIC_FOLDER+PICTURE_NAMES[context.user_data[PIC_NUM]], new_name=pic_name)
                context.bot.sendPhoto(
                    chat_id=update.message.chat.id,
                    photo=open(pic_name, 'rb'),
                )
                update.message.reply_text(
                    text=f"Предпросмотр открытки ⬆️\nЕсли передумали и хотите поменять пожелание, введите его заново. Либо выберите нужна ли на открытке подпись⬇️",
                    reply_markup=InlineKeyboardMarkup(keyboard, one_time_keyboard=True),
                )
        elif context.user_data[FROM_MODE] == 'True':
            from_whom = text
            context.user_data[FROM_WHOM] = from_whom
            logger.info('user_data: %s', context.user_data)
            keyboard = [
                [InlineKeyboardButton(BUTTON7_ADD_SCREENSHOT, callback_data=CALLBACK_BUTTON7_ADD_SCREENSHOT)],
                [InlineKeyboardButton(BUTTON8_NO_SCREENSHOT, callback_data=CALLBACK_BUTTON8_NO_SCREENSHOT)]
            ]
            pic_name_wish = PIC_FOLDER+'wish_' + str(update.message.chat.id) + '_' + PICTURE_NAMES[context.user_data[PIC_NUM]]
            pic_name = PIC_FOLDER+'from_'+str(update.message.chat.id) + '_' + PICTURE_NAMES[context.user_data[PIC_NUM]]
            write_from(text=from_whom, pic_number=context.user_data[PIC_NUM], pic_name=pic_name_wish, new_name=pic_name)
            context.bot.sendPhoto(
                chat_id=update.message.chat.id,
                photo=open(pic_name, 'rb'),
            )
            update.message.reply_text(
                text=f"Предпросмотр открытки ⬆️\nЕсли передумали и хотите поменять подпись, введите ее заново. Либо выберите нужно ли прикреплять скриншот.",
                reply_markup=InlineKeyboardMarkup(keyboard, one_time_keyboard=True),
            )
        elif context.user_data[DELETE_MODE] == 'True':
            wishlistname = text
            wishlist = find_wishlist(namelowreg=wishlistname.lower(), limit=1)
            if wishlist:
                if wishlist[0][0] != update.message.chat.id:
                    update.message.reply_text('Вы не можете удалить этот вишлист, так как не Вы его создали. Введите другой вишлист или нажмите /start')
                if wishlist[0][0] == update.message.chat.id:
                    delete(namelowreg=wishlistname.lower())
                    update.message.reply_text('Вишлист успешно удален. Чтобы найти или создать вишлист нажмите /start')
                    context.user_data[DELETE_MODE] = 'False'
                    logger.info(f'wishlist {wishlistname} deleted')
            else:
                update.message.reply_text('Вишлист c таким именем не найден. Введите другой вишлист или нажмите /start')
        else:
            update.message.reply_text('Неверный формат ввода')

def photo_handler(update: Update, context: CallbackContext):
    context.user_data[WISH_MODE] = 'False'
    context.user_data[FROM_MODE] = 'False'
    context.user_data[DELETE_MODE] = 'False'
    name_screenshot = PIC_FOLDER+'screen_'+str(update.message.chat.id)+'.png'
    photo_file = update.message.photo[-1].get_file()
    photo_file.download(name_screenshot)
    logger.info("Photo of %s", name_screenshot)
    keyboard = [[InlineKeyboardButton(BUTTON9_READY, callback_data=CALLBACK_BUTTON9_READY)]]
    update.message.reply_text(
        text='Скриншот добавлен',
        reply_markup=InlineKeyboardMarkup(keyboard, one_time_keyboard=True),
    )

@debug_request
def name_handler(update: Update, context: CallbackContext):
    context.user_data[WISH_MODE] = 'False'
    context.user_data[FROM_MODE] = 'False'
    context.user_data[DELETE_MODE] = 'False'
    name = update.message.text
    if len(name.split(' ')) > 1:
        update.message.reply_text(
            text='Пожалуйста введите название без пробелов.',
            parse_mode=ParseMode.HTML,
        )
    else:
        if wishlist_name_available(namelowreg=name.lower()):
            context.user_data[NAME] = name
            logger.info('user_data: %s', context.user_data)
            update.message.reply_text(
                text='''
Название сохранено✔️.

Введите приветственное обращение к друзьям.
Пример:
Привет! Это Иван Иванов. Буду рад если вы пожертвуете в один из следующих фондов, для меня их деятельность очень важна.

Отменить создание вишлиста - /cancel''',
                parse_mode=ParseMode.HTML,
            )
            return WELCOME_SPEECH
        else:
            update.message.reply_text(
                text='К сожалению такое название уже занято, пожалуйста введите другое название.',
                parse_mode=ParseMode.HTML,
            )

def welcome_speech_handler(update: Update, context: CallbackContext):
    context.user_data[WELCOME_SPEECH] = update.message.text
    update.message.reply_text(
        text='Введите название первой благотворительной организации (максимум - 3)\n\nОтменить создание вишлиста - /cancel',
        parse_mode=ParseMode.HTML,
    )
    return FOUNDATION_0

@debug_request
def foundation_0_handler(update: Update, context: CallbackContext):
    context.user_data[FOUNDATION_0] = update.message.text
    logger.info('user_data: %s', context.user_data)
    update.message.reply_text(
        text='Введите методы оплаты для этой организации в свободном формате. Также можете указать сайт проекта.\n\nПример: карта сбербанка 1111 2222 3333 4444 либо Paypal paypal@mail.ru либо на сайте www.fund.ru/donate\n\nОтменить создание вишлиста - /cancel',
        parse_mode=ParseMode.HTML,
    )
    return METHOD_0

@debug_request
def method_0_handler(update: Update, context: CallbackContext):
    context.user_data[METHOD_0] = update.message.text
    context.user_data[N_FOUNDS] = 1
    logger.info('user_data: %s', context.user_data)
    update.message.reply_text(
        text="Введите название второй благотворительной организации.\n\nЕсли одной достаточно нажмите /skip . Отменить создание вишлиста - /cancel",
        )
    return FOUNDATION_1

@debug_request
def foundation_1_handler(update: Update, context: CallbackContext):
    context.user_data[FOUNDATION_1] = update.message.text
    logger.info('user_data: %s', context.user_data)
    update.message.reply_text(
        text='Введите методы оплаты для этой организации в свободном формате. Также можете указать сайт проекта\n\nПример: карта сбербанка 1111 2222 3333 4444 либо Paypal paypal@mail.ru либо на сайте www.fund.ru/donate\n\nОтменить создание вишлиста - /cancel',
        parse_mode=ParseMode.HTML,
    )
    return METHOD_1

@debug_request
def method_1_handler(update: Update, context: CallbackContext):
    context.user_data[METHOD_1] = update.message.text
    context.user_data[N_FOUNDS] = 2
    logger.info('user_data: %s', context.user_data)
    update.message.reply_text(
        text="Введите название третьей благотворительной организации.\nЕсли двух достаточно нажмите /skip . Отменить создание вишлиста - /cancel",
    )
    return FOUNDATION_2

@debug_request
def foundation_2_handler(update: Update, context: CallbackContext):
    context.user_data[FOUNDATION_2] = update.message.text
    logger.info('user_data: %s', context.user_data)
    update.message.reply_text(
        text='Введите методы оплаты для этой организации в свободном формате. Также можете указать сайт проекта\n\nПример: карта сбербанка 1111 2222 3333 4444 либо Paypal paypal@mail.ru либо на сайте www.fund.ru/donate\n\nОтменить создание вишлиста - /cancel',
        parse_mode=ParseMode.HTML,
    )
    return METHOD_2

@debug_request
def method_2_handler(update: Update, context: CallbackContext):
    context.user_data[METHOD_2] = update.message.text
    context.user_data[N_FOUNDS] = 3
    logger.info('user_data: %s', context.user_data)
    update.message.reply_text(
        text=f'''
Введите сообщение-благодарность. Это сообщение ваши друзья увидят когда отправят вам открытку.

Пример:
Спасибо вам за пожертвование. Вы классные. Ваш Иван Иванов🤍

Отменить создание вишлиста - /cancel''',
        parse_mode=ParseMode.HTML,
    )

    return THANKS_SPEECH

@debug_request
def skip(update: Update, context: CallbackContext) -> int:
    logger.info("User %s wants to skip other funds.", context.user_data)
    update.message.reply_text(
        text=f'''
Ввод оранизаций завершен
Введите сообщение-благодарность. Это сообщение ваши друзья увидят когда отправят вам открытку.

Пример:
Спасибо вам за пожертвование. Вы классные. Ваш Иван Иванов🤍

Отменить создание вишлиста - /cancel
''',
        parse_mode=ParseMode.HTML
    )
    return THANKS_SPEECH

def thanks_speech_handler(update: Update, context: CallbackContext) -> int:
    context.user_data[THANKS_SPEECH] = update.message.text
    name = context.user_data[NAME]
    n_founds = context.user_data[N_FOUNDS]
    logger.info("User %s wants to skip other funds.", context.user_data)
    #keyboard = [[KeyboardButton(BUTTON_SAVE_WISHLIST)]]
    keyboard = [[InlineKeyboardButton(BUTTON_SAVE_WISHLIST, callback_data=CALLBACK_BUTTON11_SAVE_WISHLIST)]]
    welcome_speech = context.user_data[WELCOME_SPEECH]
    thanks_speech = context.user_data[THANKS_SPEECH]
    foundation0 = context.user_data[FOUNDATION_0]
    method0 = context.user_data[METHOD_0]
    if n_founds == 1:
        reply_text = print_1_fund(name, welcome_speech, foundation0, method0, thanks_speech)
    if n_founds == 2:
        foundation1 = context.user_data[FOUNDATION_1]
        method1 = context.user_data[METHOD_1]
        reply_text = print_2_funds(name, welcome_speech, foundation0, method0, foundation1, method1, thanks_speech)
    if n_founds == 3:
        foundation1 = context.user_data[FOUNDATION_1]
        method1 = context.user_data[METHOD_1]
        foundation2 = context.user_data[FOUNDATION_2]
        method2 = context.user_data[METHOD_2]
        reply_text = print_3_funds(name, welcome_speech, foundation0, method0, foundation1, method1, foundation2, method2, thanks_speech)
    update.message.reply_text(
        text=f"{reply_text}\nЕсли все верно нажмите <b>Сохранить вишлист</b>. Для отмены - /cancel",
        reply_markup=InlineKeyboardMarkup(keyboard, one_time_keyboard=True),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )

    return CONFIRM

@debug_request
def finish_creating_handler(update: Update, context: CallbackContext):
    context.user_data[WISH_MODE] = 'False'
    context.user_data[FROM_MODE] = 'False'
    context.user_data[DELETE_MODE] = 'False'
    user = update.effective_user
    name = context.user_data[NAME]
    foundation0 = context.user_data[FOUNDATION_0]
    method0 = context.user_data[METHOD_0]
    n_founds = context.user_data[N_FOUNDS]
    welcome_speech = context.user_data[WELCOME_SPEECH]
    thanks_speech = context.user_data[THANKS_SPEECH]
    if n_founds == 1:
        foundation1 = 'None'
        method1 = 'None'
        foundation2 = 'None'
        method2 = 'None'
    if n_founds == 2:
        foundation1 = context.user_data[FOUNDATION_1]
        method1 = context.user_data[METHOD_1]
        foundation2 = 'None'
        method2 = 'None'
    if n_founds == 3:
        foundation1 = context.user_data[FOUNDATION_1]
        method1 = context.user_data[METHOD_1]
        foundation2 = context.user_data[FOUNDATION_2]
        method2 = context.user_data[METHOD_2]
    if name:
        if foundation0:
            if method0:
                add_message(
                    user_id=user.id,
                    name=name,
                    namelowreg=name.lower(),
                    welcome_speech=welcome_speech,
                    foundation0=foundation0,
                    method0=method0,
                    foundation1=foundation1,
                    method1=method1,
                    foundation2=foundation2,
                    method2=method2,
                    thanks_speech=thanks_speech,
                    n_founds=n_founds
                )
    update.callback_query.bot.send_message(
        chat_id=update.callback_query.message.chat.id,
        text=f'''
Вишлист сохранен✔️
Отправьте вашим друзьям тег #{name}, и они смогут с помощью данного бота найти ваш вишлист и отправить вам открытку.

Чтобы найти или создать вишлист нажмите /start''',
        reply_markup=ReplyKeyboardRemove(),
        parse_mode=ParseMode.HTML
    )
    logger.info('user_data: %s', context.user_data)
    return ConversationHandler.END

@debug_request
def cancel_handler(update: Update, context: CallbackContext) -> int:
    context.user_data[WISH_MODE] = 'False'
    context.user_data[FROM_MODE] = 'False'
    context.user_data[DELETE_MODE] = 'False'
    logger.info(f'{update.message.chat.id} cancelled making wishlist')
    update.message.reply_text(
        text='Вы отменили создание вишлиста. Чтобы вернуться нажмите /start',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


@debug_request
def about(update: Update, context: CallbackContext):
    context.user_data[WISH_MODE] = 'False'
    context.user_data[FROM_MODE] = 'False'
    context.user_data[DELETE_MODE] = 'False'
    keyboard = [
        [InlineKeyboardButton(BUTTON1_FIND, callback_data=CALLBACK_BUTTON1_FIND)],
        [InlineKeyboardButton(BUTTON2_MAKE, callback_data=CALLBACK_BUTTON2_MAKE)],
        [InlineKeyboardButton(BUTTON3_SHOW, callback_data=CALLBACK_BUTTON3_SHOW)],
    ]
    update.message.reply_text(
        text='''
*Подробнее о боте «Вместо открытки»:*

Бот позволяет создать благотворительный вишлист: список организаций, в одну из которых ваши друзья могут сделать пожертвование в качестве подарка вам.
Благотворительный вишлист в красивом оформлении можно скопировать в инстаграм и другие соцсети.
Также бот может найти уже созданный вишлист и отправить поздравительную открытку автору вишлиста. Открытку можно отправить как анонимно так и с указанием имени отправителя.

Бот не хранит никакую информацию об отправителях открыток. Когда вы взаимодейтвуете с чьим-то вишлистом ваше имя нигде не отображается. Иными словами, даже авторы бота не могут узнать кем отправлены анонимные открытки.

Большое спасибо художникам [66hellena66](https://www.instagram.com/66hellena66/) и [Студия логотипов Станислава Гора](http://logotype.su)
Телеграм создателей бота - [@neverending_why](@neverending_why). Вы можете написать нам если увидели ошибку или хотите что-то улучшить в работе бота. Мы рады любым предложениям и замечаниям.🤍

*Выберите режим:*
''',
        reply_markup=InlineKeyboardMarkup(keyboard, one_time_keyboard=True),
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True
    )


def main():
    logger.info('Start bot')


    req = Request(
        connect_timeout=0.5,
        read_timeout=1.0,
    )
    bot = Bot(
        token=TG_TOKEN,
        request=req,
    )
    updater = Updater(
        bot=bot,
        use_context=True,
    )
    info = bot.get_me()
    logger.info(f'Bot info {info}')

    init_db()

    conv_create_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(do_create, pass_user_data=True),
        ],
        states={
            NAME: [
                MessageHandler(Filters.text, name_handler, pass_user_data=True),
            ],
            WELCOME_SPEECH: [
                MessageHandler(Filters.text, welcome_speech_handler, pass_user_data=True),
            ],
            FOUNDATION_0: [
                MessageHandler(Filters.text, foundation_0_handler, pass_user_data=True),
            ],
            METHOD_0: [
                MessageHandler(Filters.text, method_0_handler, pass_user_data=True),
            ],
            FOUNDATION_1: [
                MessageHandler(Filters.text, foundation_1_handler, pass_user_data=True),
                CommandHandler('skip', skip),
            ],
            METHOD_1: [
                MessageHandler(Filters.text, method_1_handler, pass_user_data=True),
            ],
            FOUNDATION_2: [
                MessageHandler(Filters.text, foundation_2_handler, pass_user_data=True),
                CommandHandler('skip', skip),
            ],
            METHOD_2: [
                MessageHandler(Filters.text, method_2_handler, pass_user_data=True),
            ],
            THANKS_SPEECH: [
                MessageHandler(Filters.text, thanks_speech_handler, pass_user_data=True),
            ],
            CONFIRM: [
                CallbackQueryHandler(finish_creating_handler, pass_user_data=True),
            ]
        },
        fallbacks=[
            CommandHandler('cancel', cancel_handler),
            CommandHandler('start', start_buttons_handler),
        ],
    )

    updater.dispatcher.add_handler(conv_create_handler)
    updater.dispatcher.add_handler(CommandHandler('start', start_buttons_handler))
    updater.dispatcher.add_handler(CommandHandler('about', about))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.photo, photo_handler))
    updater.dispatcher.add_handler(CommandHandler('mybday', set_timer_bday))
    updater.dispatcher.add_handler(CommandHandler('notify_all_users', notify_all_users_admin))

    updater.start_polling()
    updater.idle()
    logger.info('Stop bot')

if __name__ == '__main__':
    main()
