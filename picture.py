from PIL import Image, ImageDraw, ImageFont

pic_name = 'pic_lena_big.JPG'

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



def write_wish(text: str, pic_name: str, new_name: str):
    prepared_text = prepare_text(text, 28)
    if prepared_text[0] == ' ':
        prepared_text = prepared_text[1:]
    im = Image.open(pic_name)
    font = ImageFont.truetype('DejaVuSerif.ttf', size=80)
    draw_text = ImageDraw.Draw(im)
    draw_text.text(
        (1050, 200),
        text=prepared_text,
        fill='black',
        font=font
        )
    im.save(new_name)

def write_from(text: str, pic_name: str, new_name: str):
    prepared_text = prepare_text(text, 20)
    if prepared_text[0] == ' ':
        prepared_text = prepared_text[1:]
    im = Image.open(pic_name)
    font = ImageFont.truetype('DejaVuSerif.ttf', size=50)
    draw_text = ImageDraw.Draw(im)
    draw_text.text(
        (1800, 1500),
        text=prepared_text,
        fill='black',
        font=font
        )
    im.save(new_name)

if __name__ == '__main__':
    print(prepare_text('Я классный у бабущки и мноно денег и я хочу много денег и надо делать презентация', 30))