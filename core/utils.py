import base64
import importlib
import io
import re
from html import unescape

from bs4 import BeautifulSoup
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from wagtail.blocks.stream_block import StreamValue
from wagtail.models import Page

from urllib.parse import urlparse, parse_qs

def validate_email(email):
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    emails = email.split(',')

    for email in emails:
        if not re.match(email_pattern, email.strip()):
            return False

    return True

def validate_email_query_string(query_string):
    query_params = parse_qs(unescape(query_string))
    valid_params = {'to', 'cc', 'bcc', 'subject', 'body'}

    for key, values in query_params.items():
        if not (key in valid_params and re.match(r'^\w+=.+$', f"{key}={values[0]}")):
            return False

    return True

def validate_email_with_query_string(string):
    url_parts = urlparse(string)

    if not url_parts.path:
        return False

    email = url_parts.path
    query_string = url_parts.query

    if validate_email(email):
        if query_string:
            return validate_email_query_string(query_string)
        else:
            return True

    return False

def page_url(slug, target=None):
    pg = Page.objects.filter(slug=slug).first()
    return f'{pg.url}{"#" + target if target else ""}' if pg else ''

def get_streamfield_text(
    streamfield, 
    strip_newlines=True, 
    strip_punctuation=True, 
    lowercase=False,
    strip_tags=['style', 'script', 'code']
    ):
    
    html = streamfield.render_as_block()
    soup = BeautifulSoup(unescape(html), "html.parser")

    # strip unwanted tags tags (e.g. ['code', 'script', 'style'])
    # <style> & <script> by default
    if strip_tags:
        for script in soup(strip_tags):
            script.extract()

    inner_text = ' '.join(soup.findAll(text=True))

    # replace &nbsp; with space
    inner_text = inner_text.replace('\xa0',' ')

    # replace & with and
    inner_text = inner_text.replace(' & ',' and ')

    # strip font awesome text
    inner_text = re.sub(r'\bfa-[^ ]*', '', inner_text)

    if strip_newlines:
        inner_text = re.sub(r'([\n]+.?)+', ' ', inner_text)

    if strip_punctuation:
        # replace xx/yy with xx yy, leave fractions (1/2)
        inner_text = re.sub(r'(?<=\D)/(?=\D)', ' ', inner_text)
        # strip full stops, leave decimal points and point separators
        inner_text = re.sub(r'\.(?=\s)', '', inner_text)
        punctuation = '!"#$%&\'()*+,-:;<=>?@[\\]^_`{|}~“”‘’–«»‹›¿¡'
        inner_text = inner_text.translate(str.maketrans('', '', punctuation))

    if lowercase:
        inner_text = inner_text.lower()

    # strip excess whitespace
    inner_text = re.sub(r' +', ' ', inner_text).strip()

    return inner_text

def count_words(text):
    try:
        word_break_chars='[\n|\r|\t|\f| ]'
        ignore_words = ['', '-', '−', '–', '/']
        return len([x for x in re.split(word_break_chars, text) if not x in ignore_words])
    except:
        return -1

def plt_to_png_string(plt):
    image_bytes = io.BytesIO()
    plt.tight_layout()
    plt.savefig(image_bytes, format='png', bbox_inches='tight', pad_inches=0)
    image_bytes.seek(0)
    png = base64.b64encode(image_bytes.read()).decode('utf8')
    return f'data:image/png;base64,{png}'

def text_from_html(value):
    """
    Returns the unescaped text content of an HTML string.
    """

    return BeautifulSoup(force_str(value), "html5lib").getText()

def has_role(user, groups):
    try:
        group_list = groups if isinstance(groups, list) else [groups]
        return user.groups.get_queryset().filter(name__in=group_list).exists()
    except Exception as e:
        print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")       
        return False

def count_words(text):
    try:
        word_break_chars='[\n|\r|\t|\f| ]'
        ignore_words = ['', '-', '−', '–', '/']
        return len([x for x in re.split(word_break_chars, text) if not x in ignore_words])
    except:
        return -1

def find_all_streamfields_with_css_class(css_class):
    
    found_pages = []
    pages = Page.objects.all().specific()

    for page in pages:

        for item in page.__dict__.items():
            if item[1].__class__ == StreamValue:
                if stream_has_css_class(item[1], css_class): found_pages.append((page, item[0]))
                print(page.title)
    
    return [*set(found_pages)]

def stream_has_css_class(streamvalue, css_class):
    render = BeautifulSoup(streamvalue.render_as_block(), 'html.parser')
    return (render.select_one(f'.{css_class}') != None) if render else False

def import_text_field_button(field):
    return '''
        <label for="''' + field + '''File"> 
            <span class="w-panel__heading w-panel__heading--label">''' + _("Read data from file") + '''</span> 
        </label> 
        <input type="file" id="''' + field + '''File" style="border-style: none; padding: 0;" />
        <script> 
            const ''' + field + '''File = document.getElementById("''' + field + '''File"); 
            ''' + field + '''File.addEventListener("change", (e) => {
                e.preventDefault(); 
                const input = ''' + field + '''File.files[0]; 
                const reader = new FileReader(); 
                reader.onload = function (e) {
                    const ''' + field + '''Field = document.getElementById("id_''' + field + '''"); 
                    ''' + field + '''Field.value = e.target.result; 
                }; 
                reader.readAsText(input); 
            }); 
        </script>'''    

