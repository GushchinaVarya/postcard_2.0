from PIL import Image, ImageDraw, ImageFont
from config import FONT_NAME
from pic_config import PIC_INFO, PIC_FOLDER, FONTS_FOLDER

from logger_debug import *
logger = getLogger(__name__)

@debug_request
def prepare_text_2(text: str, pic_number:int, type:str):
    assert (type in ['wish', 'from', 'author', 'fund1', 'fund2', 'fund3', 'discl', 'tag']), 'unknown type'
    textlen= len(text)
    i = 0
    while PIC_INFO[str(pic_number)]['lenths_'+type][i] < textlen:
        i = i + 1
    fontsize = PIC_INFO[str(pic_number)]['fontsizes_'+type][i]
    max_width = PIC_INFO[str(pic_number)]['rowlens_'+type][i]
    arrwords = text.split(' ')
    prepared_text = ''
    current_rowlen = 0
    max_rowlen = 0
    nrows = 1
    for word in arrwords:
        if current_rowlen == 0:
            prepared_text = prepared_text + word
            current_rowlen = current_rowlen + len(word) + 1
            if max_rowlen < current_rowlen:
                max_rowlen = current_rowlen
        elif current_rowlen + len(word) + 1 <= max_width:
            prepared_text = prepared_text+' '+word
            current_rowlen = current_rowlen + len(word) + 1
            if max_rowlen < current_rowlen:
                max_rowlen = current_rowlen
        else:
            prepared_text = prepared_text + '\n' + word
            nrows = nrows + 1
            current_rowlen = len(word)
            if max_rowlen < current_rowlen:
                max_rowlen = current_rowlen
    return prepared_text, fontsize, i, max_rowlen, nrows

@debug_request
def calculate_loc_from(loc, max_rowlen, fontsize, nrows):
    loc_0_new = int(loc[0] - max_rowlen*fontsize*0.5)
    loc_1_new = int(loc[1] - nrows*fontsize*0.5)
    return (loc_0_new, loc_1_new)

@debug_request
def write_text_2(text: str, pic_number:int, user_id: int, type:str):
    assert (type in ['wish', 'from', 'author', 'fund1', 'fund2', 'fund3', 'discl', 'tag']), 'unknown type'
    prepared_text = prepare_text_2(text, pic_number, type)[0]
    fontsize = prepare_text_2(text, pic_number, type)[1]
    max_rowlen = prepare_text_2(text, pic_number, type)[3]
    nrows = prepare_text_2(text, pic_number, type)[4]
    loc = PIC_INFO[str(pic_number)]['loc_'+type]
    if type == 'from':
        loc = calculate_loc_from(loc, max_rowlen, fontsize, nrows)
    color = PIC_INFO[str(pic_number)]['color_'+type]
    if prepared_text[0] == ' ':
        prepared_text = prepared_text[1:]
    if type == 'wish':
        pic_name = PIC_FOLDER+PIC_INFO[str(pic_number)]['pic_name']
    elif type == 'from':
        pic_name = PIC_FOLDER+'wish_'+str(user_id)+'_'+PIC_INFO[str(pic_number)]['pic_name']
    elif type == 'author':
        pic_name = PIC_FOLDER+PIC_INFO[str(pic_number)]['pic_name']
    elif type == 'tag':
        pic_name = PIC_FOLDER+'author_'+str(user_id)+'_'+PIC_INFO[str(pic_number)]['pic_name']
    elif type == 'discl':
        pic_name = PIC_FOLDER+'tag_'+str(user_id)+'_'+PIC_INFO[str(pic_number)]['pic_name']
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