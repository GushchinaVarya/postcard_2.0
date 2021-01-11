from typing import Optional


GENDER_MAP = {
    1: 'мужской',
    2: 'женский',
    3: 'не знаю',
}


def gender_hru(gender: int) -> Optional[str]:
    return GENDER_MAP.get(gender)


def validate_age(text: str) -> Optional[int]:
    try:
        age = int(text)
    except (TypeError, ValueError):
        return None

    if age < 0 or age > 100:
        return None
    return age

def validate_gender(text: str) -> Optional[int]:
    try:
        gender = int(text)
    except (TypeError, ValueError):
        return None

    if (gender != 1) & (gender != 2) & (gender != 3):
        return None
    return gender
