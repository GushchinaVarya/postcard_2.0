import sqlite3

__connection = None

def get_connection():
    global __connection
    if __connection is None:
        __connection = sqlite3.connect('wishlist.db')
    return __connection

def ensure_connection(func):
    def inner(*args, **kwargs):
        with sqlite3.connect('wishlist.db') as conn:
            kwargs['conn'] = conn
            res = func(*args, **kwargs)
        return res
    return inner

#@ensure_connection
def init_db(force: bool = False):
    conn = get_connection()
    c = conn.cursor()
    if force:
        c.execute('DROP TABLE IF EXISTS user_wishlist')
    c.execute('''
    CREATE TABLE IF NOT EXISTS user_wishlist (
        id              INTEGER PRIMARY KEY,
        user_id         INTEGER NOT NULL,
        name            TEXT NOT NULL,
        welcome_speech  TEXT NOT NULL,
        foundation0     TEXT NOT NULL,
        method0         TEXT NOT NULL,
        foundation1     TEXT NOT NULL,
        method1         TEXT NOT NULL,
        foundation2     TEXT NOT NULL,
        method2         TEXT NOT NULL,
        thanks_speech   TEXT NOT NULL,
        n_founds        INTEGER NOT NULL
    )
    '''
    )
    conn.commit()

#@ensure_connection
def add_message(user_id: int, name: str, welcome_speech:str, foundation0:str, method0:str, foundation1:str, method1:str, foundation2:str, method2:str, thanks_speech:str, n_founds:int):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO user_wishlist (user_id, name, welcome_speech, foundation0, method0, foundation1, method1, foundation2, method2, thanks_speech, n_founds) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (user_id, name, welcome_speech, foundation0, method0, foundation1, method1, foundation2, method2, thanks_speech, n_founds))
    conn.commit()

#@ensure_connection
def count_messages(user_id: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM user_wishlist WHERE user_id = ?', (user_id, ))
    (res,) = c.fetchone()
    return res

def find_wishlist(name: str, limit: int = 1):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT user_id, name, welcome_speech, foundation0, method0, foundation1, method1, foundation2, method2, thanks_speech, n_founds FROM user_wishlist WHERE name = ? ORDER BY id DESC LIMIT ?', (name, limit))
    return c.fetchall()

def wishlist_name_available(name: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM user_wishlist WHERE name = ?', (name,))
    (res,) = c.fetchone()
    if res == 0:
        return True
    else:
        return False

def show_my_wishlists(user_id: int, limit: int = 10):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT user_id, name, welcome_speech, foundation0, method0, foundation1, method1, foundation2, method2, thanks_speech, n_founds FROM user_wishlist WHERE user_id = ? ORDER BY id DESC LIMIT ?', (user_id, limit))
    return c.fetchall()

if __name__ == '__main__':
    #init_db(True)
    init_db(False)
    #add_message(user_id=97870197, name='ДеньРожденияВари13012020', welcome_speech='welcome_speech', foundation0='теплый дом', method0='вебсайт теплый-дом.рф', foundation1='foundation1', method1='method1', foundation2='foundation2', method2='method2', thanks_speech='thanks_speech', n_founds=1)

    r = count_messages(user_id=123)
    print(r)

    r = find_wishlist(name='TestUser', limit=1)
    print(r)

    print('Un', wishlist_name_available('Un'))

    r = show_my_wishlists(user_id=10, limit=10)
    print(len(r))
    for i in r:
        print (i)