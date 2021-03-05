from PIL import Image, ImageDraw, ImageFont
from config import FONT_NAME

def prepare_text(text: str, max_width:int):
    arrwords = text.split(' ')
    prepared_text = ''
    current_rowlen = 0
    for word in arrwords:
        if current_rowlen == 0:
            prepared_text = prepared_text + word
            current_rowlen = current_rowlen + len(word) + 1
        elif current_rowlen + len(word) + 1 <= max_width:
            prepared_text = prepared_text+' '+word
            current_rowlen = current_rowlen + len(word) + 1
        else:
            prepared_text = prepared_text + '\n' + word
            current_rowlen = len(word)
    return prepared_text



def write_wish(text: str, pic_number:int, pic_name: str, new_name: str):
    if pic_number == 0:
        #rowlen = 35
        #fontsize = 75
        #loc = (1050, 200)
        rowlen = 35
        fontsize = 40
        loc = (570, 100)
        color = 'black'

    if pic_number == 1:
        rowlen = 35
        fontsize = 40
        loc = (50, 450)
        color = 'white'

    if pic_number == 2:
        rowlen = 40
        fontsize = 35
        loc = (75, 75)
        color = 'black'

    if pic_number == 3:
        rowlen = 40
        fontsize = 35
        loc = (75, 75)
        color = 'black'

    prepared_text = prepare_text(text, rowlen)
    if prepared_text[0] == ' ':
        prepared_text = prepared_text[1:]
    im = Image.open(pic_name)
    font = ImageFont.truetype(FONT_NAME, size=fontsize)
    draw_text = ImageDraw.Draw(im)
    draw_text.text(
        loc,
        text=prepared_text,
        fill=color,
        font=font
        )
    im.save(new_name)

def write_from(text: str, pic_number:int, pic_name: str, new_name: str):
    if pic_number == 0:
        #rowlen = 25
        #fontsize = 50
        #loc = (1800, 1500)
        rowlen = 25
        fontsize = 30
        loc = (900, 800)
        color = 'black'

    if pic_number == 1:
        rowlen = 25
        fontsize = 25
        loc = (50, 1020)
        color = 'black'

    if pic_number == 2:
        rowlen = 20
        fontsize = 22
        loc = (500, 970)
        color = 'black'

    if pic_number == 3:
        rowlen = 25
        fontsize = 22
        loc = (50, 420)
        color = 'black'

    prepared_text = prepare_text(text, rowlen)
    if prepared_text[0] == ' ':
        prepared_text = prepared_text[1:]
    im = Image.open(pic_name)
    font = ImageFont.truetype(FONT_NAME, size=fontsize)
    draw_text = ImageDraw.Draw(im)
    draw_text.text(
        loc,
        text=prepared_text,
        fill=color,
        font=font
        )
    im.save(new_name)

if __name__ == '__main__':
    print(prepare_text('Я классный у бабущки и мноно денег и я хочу много денег и надо делать презентация', 30))