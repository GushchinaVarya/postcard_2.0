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

@ensure_connection
def init_db(conn, force: bool = False):
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

@ensure_connection
def add_message(conn, user_id: int, name: str, welcome_speech:str, foundation0:str, method0:str, foundation1:str, method1:str, foundation2:str, method2:str, thanks_speech:str, n_founds:int):
    c = conn.cursor()
    c.execute('INSERT INTO user_wishlist (user_id, name, welcome_speech, foundation0, method0, foundation1, method1, foundation2, method2, thanks_speech, n_founds) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (user_id, name, welcome_speech, foundation0, method0, foundation1, method1, foundation2, method2, thanks_speech, n_founds))
    conn.commit()

@ensure_connection
def count_messages(conn, user_id: int):
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM user_wishlist WHERE user_id = ?', (user_id, ))
    (res,) = c.fetchone()
    return res

@ensure_connection
def find_wishlist(conn, name: int, limit: int = 10):
    c = conn.cursor()
    c.execute('SELECT user_id, name, welcome_speech, foundation0, method0, foundation1, method1, foundation2, method2, thanks_speech, n_founds FROM user_wishlist WHERE name = ? ORDER BY id DESC LIMIT ?', (name, limit))
    return c.fetchall()

@ensure_connection
def wishlist_name_available(conn, name: str):
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM user_wishlist WHERE name = ?', (name,))
    (res,) = c.fetchone()
    if res == 0:
        return True
    else:
        return False

@ensure_connection
def show_my_wishlists(conn, user_id: int, limit: int = 1):
    c = conn.cursor()
    c.execute('SELECT user_id, name, welcome_speech, foundation0, method0, foundation1, method1, foundation2, method2, thanks_speech, n_founds FROM user_wishlist WHERE user_id = ? ORDER BY id DESC LIMIT ?', (user_id, limit))
    return c.fetchall()