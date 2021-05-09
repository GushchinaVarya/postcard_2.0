from pic_config import PIC_INFO, PIC_FOLDER
from picture import write_text_2

from logger_debug import *
logger = getLogger(__name__)

@debug_request
def print_wishlist(wishlist):
    n_founds = wishlist[10]
    if n_founds == 1:
        print_result = f'''
⬜️#{wishlist[1]}⬜️\n
<b>{wishlist[2]}</b>\n
🔘️ {wishlist[3]}
Как пожертвовать: {wishlist[4]}\n'''
    if n_founds == 2:
        print_result = f'''
⬜️#{wishlist[1]}⬜️\n
<b>{wishlist[2]}</b>\n
🔘️ {wishlist[3]}
Как пожертвовать: {wishlist[4]}\n
🔘️{wishlist[5]}
Как пожертвовать: {wishlist[6]}\n'''
    if n_founds == 3:
        print_result = f'''
⬜️#{wishlist[1]}⬜️\n
<b>{wishlist[2]}</b>\n
🔘️ {wishlist[3]}
Как пожертвовать: {wishlist[4]}\n
🔘️{wishlist[5]}
Как пожертвовать: {wishlist[6]}\n
🔘️{wishlist[7]}
Как пожертвовать: {wishlist[8]}\n'''
    return print_result

@debug_request
def print_wishlist_with_thanks(wishlist_i):
    print_result = print_wishlist(wishlist_i)+f'\n\n<i>Сообщение которое друзья увидят только после отправки открытки:</i> {wishlist_i[9]}\n'
    return print_result

@debug_request
def print_1_fund(name: str, welcome_speech: str, foundation0: str, method0: str, thanks_speech:str):
    print_result = f'''
Ваш вишлист выглядит вот так:\n
⬜️#{name}⬜️\n
<b>{welcome_speech}</b>\n
🔘️ {foundation0}
Как пожертвовать: {method0}\n
<i>Сообщение которое друзья увидят только после отправки открытки:</i> {thanks_speech}\n
'''
    return print_result

@debug_request
def print_2_funds(name: str, welcome_speech: str, foundation0: str, method0: str, foundation1: str, method1: str, thanks_speech:str):
    print_result = f'''
Ваш вишлист выглядит вот так:\n
⬜️#{name}⬜️\n
<b>{welcome_speech}</b>\n
🔘️ {foundation0}
Как пожертвовать: {method0}\n
🔘️ {foundation1}
Как пожертвовать: {method1}\n
<i>Сообщение которое друзья увидят только после отправки открытки:</i> {thanks_speech}\n
'''
    return print_result

@debug_request
def print_3_funds(name: str, welcome_speech: str, foundation0: str, method0: str, foundation1: str, method1: str, foundation2: str, method2: str, thanks_speech:str):
    print_result = f'''
Ваш вишлист выглядит вот так:\n
⬜️#{name}⬜️\n
<b>{welcome_speech}</b>\n
🔘️ {foundation0}
Как пожертвовать: {method0}\n
🔘️ {foundation1}
Как пожертвовать: {method1}\n
🔘️ {foundation2}
Как пожертвовать: {method2}\n
<i>Сообщение которое друзья увидят только после отправки открытки:</i> {thanks_speech}\n
'''
    return print_result

@debug_request
def print_wishlist_as_a_picture(n_founds, welcome_speech, name, foundation0, foundation1, foundation2, user_id):
    discl = f'Чтобы пожертвовать и отправить мне открытку введите #{name} в telegtam-боте "Вместо Открытки"'
    if n_founds == 1:
        pic_num = 4
        write_text_2(welcome_speech, pic_num, user_id, 'author')
        write_text_2(f'#{name}', pic_num, user_id, 'tag')
        write_text_2(discl, pic_num, user_id, 'discl')
        write_text_2(foundation0, pic_num, user_id, 'fund1')
        wishlist_pic_name = PIC_FOLDER+'fund1_'+str(user_id)+'_'+PIC_INFO[str(pic_num)]['pic_name']
    if n_founds == 2:
        pic_num = 5
        write_text_2(welcome_speech, pic_num, user_id, 'author')
        write_text_2(f'#{name}', pic_num, user_id, 'tag')
        write_text_2(discl, pic_num, user_id, 'discl')
        write_text_2(foundation0, pic_num, user_id, 'fund1')
        write_text_2(foundation1, pic_num, user_id, 'fund2')
        wishlist_pic_name = PIC_FOLDER+'fund2_' + str(user_id) + '_' + PIC_INFO[str(pic_num)]['pic_name']
    if n_founds == 3:
        pic_num = 6
        write_text_2(welcome_speech, pic_num, user_id, 'author')
        write_text_2(f'#{name}', pic_num, user_id, 'tag')
        write_text_2(discl, pic_num, user_id, 'discl')
        write_text_2(foundation0, pic_num, user_id, 'fund1')
        write_text_2(foundation1, pic_num, user_id, 'fund2')
        write_text_2(foundation2, pic_num, user_id, 'fund3')
        wishlist_pic_name = PIC_FOLDER+'fund3_' + str(user_id) + '_' + PIC_INFO[str(pic_num)]['pic_name']
    return wishlist_pic_name