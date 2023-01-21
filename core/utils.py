import base64
import io
import re
from html import unescape

from bs4 import BeautifulSoup


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
    plt.tight_layout()
    plt.savefig(image_bytes, format='png', bbox_inches='tight', pad_inches=0)
    image_bytes.seek(0)
    png = base64.b64encode(image_bytes.read()).decode('utf8')
    return f'data:image/png;base64,{png}'

