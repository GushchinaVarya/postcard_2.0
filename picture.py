from PIL import Image, ImageDraw, ImageFont
from config import FONT_NAME
from pic_config import PIC_INFO, PIC_FOLDER, FONTS_FOLDER

from logger_debug import *
logger = getLogger(__name__)

@debug_request
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


@debug_request
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

@debug_request
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


@debug_request
def prepare_text_2(text: str, pic_number:int, type:str):
    assert (type in ['wish', 'from', 'author', 'fund1', 'fund2', 'fund3', 'discl']), 'unknown type'
    textlen= len(text)
    i = 0
    while PIC_INFO[str(pic_number)]['lenths_'+type][i] < textlen:
        i = i + 1
    fontsize = PIC_INFO[str(pic_number)]['fontsizes_'+type][i]
    max_width = PIC_INFO[str(pic_number)]['rowlens_'+type][i]
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
    return prepared_text, fontsize, i


@debug_request
def write_text_2(text: str, pic_number:int, user_id: int, type:str):
    assert (type in ['wish', 'from', 'author', 'fund1', 'fund2', 'fund3', 'discl']), 'unknown type'
    prepared_text = prepare_text_2(text, pic_number, type)[0]
    fontsize = prepare_text_2(text, pic_number, type)[1]
    loc = PIC_INFO[str(pic_number)]['loc_'+type]
    color = PIC_INFO[str(pic_number)]['color_'+type]
    if prepared_text[0] == ' ':
        prepared_text = prepared_text[1:]
    if type == 'wish':
        pic_name = PIC_FOLDER+PIC_INFO[str(pic_number)]['pic_name']
    elif type == 'from':
        pic_name = PIC_FOLDER+'wish_'+str(user_id)+'_'+PIC_INFO[str(pic_number)]['pic_name']
    elif type == 'author':
        pic_name = PIC_FOLDER+PIC_INFO[str(pic_number)]['pic_name']
    elif type == 'discl':
        pic_name = PIC_FOLDER+'author_'+str(user_id)+'_'+PIC_INFO[str(pic_number)]['pic_name']
    elif type == 'fund1':
        pic_name = PIC_FOLDER+'discl_'+str(user_id)+'_'+PIC_INFO[str(pic_number)]['pic_name']
    elif type == 'fund2':
        pic_name = PIC_FOLDER+'fund1_'+str(user_id)+'_'+PIC_INFO[str(pic_number)]['pic_name']
    elif type == 'fund3':
        pic_name = PIC_FOLDER+'fund2_'+str(user_id)+'_'+PIC_INFO[str(pic_number)]['pic_name']

    im = Image.open(pic_name)
    font = ImageFont.truetype(FONTS_FOLDER+PIC_INFO[str(pic_number)]['font_'+type], size=fontsize)
    draw_text = ImageDraw.Draw(im)
    draw_text.text(
        loc,
        text=prepared_text,
        fill=color,
        font=font
        )
    im.save(PIC_FOLDER+type+'_'+str(user_id)+'_'+PIC_INFO[str(pic_number)]['pic_name'])

if __name__ == '__main__':
    print(prepare_text('Я классный у бабущки и мноно денег и я хочу много денег и надо делать презентация', 30))