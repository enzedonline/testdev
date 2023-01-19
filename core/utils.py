import base64
import io
import re
from html import unescape

import matplotlib.pyplot as plt
import numpy as np
from bs4 import BeautifulSoup
from PIL import Image
from wordcloud import WordCloud


def get_streamfield_text(streamfield, strip_newlines=True, strip_punctuation=True, lowercase=True):
    html = streamfield.render_as_block()
    soup = BeautifulSoup(unescape(html), "html.parser")
    # strip <style> and <script> tags
    for script in soup(["script", "style"]):
        script.extract()

    inner_text = ' '.join(soup.findAll(text=True))
    inner_text = inner_text.replace('\xa0','') # strip &nbsp;
    inner_text = re.sub(r'\bfa-[^ ]*', ' ', inner_text) # strip font awesome classes
    if strip_newlines:
        inner_text = re.sub(r'([\n]+.?)+', ' ', inner_text) # strip excess newlines
    if strip_punctuation:
        import string
        punctuation = f'{string.punctuation}“”’–'
        inner_text = inner_text.translate(str.maketrans('', '', punctuation))
    if lowercase:
        inner_text = inner_text.lower()
    inner_text = re.sub(r' +', ' ', inner_text) # strip excess whitespace

    return inner_text.strip()

def plt_to_png_string(plt):
    image_bytes = io.BytesIO()
    plt.savefig(image_bytes, format='png', bbox_inches='tight', pad_inches=0)
    image_bytes.seek(0)
    png = base64.b64encode(image_bytes.read()).decode('utf8')
    return f'data:image/png;base64,{png}'

def wordcloud_shape(corpus, mask_image):
    mask=np.array(Image.open(mask_image.file.path))
    wordcloud = WordCloud(
        width=mask_image.width, 
        height=mask_image.height, 
        random_state=1, 
        mask=mask, 
        mode='RGBA', 
        background_color='rgba(255, 255, 255, 0)', 
        margin=0
        ).generate(corpus)
    px = 1/plt.rcParams['figure.dpi']
    plt.figure(figsize=(mask_image.width*px, mask_image.height*px))
    plt.axis("off")
    plt.margins(x=0, y=0)
    plt.imshow(wordcloud, interpolation="bilinear")
    return plt
