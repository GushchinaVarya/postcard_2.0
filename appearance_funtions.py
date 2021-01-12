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

def print_wishlist_with_thanks(wishlist_i):
    print_result = print_wishlist(wishlist_i)+f'\n\n<i>Сообщение которое друзья увидят только после отправки открытки:</i> {wishlist_i[9]}\n'
    return print_result


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