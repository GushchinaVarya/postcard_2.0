from telegram import Bot,  ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram.ext import ConversationHandler
from telegram.utils.request import Request
from db import *
import os
from appearance_funtions import *
from telegram import InputMediaPhoto, InputFile

from admin_functions import *
from pic_config import PIC_INFO, PIC_FOLDER, PICTURE_NAMES_DEMO

logger = getLogger(__name__)

NAME = 0
CONFIRM = 1
WELCOME_SPEECH = 2
FOUNDATION_0 = 3
METHOD_0 = 4
FOUNDATION_1 = 5
METHOD_1 = 6
FOUNDATION_2 = 7
METHOD_2 = 8
N_FOUNDS = 9
THANKS_SPEECH = 10
WISH = 11
FROM_WHOM = 12
FOUND_WISHLIST = 13
WISH_MODE = 14
FROM_MODE = 15
PIC_NUM = 16
DELETE_MODE = 17
REPLY_MODE = 18
REPLY_USER = 19
REPLY_WISHLIST = 20


@debug_request
def start_buttons_handler(update: Update, context: CallbackContext):
    context.user_data[WISH_MODE] = 'False'
    context.user_data[FROM_MODE] = 'False'
    context.user_data[DELETE_MODE] = 'False'
    context.user_data[REPLY_MODE] = 'False'
    chat_id = update.message.chat.id
    logger.info(f'chat_id {chat_id} started conversation')
    user_id_df = pd.read_csv(USER_IDS_FILE, index_col=0)
    if chat_id not in user_id_df.user_id.values:
        user_id_df = pd.concat([user_id_df,
                   pd.DataFrame([{'user_id': chat_id}])], ignore_index=True)
        user_id_df.to_csv(USER_IDS_FILE)
        logger.info(f'added to file of unique users chat_id {chat_id}')
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
        context.user_data[REPLY_MODE] = 'False'
        logger.info(f'chat_id {chat_id} wants to find wishlist')
        update.callback_query.bot.send_message(
            chat_id=chat_id,
            text='Введите название вишлиста используя знак #\n\nпример #ДеньРожденияИванаИванова01Янв2021',
            reply_markup=ReplyKeyboardRemove()
        )

    if init == CALLBACK_BUTTON3_SHOW:
        context.user_data[WISH_MODE] = 'False'
        context.user_data[FROM_MODE] = 'False'
        context.user_data[DELETE_MODE] = 'False'
        context.user_data[REPLY_MODE] = 'False'
        logger.info(f'chat_id {chat_id} wants to see its wishlists')
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
                n_founds = wishlist_i[10]
                welcome_speech = wishlist_i[2]
                name = wishlist_i[1]
                foundation0 = wishlist_i[3]
                foundation1 = wishlist_i[5]
                foundation2 = wishlist_i[7]
                wishlist_pic_name = print_wishlist_as_a_picture(n_founds, welcome_speech, name, foundation0, foundation1, foundation2, chat_id, picstyle='dark')
                update.callback_query.bot.send_message(
                    chat_id=chat_id,
                    text=name
                )
                update.callback_query.bot.sendPhoto(
                    chat_id=chat_id,
                    photo=open(wishlist_pic_name, 'rb'),
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
            os.system(f"(rm -rf {PIC_FOLDER + '*_' + str(chat_id) + '_' + PIC_INFO['4']['pic_name']})")
            os.system(f"(rm -rf {PIC_FOLDER + '*_' + str(chat_id) + '_' + PIC_INFO['5']['pic_name']})")
            os.system(f"(rm -rf {PIC_FOLDER + '*_' + str(chat_id) + '_' + PIC_INFO['6']['pic_name']})")
            logger.info(f'all temporary data for {chat_id} was successfully deleted')

    if init == CALLBACK_BUTTON2_MAKE:
        context.user_data[WISH_MODE] = 'False'
        context.user_data[FROM_MODE] = 'False'
        context.user_data[DELETE_MODE] = 'False'
        context.user_data[REPLY_MODE] = 'False'
        logger.info(f'{chat_id} started making wishlist')
        update.callback_query.bot.send_message(
            chat_id=chat_id,
            text='''
<b>Придумайте имя вашего вишлиста.</b>
Одно слово без пробелов и знаков. Пример ДеньРожденияИванаИванова01Янв2021

Отменить создание вишлиста - /cancel''',
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=ParseMode.HTML
        )
        return NAME

    if init == CALLBACK_BUTTON4_GENERATE_POSTCARD:
        context.user_data[WISH_MODE] = 'False'
        context.user_data[FROM_MODE] = 'False'
        context.user_data[DELETE_MODE] = 'False'
        context.user_data[REPLY_MODE] = 'False'
        try:
            found_wishlist = context.user_data[FOUND_WISHLIST]
            logger.info(f'{chat_id} started generating postcard for wishlist {found_wishlist}')
            keyboard = [
                [InlineKeyboardButton(BUTTON_PIC0, callback_data=CALLBACK_BUTTON_PIC0),
                 InlineKeyboardButton(BUTTON_PIC1, callback_data=CALLBACK_BUTTON_PIC1)],
                [InlineKeyboardButton(BUTTON_PIC2, callback_data=CALLBACK_BUTTON_PIC2),
                 InlineKeyboardButton(BUTTON_PIC3, callback_data=CALLBACK_BUTTON_PIC3)]
            ]
            update.callback_query.bot.send_message(
                chat_id=chat_id,
                text=f'<b>Вы совершили пожертвование! Давайте порадуем автора вишлиста и отправим ему открытку!</b>',
                parse_mode=ParseMode.HTML
            )
            message_to_del = context.bot.send_message(
                chat_id=chat_id,
                text='⏳Готовим варианты открыток...',
            )
            context.bot.sendPhoto(
                chat_id=chat_id,
                photo=open(PIC_FOLDER + PICTURE_NAMES_DEMO[0], 'rb'),
            )
            delete_flag = 0
            update.callback_query.bot.send_message(
                chat_id=chat_id,
                text=f'Выберите внешний вид открытки',
                reply_markup=InlineKeyboardMarkup(keyboard, one_time_keyboard=True),
                parse_mode=ParseMode.HTML
            )
            delete_flag = 1
            if delete_flag == 1:
                context.bot.delete_message(
                    chat_id=chat_id,
                    message_id=message_to_del.message_id
                )
        except:
            logger.info(f'{chat_id} started generating postcard but no wishlist in ram')
            update.callback_query.bot.send_message(
                chat_id=chat_id,
                text='Кажется мы слишком давно не общались😔 Простите, но я забыл о чем мы говорили. Пожалуйста нажмите /start и начните сначала'
            )

    if init == CALLBACK_BUTTON_PIC0:
        context.user_data[WISH_MODE] = 'True'
        context.user_data[FROM_MODE] = 'False'
        context.user_data[DELETE_MODE] = 'False'
        context.user_data[REPLY_MODE] = 'False'
        context.user_data[PIC_NUM] = 0
        logger.info(f'{chat_id} choose pic0')
        try:
            found_wishlist = context.user_data[FOUND_WISHLIST]
            WISH_LIMIT = PIC_INFO['0']['lenths_wish'][-1]
            update.callback_query.bot.send_message(
                chat_id=chat_id,
                text=f'Введите небольшое (до {WISH_LIMIT} символов) пожелание\nнапример: Счастья здоровья',
                parse_mode=ParseMode.HTML
            )
        except:
            logger.info(f'{chat_id} started chose pic0 but no wishlist in ram')
            update.callback_query.bot.send_message(
                chat_id=chat_id,
                text='Кажется мы слишком давно не общались😔 Простите, но я забыл о чем мы говорили. Пожалуйста нажмите /start и начните сначала'
            )


    if init == CALLBACK_BUTTON_PIC1:
        context.user_data[WISH_MODE] = 'True'
        context.user_data[FROM_MODE] = 'False'
        context.user_data[DELETE_MODE] = 'False'
        context.user_data[REPLY_MODE] = 'False'
        context.user_data[PIC_NUM] = 1
        logger.info(f'{chat_id} choose pic1')
        try:
            found_wishlist = context.user_data[FOUND_WISHLIST]
            WISH_LIMIT = PIC_INFO['1']['lenths_wish'][-1]
            update.callback_query.bot.send_message(
                chat_id=chat_id,
                text=f'Введите небольшое (до {WISH_LIMIT} символов) пожелание\nнапример: Счастья здоровья',
                parse_mode=ParseMode.HTML
            )
        except:
            logger.info(f'{chat_id} started chose pic1 but no wishlist in ram')
            update.callback_query.bot.send_message(
                chat_id=chat_id,
                text='Кажется мы слишком давно не общались😔 Простите, но я забыл о чем мы говорили. Пожалуйста нажмите /start и начните сначала'
            )

    if init == CALLBACK_BUTTON_PIC2:
        context.user_data[WISH_MODE] = 'True'
        context.user_data[FROM_MODE] = 'False'
        context.user_data[DELETE_MODE] = 'False'
        context.user_data[REPLY_MODE] = 'False'
        context.user_data[PIC_NUM] = 2
        logger.info(f'{chat_id} choose pic2')
        try:
            found_wishlist = context.user_data[FOUND_WISHLIST]
            WISH_LIMIT = PIC_INFO['2']['lenths_wish'][-1]
            update.callback_query.bot.send_message(
                chat_id=chat_id,
                text=f'Введите небольшое (до {WISH_LIMIT} символов) пожелание\nнапример: Счастья здоровья',
                parse_mode=ParseMode.HTML
            )
        except:
            logger.info(f'{chat_id} started chose pic2 but no wishlist in ram')
            update.callback_query.bot.send_message(
                chat_id=chat_id,
                text='Кажется мы слишком давно не общались😔 Простите, но я забыл о чем мы говорили. Пожалуйста нажмите /start и начните сначала'
            )

    if init == CALLBACK_BUTTON_PIC3:
        context.user_data[WISH_MODE] = 'True'
        context.user_data[FROM_MODE] = 'False'
        context.user_data[DELETE_MODE] = 'False'
        context.user_data[REPLY_MODE] = 'False'
        context.user_data[PIC_NUM] = 3
        logger.info(f'{chat_id} choose pic3')
        try:
            found_wishlist = context.user_data[FOUND_WISHLIST]
            WISH_LIMIT = PIC_INFO['3']['lenths_wish'][-1]
            update.callback_query.bot.send_message(
                chat_id=chat_id,
                text=f'Введите небольшое (до {WISH_LIMIT} символов) пожелание\nнапример: Счастья здоровья',
                parse_mode=ParseMode.HTML
            )
        except:
            logger.info(f'{chat_id} started chose pic3 but no wishlist in ram')
            update.callback_query.bot.send_message(
                chat_id=chat_id,
                text='Кажется мы слишком давно не общались😔 Простите, но я забыл о чем мы говорили. Пожалуйста нажмите /start и начните сначала'
            )

    #if init == CALLBACK_BUTTON_8MARCH_PIC1:
    #    context.user_data[WISH_MODE] = 'True'
    #    context.user_data[FROM_MODE] = 'False'
    #    context.user_data[DELETE_MODE] = 'False'
    #    context.user_data[PIC_NUM] = 2
    #    logger.info(f'{chat_id} choose 8 march pic1')
    #    update.callback_query.bot.send_message(
    #        chat_id=chat_id,
    #        text=f'Введите небольшое (до {WISH_LIMIT} символов) пожелание\nнапример: Счастья здоровья',
    #        parse_mode=ParseMode.HTML
    #    )

    #if init == CALLBACK_BUTTON_8MARCH_PIC2:
    #    context.user_data[WISH_MODE] = 'True'
    #    context.user_data[FROM_MODE] = 'False'
    #    context.user_data[DELETE_MODE] = 'False'
    #    context.user_data[PIC_NUM] = 3
    #    logger.info(f'{chat_id} choose 8 march pic2')
    #    update.callback_query.bot.send_message(
    #        chat_id=chat_id,
    #        text=f'Введите небольшое (до {WISH_LIMIT} символов) пожелание\nнапример: Счастья здоровья',
    #        parse_mode=ParseMode.HTML
    #    )

    if init == CALLBACK_BUTTON6_ADD_NAME:
        context.user_data[WISH_MODE] = 'False'
        context.user_data[FROM_MODE] = 'True'
        context.user_data[DELETE_MODE] = 'False'
        context.user_data[REPLY_MODE] = 'False'
        logger.info(f'{chat_id} writing from')
        try:
            found_wishlist = context.user_data[FOUND_WISHLIST]
            pic_num = context.user_data[PIC_NUM]
            wish = context.user_data[WISH]
            update.callback_query.bot.send_message(
                chat_id=chat_id,
                text='Введите короткую подпись\nнапример: Oт твоей лучшей подруги',
                parse_mode=ParseMode.HTML
            )
        except:
            logger.info(f'{chat_id} started chose writing from but no wishlist in ram')
            update.callback_query.bot.send_message(
                chat_id=chat_id,
                text='Кажется мы слишком давно не общались😔 Простите, но я забыл о чем мы говорили. Пожалуйста нажмите /start и начните сначала'
            )

    elif init == CALLBACK_BUTTON5_ANONYMOUS_SEND:
        context.user_data[FROM_MODE] = 'False'
        context.user_data[WISH_MODE] = 'False'
        context.user_data[DELETE_MODE] = 'False'
        context.user_data[REPLY_MODE] = 'False'
        logger.info(f'{chat_id} chose anonymous sending')
        try:
            found_wishlist = context.user_data[FOUND_WISHLIST]
            pic_num = context.user_data[PIC_NUM]
            wish = context.user_data[WISH]
            keyboard = [
                [InlineKeyboardButton(BUTTON7_ADD_SCREENSHOT, callback_data=CALLBACK_BUTTON7_ADD_SCREENSHOT)],
                [InlineKeyboardButton(BUTTON8_NO_SCREENSHOT, callback_data=CALLBACK_BUTTON8_NO_SCREENSHOT)]
            ]
            pic_name = PIC_FOLDER+'wish_'+str(chat_id)+'_'+PIC_INFO[str(context.user_data[PIC_NUM])]['pic_name']
            update.callback_query.bot.sendPhoto(
                chat_id=chat_id,
                photo=open(pic_name, 'rb'),
            )
            update.callback_query.bot.send_message(
                chat_id=chat_id,
                text=f"Предпросмотр открытки ⬆️ \n(Ваша открытка будет отправлена анонимно)",
                reply_markup=InlineKeyboardMarkup(keyboard, one_time_keyboard=True),
            )
        except:
            logger.info(f'{chat_id} started chose anonymos send but no wishlist in ram')
            update.callback_query.bot.send_message(
                chat_id=chat_id,
                text='Кажется мы слишком давно не общались😔 Простите, но я забыл о чем мы говорили. Пожалуйста нажмите /start и начните сначала'
            )

    elif init == CALLBACK_BUTTON7_ADD_SCREENSHOT:
        context.user_data[FROM_MODE] = 'False'
        context.user_data[WISH_MODE] = 'False'
        context.user_data[DELETE_MODE] = 'False'
        context.user_data[REPLY_MODE] = 'False'
        logger.info(f'{chat_id} sending screenshot')
        try:
            found_wishlist = context.user_data[FOUND_WISHLIST]
            pic_num = context.user_data[PIC_NUM]
            wish = context.user_data[WISH]
            update.callback_query.bot.send_message(
                chat_id=chat_id,
                text='Пришлите скриншот перевода. Можно отправить только одно изображение.'
            )
        except:
            logger.info(f'{chat_id} started tries to add screenshot but no wishlist in ram')
            update.callback_query.bot.send_message(
                chat_id=chat_id,
                text='Кажется мы слишком давно не общались😔 Простите, но я забыл о чем мы говорили. Пожалуйста нажмите /start и начните сначала'
            )

    elif init == CALLBACK_BUTTON8_NO_SCREENSHOT:
        context.user_data[WISH_MODE] = 'False'
        context.user_data[FROM_MODE] = 'False'
        context.user_data[DELETE_MODE] = 'False'
        context.user_data[REPLY_MODE] = 'False'
        logger.info(f'{chat_id} chose no screenshot')
        try:
            wishlist = find_wishlist(namelowreg=(context.user_data[FOUND_WISHLIST]).lower(), limit=1)
            wishlist_author_user_id = wishlist[0][0]
            wishlist_thanks_message = wishlist[0][9]
            bot = update.callback_query.bot
            if os.path.exists(PIC_FOLDER+'from_'+str(chat_id)+'_'+PIC_INFO[str(context.user_data[PIC_NUM])]['pic_name']):
                pic_name = PIC_FOLDER+'from_'+str(chat_id)+'_'+PIC_INFO[str(context.user_data[PIC_NUM])]['pic_name']
            else:
                pic_name = PIC_FOLDER+'wish_'+str(chat_id)+'_'+PIC_INFO[str(context.user_data[PIC_NUM])]['pic_name']
            bot.send_message(
                chat_id=wishlist_author_user_id,
                text=f'💌 ВАМ НОВАЯ ОТКРЫТКА!💌 \n\n\n',
            )
            callback_button_name = 'callback_button_reply|'+str(chat_id)+'|'+str(datetime.datetime.now())[:19]
            logger.info(f'PLACE {callback_button_name}')
            reply_buttons_df = pd.read_csv(REPLY_BUTTONS_FILE, index_col=0)
            reply_buttons_df = pd.concat([reply_buttons_df, pd.DataFrame([{'callback_button_name': callback_button_name, 'wishlist': wishlist[0][1]}])], ignore_index=True)
            reply_buttons_df.to_csv(REPLY_BUTTONS_FILE)
            logger.info(f'button {callback_button_name} added to file of reply buttons chat_id')
            keyboard = [[InlineKeyboardButton(BUTTON11_REPLY_TO_POSTCARD, callback_data=callback_button_name)]]
            bot.sendPhoto(
                chat_id=wishlist_author_user_id,
                photo=open(pic_name, 'rb'),
                reply_markup=InlineKeyboardMarkup(keyboard, one_time_keyboard=True),
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
            os.system(f"(rm -rf {PIC_FOLDER + 'screen_' + str(chat_id) + '.png'})")
            os.system(f"(rm -rf {PIC_FOLDER + 'from_' + str(chat_id) + '_' + PIC_INFO[str(context.user_data[PIC_NUM])]['pic_name']})")
            os.system(f"(rm -rf {PIC_FOLDER + 'wish_' + str(chat_id) + '_' + PIC_INFO[str(context.user_data[PIC_NUM])]['pic_name']})")
            logger.info(f'all temporary data for {chat_id} was successfully deleted')
        except:
            logger.info(f'{chat_id} wants to send without screenshot but error occured')
            update.callback_query.bot.send_message(
                chat_id=chat_id,
                text='Что-то пошло не так😔 Пожалуйста нажмите /start и начните сначала'
            )

    elif init == CALLBACK_BUTTON9_READY:
        context.user_data[FROM_MODE] = 'False'
        context.user_data[WISH_MODE] = 'False'
        context.user_data[DELETE_MODE] = 'False'
        context.user_data[REPLY_MODE] = 'False'
        try:
            wishlist = find_wishlist(namelowreg=(context.user_data[FOUND_WISHLIST]).lower(), limit=1)
            wishlist_author_user_id = wishlist[0][0]
            wishlist_thanks_message = wishlist[0][9]
            if os.path.exists(PIC_FOLDER+'from_'+str(chat_id)+'_'+PIC_INFO[str(context.user_data[PIC_NUM])]['pic_name']):
                pic_name = PIC_FOLDER+'from_'+str(chat_id)+'_'+PIC_INFO[str(context.user_data[PIC_NUM])]['pic_name']
            else:
                pic_name = PIC_FOLDER+'wish_'+str(chat_id)+'_'+PIC_INFO[str(context.user_data[PIC_NUM])]['pic_name']
            bot = update.callback_query.bot
            callback_button_name = 'callback_button_reply|' + str(chat_id) + '|' + str(datetime.datetime.now())[:19]
            reply_buttons_df = pd.read_csv(REPLY_BUTTONS_FILE, index_col=0)
            reply_buttons_df = pd.concat([reply_buttons_df, pd.DataFrame([{'callback_button_name': callback_button_name, 'wishlist': wishlist[0][1]}])], ignore_index=True)
            reply_buttons_df.to_csv(REPLY_BUTTONS_FILE)
            logger.info(f'button {callback_button_name} added to file of reply buttons chat_id')
            keyboard = [[InlineKeyboardButton(BUTTON11_REPLY_TO_POSTCARD, callback_data=callback_button_name)]]
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
                reply_markup=InlineKeyboardMarkup(keyboard, one_time_keyboard=True),
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
            logger.info(f'{chat_id} successfully sent postcard to user {wishlist_author_user_id} pic {PIC_INFO[str(context.user_data[PIC_NUM])]}')
            os.system(f"(rm -rf {PIC_FOLDER+'screen_' + str(chat_id) + '.png'})")
            os.system(f"(rm -rf {PIC_FOLDER+'from_'+str(chat_id)+'_'+PIC_INFO[str(context.user_data[PIC_NUM])]['pic_name']})")
            os.system(f"(rm -rf {PIC_FOLDER+'wish_'+str(chat_id)+'_'+PIC_INFO[str(context.user_data[PIC_NUM])]['pic_name']})")
            logger.info(f'all temporary data for {chat_id} was successfully deleted')
        except:
            logger.info(f'{chat_id} wants to send postcard but error occured')
            update.callback_query.bot.send_message(
                chat_id=chat_id,
                text='Что-то пошло не так😔 Пожалуйста нажмите /start и начните сначала'
            )

    elif init == CALLBACK_BUTTON10_DELETE_WISHLIST:
        context.user_data[FROM_MODE] = 'False'
        context.user_data[WISH_MODE] = 'False'
        context.user_data[DELETE_MODE] = 'True'
        context.user_data[REPLY_MODE] = 'False'
        update.callback_query.bot.send_message(
            chat_id=chat_id,
            text=f"Введите название вишлиста который нужно удалить (просто имя без знака #)",
            reply_markup=ReplyKeyboardRemove(),
        )
    elif init in pd.read_csv(REPLY_BUTTONS_FILE, index_col=0).callback_button_name.values:
        context.user_data[FROM_MODE] = 'False'
        context.user_data[WISH_MODE] = 'False'
        context.user_data[DELETE_MODE] = 'False'
        context.user_data[REPLY_MODE] = 'True'
        context.user_data[REPLY_USER] = init.split('|')[1]
        reply_buttons_df = pd.read_csv(REPLY_BUTTONS_FILE, index_col=0)
        context.user_data[REPLY_WISHLIST] = reply_buttons_df[reply_buttons_df.callback_button_name == init].wishlist.values[-1]
        update.callback_query.bot.send_message(
            chat_id=chat_id,
            text=f"Введите сообщение. Оно придет пользователю от имени бота.",
            reply_markup=ReplyKeyboardRemove(),
        )
    elif init[:21] == 'callback_button_reply':
        context.user_data[FROM_MODE] = 'False'
        context.user_data[WISH_MODE] = 'False'
        context.user_data[DELETE_MODE] = 'False'
        context.user_data[REPLY_MODE] = 'False'
        update.callback_query.bot.send_message(
            chat_id=chat_id,
            text=f"К сожалению ответить на эту открытку уже нельзя, так как открытка была отправлена слишком давно.️",
            reply_markup=ReplyKeyboardRemove(),
        )

@debug_request
def message_handler(update: Update, context: CallbackContext):
    text = update.message.text
    user_id = update.message.chat.id
    chat_id = update.message.chat.id
    if text[0] == '#':
        try:
            if context.user_data[DELETE_MODE] == 'True':
                update.message.reply_text('Чтобы удалить вишлист введите его название без # . Вернуться в главное меню - /start')
                logger.info(f'{chat_id} tries to delete wishlist but wrote with #')
            else:
                wishlistname = text[1:]
                logger.info(f'{chat_id} tries to find wishlist with name {wishlistname}')
                wishlist = find_wishlist(namelowreg=wishlistname.lower(), limit=1)
                if wishlist:
                    context.user_data[FOUND_WISHLIST] = wishlistname
                    logger.info(f'{chat_id} successfully found wishlist with name {wishlistname}')
                    keyboard = [[InlineKeyboardButton(BUTTON4_GENERATE_POSTCARD,
                                                      callback_data=CALLBACK_BUTTON4_GENERATE_POSTCARD)]]
                    reply_text = print_wishlist(wishlist[0])
                    update.message.reply_text(
                        text=f'''
Вишлист <b>{wishlist[0][1]}</b> найден!✔️

️{reply_text}

<b>Если вы хотите поздравить автора пожертвуйте в одну из этих организаций и нажмите кнопку "Я совершил пожертвование!"</b>''',
                        reply_markup=InlineKeyboardMarkup(keyboard, one_time_keyboard=True),
                        parse_mode=ParseMode.HTML,
                        disable_web_page_preview=True
                    )
                else:
                    logger.info(f'no wishlist with name {wishlistname}')
                    update.message.reply_text(
                        text='Вишлист c таким именем не найден. Введите другой вишлист.',
                        reply_markup=ReplyKeyboardRemove()
                    )
        except:
            context.user_data[FROM_MODE] = 'False'
            context.user_data[WISH_MODE] = 'False'
            context.user_data[DELETE_MODE] = 'False'
            context.user_data[REPLY_MODE] = 'False'
            wishlistname = text[1:]
            logger.info(f'{chat_id} tries to find wishlist with name {wishlistname}')
            wishlist = find_wishlist(namelowreg=wishlistname.lower(), limit=1)
            if wishlist:
                context.user_data[FOUND_WISHLIST] = wishlistname
                logger.info(f'{chat_id} successfully found wishlist with name {wishlistname}')
                keyboard = [[InlineKeyboardButton(BUTTON4_GENERATE_POSTCARD, callback_data=CALLBACK_BUTTON4_GENERATE_POSTCARD)]]
                reply_text = print_wishlist(wishlist[0])
                update.message.reply_text(
                    text=f'''
Вишлист <b>{wishlist[0][1]}</b> найден!✔️

{reply_text}

<b>Если вы хотите поздравить автора пожертвуйте в одну из этих организаций и нажмите кнопку "Я совершил пожертвование!"</b>''',
                    reply_markup=InlineKeyboardMarkup(keyboard, one_time_keyboard=True),
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True
                )
            else:
                logger.info(f'no wishlist with name {wishlistname}')
                update.message.reply_text(
                    text='Вишлист c таким именем не найден. Введите другой вишлист.',
                    reply_markup=ReplyKeyboardRemove()
                )

    else:
        try:
            if context.user_data[WISH_MODE] == 'True':
                wishtext = text
                if len(wishtext) > PIC_INFO[str(context.user_data[PIC_NUM])]['lenths_wish'][-1]:
                    logger.info(f'{chat_id} made too long wish')
                    update.message.reply_text(
                        text="Слишком длинное пожелание. Введите пожалуйста пожелание покороче😊"
                    )
                else:
                    context.user_data[WISH] = wishtext
                    keyboard = [
                        [InlineKeyboardButton(BUTTON5_ANONYMOUS_SEND, callback_data=CALLBACK_BUTTON5_ANONYMOUS_SEND)],
                        [InlineKeyboardButton(BUTTON6_ADD_NAME, callback_data=CALLBACK_BUTTON6_ADD_NAME)],
                    ]
                    write_text_2(wishtext, context.user_data[PIC_NUM], user_id, 'wish')
                    context.bot.sendPhoto(
                        chat_id=update.message.chat.id,
                        photo=open(PIC_FOLDER+'wish_'+str(user_id)+'_'+PIC_INFO[str(context.user_data[PIC_NUM])]['pic_name'], 'rb'),
                    )
                    update.message.reply_text(
                        text=f"Предпросмотр открытки ⬆️\nЕсли передумали и хотите поменять пожелание, введите его заново. Либо выберите нужна ли на открытке подпись⬇️",
                        reply_markup=InlineKeyboardMarkup(keyboard, one_time_keyboard=True),
                    )
                    logger.info(f'{chat_id} successfully wrote wish with length {len(wishtext)}')
            elif context.user_data[FROM_MODE] == 'True':
                from_whom = text
                if len(from_whom) > PIC_INFO[str(context.user_data[PIC_NUM])]['lenths_from'][-1]:
                    logger.info(f'{chat_id} made too long from')
                    update.message.reply_text(
                        text="Слишком длинная подпись. Введите пожалуйста подпись покороче😊"
                    )
                else:
                    context.user_data[FROM_WHOM] = from_whom
                    keyboard = [
                        [InlineKeyboardButton(BUTTON7_ADD_SCREENSHOT, callback_data=CALLBACK_BUTTON7_ADD_SCREENSHOT)],
                        [InlineKeyboardButton(BUTTON8_NO_SCREENSHOT, callback_data=CALLBACK_BUTTON8_NO_SCREENSHOT)]
                    ]
                    write_text_2(from_whom, context.user_data[PIC_NUM], user_id, 'from')
                    context.bot.sendPhoto(
                        chat_id=update.message.chat.id,
                        photo=open(PIC_FOLDER+'from_'+str(user_id)+'_'+PIC_INFO[str(context.user_data[PIC_NUM])]['pic_name'], 'rb'),
                    )
                    update.message.reply_text(
                        text=f"Предпросмотр открытки ⬆️\nЕсли передумали и хотите поменять подпись, введите ее заново. Либо выберите нужно ли прикреплять скриншот.",
                        reply_markup=InlineKeyboardMarkup(keyboard, one_time_keyboard=True),
                    )
                    logger.info(f'{chat_id} successfully wrote from with length {len(from_whom)}')
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
            elif context.user_data[REPLY_MODE] == 'True':
                reply_message = text
                reply_user_id = int(context.user_data[REPLY_USER])
                reply_wishlist = context.user_data[REPLY_WISHLIST]
                context.bot.send_message(
                    chat_id=reply_user_id,
                    text=f'''
📩Вам новое ообщение от автора вишлиста {reply_wishlist} в ответ на вашу открытку:

"<b><i>{reply_message}</i></b>"

Обратите внимание, что если вы отправляли открытку анонимно, то автор вишлиста не знает кому пришло это сообщение.
''',
                    parse_mode=ParseMode.HTML,
                )
                update.message.reply_text('Сообщение отправлено')

            else:
                update.message.reply_text('Неверный формат ввода')
        except:
            context.user_data[FROM_MODE] = 'False'
            context.user_data[WISH_MODE] = 'False'
            context.user_data[DELETE_MODE] = 'False'
            update.message.reply_text('Кажется мы слишком давно не общались😔 Простите, но я забыл о чем мы говорили. Пожалуйста нажмите /start и начните сначала')


def photo_handler(update: Update, context: CallbackContext):
    context.user_data[WISH_MODE] = 'False'
    context.user_data[FROM_MODE] = 'False'
    context.user_data[DELETE_MODE] = 'False'
    context.user_data[REPLY_MODE] = 'False'
    name_screenshot = PIC_FOLDER+'screen_'+str(update.message.chat.id)+'.png'
    photo_file = update.message.photo[-1].get_file()
    photo_file.download(name_screenshot)
    logger.info(f'{update.message.chat.id} added screenshot {name_screenshot}')
    keyboard = [[InlineKeyboardButton(BUTTON9_READY, callback_data=CALLBACK_BUTTON9_READY)]]
    update.message.reply_text(
        text='Скриншот успешно добавлен.\n<b>Отлично! Поздравление готово! Отправить открытку и скриншот автору вишлиста?</b>',
        reply_markup=InlineKeyboardMarkup(keyboard, one_time_keyboard=True),
        parse_mode=ParseMode.HTML
    )

@debug_request
def name_handler(update: Update, context: CallbackContext):
    context.user_data[WISH_MODE] = 'False'
    context.user_data[FROM_MODE] = 'False'
    context.user_data[DELETE_MODE] = 'False'
    context.user_data[REPLY_MODE] = 'False'
    name = update.message.text
    if len(name.split(' ')) > 1:
        update.message.reply_text(
            text='Пожалуйста введите название без пробелов.',
            parse_mode=ParseMode.HTML,
        )
    elif len(name) > 32:
        update.message.reply_text(
            text='Слишком длинное название. Пожалуйста придумайте более короткое имя вишлиста. Так вашим друзьям будет проще найти ваш вишлист и поздравить вас.',
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
    welcome_speech = update.message.text
    if len(welcome_speech) > PIC_INFO['6']['lenths_author'][-1]:
        update.message.reply_text(
            text='Слишком длинное вступление. Оно будет очень мелко смотреться на картинке. Пожалуйста придумайте более короткое обращение.',
            parse_mode=ParseMode.HTML,
        )
    else:
        context.user_data[WELCOME_SPEECH] = welcome_speech
        update.message.reply_text(
            text='Введите название первой благотворительной организации. Например: фонд защиты животных "WWF"\n\nОтменить создание вишлиста - /cancel',
            parse_mode=ParseMode.HTML,
        )
        return FOUNDATION_0

@debug_request
def foundation_0_handler(update: Update, context: CallbackContext):
    foundation_0 = update.message.text
    if len(foundation_0) > PIC_INFO['6']['lenths_fund1'][-1]:
        update.message.reply_text(
            text='Слишком длинный текст, он будет очень мелко смортреться на картинке. Пожалуйства введите только само название фонда или сформулируйте его более кратко.',
            parse_mode=ParseMode.HTML,
        )
    else:
        context.user_data[FOUNDATION_0] = foundation_0
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
    foundation_1 = update.message.text
    if len(foundation_1) > PIC_INFO['6']['lenths_fund2'][-1]:
        update.message.reply_text(
            text='Слишком длинный текст, он будет очень мелко смортреться на картинке. Пожалуйства введите только само название фонда или сформулируйте его более кратко.',
            parse_mode=ParseMode.HTML,
        )
    else:
        context.user_data[FOUNDATION_1] = foundation_1
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
    foundation_2 = update.message.text
    if len(foundation_2) > PIC_INFO['6']['lenths_fund3'][-1]:
        update.message.reply_text(
            text='Слишком длинный текст, он будет очень мелко смортреться на картинке. Пожалуйства введите только само название фонда или сформулируйте его более кратко.',
            parse_mode=ParseMode.HTML,
        )
    else:
        context.user_data[FOUNDATION_2] = foundation_2
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
Спасибо вам за пожертвование. Вы классные. Ваш Иван Иванов

Отменить создание вишлиста - /cancel
''',
        parse_mode=ParseMode.HTML
    )
    return THANKS_SPEECH

@debug_request
def thanks_speech_handler(update: Update, context: CallbackContext) -> int:
    context.user_data[WISH_MODE] = 'False'
    context.user_data[FROM_MODE] = 'False'
    context.user_data[DELETE_MODE] = 'False'
    context.user_data[REPLY_MODE] = 'False'
    user = update.effective_user

    update.message.reply_text(
        text=f"Поздравляем! Вы создали вишлист!",
        parse_mode=ParseMode.HTML,
    )

    message_to_del = context.bot.send_message(
        chat_id=int(user.id),
        text=f"⏳Готовим красивые картинки с вашим вишлистом... ",
        parse_mode=ParseMode.HTML
    )

    delete_flag = 0
    logger.info(f'delteflag={delete_flag}, message id{message_to_del.message_id}')

    name = context.user_data[NAME]
    n_founds = context.user_data[N_FOUNDS]
    foundation0 = context.user_data[FOUNDATION_0]
    method0 = context.user_data[METHOD_0]
    welcome_speech = context.user_data[WELCOME_SPEECH]
    thanks_speech = update.message.text
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

    # БЛОК СОЗДАНИЯ КАРТИНКИ
    wishlist_pic_name_white = print_wishlist_as_a_picture(n_founds, welcome_speech, name, foundation0, foundation1,
                                                          foundation2, user.id, picstyle='dark')
    wishlist_pic_name_dark = print_wishlist_as_a_picture(n_founds, welcome_speech, name, foundation0, foundation1,
                                                         foundation2, user.id, picstyle='white')
    context.bot.send_media_group(
        chat_id=user.id,
        media=[InputMediaPhoto(open(wishlist_pic_name_white, 'rb')),
               InputMediaPhoto(open(wishlist_pic_name_dark, 'rb'))]
    )
    os.system(f"(rm -rf {PIC_FOLDER + '*_' + str(user.id) + '_' + PIC_INFO['4']['pic_name']})")
    os.system(f"(rm -rf {PIC_FOLDER + '*_' + str(user.id) + '_' + PIC_INFO['5']['pic_name']})")
    os.system(f"(rm -rf {PIC_FOLDER + '*_' + str(user.id) + '_' + PIC_INFO['6']['pic_name']})")
    os.system(f"(rm -rf {PIC_FOLDER + '*_' + str(user.id) + '_' + PIC_INFO['7']['pic_name']})")
    os.system(f"(rm -rf {PIC_FOLDER + '*_' + str(user.id) + '_' + PIC_INFO['8']['pic_name']})")
    os.system(f"(rm -rf {PIC_FOLDER + '*_' + str(user.id) + '_' + PIC_INFO['9']['pic_name']})")
    logger.info(f'all temporary data for {user.id} was successfully deleted')

    delete_flag = 1
    if delete_flag == 1:
        context.bot.delete_message(
            chat_id=int(user.id),
            message_id=message_to_del.message_id
        )

    update.message.reply_text(
            text=f'''
<b>Отправьте друзьям тег #{name} и ссылку на бота https://t.me/MoreThanPostcardBot
Либо поделитесь любой из этих картинок в соцсетях. </b>

Теперь любой человек, который узнает о вашем вишлисте, сможет ввести #{name} в боте и увидеть этот вишлист в полном текстовом виде со всеми ссылками и методами оплаты.

Чтобы найти или создать другой вишлист нажмите /start
    ''',
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )

    #if n_founds == 1:
    #    reply_text = print_1_fund(name, welcome_speech, foundation0, method0, thanks_speech)
    #if n_founds == 2:
    #    foundation1 = context.user_data[FOUNDATION_1]
    #    method1 = context.user_data[METHOD_1]
    #    reply_text = print_2_funds(name, welcome_speech, foundation0, method0, foundation1, method1, thanks_speech)
    #if n_founds == 3:
    #    foundation1 = context.user_data[FOUNDATION_1]
    #    method1 = context.user_data[METHOD_1]
    #    foundation2 = context.user_data[FOUNDATION_2]
    #    method2 = context.user_data[METHOD_2]
    #    reply_text = print_3_funds(name, welcome_speech, foundation0, method0, foundation1, method1, foundation2, method2, thanks_speech)
    #update.message.reply_text(
    #    text=f"{reply_text}",
    #    parse_mode=ParseMode.HTML,
    #    disable_web_page_preview=True
    #)

    return ConversationHandler.END

@debug_request
def cancel_handler(update: Update, context: CallbackContext) -> int:
    context.user_data[WISH_MODE] = 'False'
    context.user_data[FROM_MODE] = 'False'
    context.user_data[DELETE_MODE] = 'False'
    context.user_data[REPLY_MODE] = 'False'
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
    context.user_data[REPLY_MODE] = 'False'
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

Также бот может найти уже созданный вишлист и отправить поздравительную открытку его автору. Открытку можно отправить как анонимно так и с указанием имени отправителя.

Бот не хранит никакую информацию об отправителях открыток. Когда вы взаимодейтвуете с чьим-то вишлистом ваше имя нигде не отображается. Иными словами, даже авторы бота не могут узнать кем отправлены анонимные открытки.

*Как пользоваться ботом?*
[Как создать вишлист](https://telegra.ph/Vmesto-Otkrytki-05-15)
[Как отправить открытку](https://telegra.ph/Vmesto-Otkrytki-05-15-2)

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
            ]
        },
        fallbacks=[
            CommandHandler('cancel', cancel_handler),
            CommandHandler('start', start_buttons_handler)
        ],
    )

    updater.dispatcher.add_handler(conv_create_handler)
    updater.dispatcher.add_handler(CommandHandler('start', start_buttons_handler))
    updater.dispatcher.add_handler(CommandHandler('about', about))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.photo, photo_handler))
    updater.dispatcher.add_handler(CommandHandler('mybday', set_timer_bday))
    updater.dispatcher.add_handler(CommandHandler('stopreminder', remove_timer_bday))
    updater.dispatcher.add_handler(CommandHandler('notify_all_users', notify_all_users_admin))
    updater.dispatcher.add_handler(CommandHandler('reset_all_timers', reset_all_timers_admin))
    updater.dispatcher.add_handler(CommandHandler('show_jobs_by_name', show_jobs_by_name))

    updater.start_polling()
    updater.idle()
    logger.info('Stop bot')

if __name__ == '__main__':
    main()
