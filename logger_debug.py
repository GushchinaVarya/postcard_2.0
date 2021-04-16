from config import *
logger = getLogger(__name__)

def debug_request(f):
    def inner(*args, **kwargs):
        try:
            logger.info(f"Обращение в функцию {f.__name__}")
            return f(*args, **kwargs)
        except:
            logger.exception(f"Ошибка в разработчике {f.__name__}")
            raise
    return inner