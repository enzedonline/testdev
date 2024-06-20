
import base64
import fnmatch
import importlib
import io
import math
import os
import re
from collections import OrderedDict
from html import unescape
from html.parser import HTMLParser

from bs4 import BeautifulSoup
from crequest.middleware import CrequestMiddleware
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from lxml import etree
from PIL.ExifTags import GPSTAGS, TAGS
from wagtail.blocks import ListBlock
from wagtail.blocks.stream_block import StreamValue
from wagtail.models import Page


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

def check_variable_existence(data, variable_name):
    if isinstance(data, dict):
        if variable_name in data:
            return data[variable_name]
        for value in data.values():
            result = check_variable_existence(value, variable_name)
            if result is not None:
                return result
    elif isinstance(data, list):
        for item in data:
            result = check_variable_existence(item, variable_name)
            if result is not None:
                return result
    return None

def block_exists(stream_data, search_value):
    if isinstance(stream_data, dict):
        if 'type' in stream_data and stream_data['type'] == search_value:
            return True
        for value in stream_data.values():
            if block_exists(value, search_value):
                return True
    elif isinstance(stream_data, (list, StreamValue.RawDataView)):
        for item in stream_data:
            if block_exists(item, search_value):
                return True
    return False

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.is_html = False

    def handle_starttag(self, tag, attrs):
        self.is_html = True

def is_html(input_string):
    parser = MyHTMLParser()
    parser.feed(input_string)
    return parser.is_html




def decode_exif(exif_data):
    decoded_data = {}
    for tag, value in exif_data.items():
        tag_name = TAGS.get(tag, tag)
        if isinstance(value, bytes):
            value = value.decode(errors='replace')
        decoded_data[tag_name] = value
    return decoded_data


def list_block_instances(streamfield):
    def list_bound_blocks(data):
        list = []
        bound_blocks = None

        if isinstance(data, StreamValue):
            bound_blocks = data._bound_blocks
        else:
            value = getattr(data, "value", None)
            if value:
                bound_blocks = getattr(value, "bound_blocks", getattr(value, "_bound_blocks", None))

        if not bound_blocks:
            return None

        if isinstance(bound_blocks, OrderedDict):
            for key, value in bound_blocks.items():
                child_blocks = list_bound_blocks(value)
                item = {
                    "type": key,
                    "class": f"{value.block.__class__.__module__}.{value.block.__class__.__name__}",
                }
                if child_blocks:
                    item["child_blocks"] = child_blocks
                list += [item]
        else:
            for bound_block in bound_blocks:
                if bound_block:
                    item = {
                        "type": bound_block.block.name,
                        "class": f"{bound_block.block.__class__.__module__}.{bound_block.block.__class__.__name__}",
                    }
                    child_blocks = list_bound_blocks(bound_block)
                    if child_blocks:
                        item["child_blocks"] = child_blocks
                    list += [item]
        return list
    
    if streamfield.is_lazy: r = streamfield.render_as_block() # force lazy object to load
    return list_bound_blocks(streamfield)

def block_instances_by_class(streamfield, block_class):
    def find_blocks(data, block_class):
        list = []
        bound_blocks = None

        if isinstance(data, StreamValue):
            bound_blocks = data._bound_blocks
        else:
            value = getattr(data, "value", None)
            if value:
                bound_blocks = getattr(value, "bound_blocks", getattr(value, "_bound_blocks", None))

        if not bound_blocks:
            return []

        if isinstance(bound_blocks, OrderedDict):
            bound_blocks = bound_blocks.values()
    
        for bound_block in bound_blocks:
            if type(bound_block.block) is block_class: list += [bound_block]
            list += find_blocks(bound_block, block_class)
        return list

    if type(block_class)==str:
        try:
            module_name, class_name = block_class.rsplit('.', 1)
            module = importlib.import_module(module_name)
            block_class = getattr(module, class_name)().__class__
        except:
            return ['Unable to parse class path. Try passing the class object instead.']    
    if streamfield.is_lazy: r = streamfield.render_as_block() # force lazy object to load

    return find_blocks(streamfield, block_class)

def list_streamfield_blocks(streamfield):
    def list_child_blocks(child_blocks):
        list = []
        for key, value in child_blocks.items():
            item = {
                "type": key,
                "class": f"{value.__class__.__module__}.{value.__class__.__name__}",
            }
            if getattr(value, 'child_blocks', False):
                item["child_blocks"] = list_child_blocks(value.child_blocks)
            elif isinstance(value, ListBlock):
                item["child_blocks"] = list_child_blocks({value.child_block.name: value.child_block})
            list += [item]
        return list
    
    return list_child_blocks(streamfield.stream_block.child_blocks)

def sf(number, significant_figures):
    if number == 0:
        return 0
    else:
        return round(number, significant_figures - int(math.floor(math.log10(abs(number)))) - 1)

def get_custom_icons(root_folder = 'core/templates', icons_folder = 'icons', file_extension = '*.svg'):
    """ Return a list of icons found in a certain path """
    icons = []
    icons_path = os.path.join(root_folder, icons_folder)

    # Walk through the directory and find matching files in the icons folder
    for foldername, subfolders, filenames in os.walk(icons_path):
        for filename in fnmatch.filter(filenames, file_extension):
            file_path = os.path.join(foldername, filename)
            relative_path = os.path.relpath(file_path, root_folder)
            icons.append(relative_path)

    return icons

def strip_svg_markup(svg_markup):
    """Strip <script> tags, height and width attributes from svg markup"""
    root = etree.fromstring(svg_markup.encode('utf-8'))
    for element in root.findall(".//{http://www.w3.org/2000/svg}script"):
        element.getparent().remove(element)
    for element in root.iter():
        element.attrib.pop('height', None)
        element.attrib.pop('width', None)
    return etree.tostring(root, encoding='unicode', method='xml', xml_declaration=False)
    
class FakeRequest:
    """
    FakeRequest takes the place of the django HTTPRequest object in various testing scenarios where
    a real one doesn't exist, but the code under test expects one to be there.

    Wagtail 2.9 now determines the current Site by looking at the hostname and port in the request object,
    which means it calls get_host() on our faked out requests. Thus, we need to emulate it.
    """

    def __init__(self, site=None, user=None, **kwargs):
        self.user = user
        # Include empty GET and POST attrs, so code which expects request.GET or request.POST to exist won't crash.
        self.GET = self.POST = {}
        # Callers can override GET and POST, or override/add any other attribute using kwargs.
        self.__dict__.update(kwargs)
        self._wagtail_site = site

    def get_host(self):
        if not self._wagtail_site:
            return 'fakehost'
        return self._wagtail_site.hostname

    def get_port(self):
        # It should be safe to pretend all test traffic is on port 443.
        # HTTPRequest.get_port() explicitly returns a string, so we do, too.
        return '443'


def set_fake_current_request(site=None, user=None, request=None, **kwargs):
    """
    Sets the current request to either a specified request object or a FakeRequest object built from the given Site
    and/or User. Any additional keyword args are added as attributes on the FakeRequest.
    """
    # If the caller didn't provide a request object, create a FakeRequest.
    if request is None:
        request = FakeRequest(site, user, **kwargs)
    # Set the created (or provided) request as the "current request".
    CrequestMiddleware.set_request(request)
    return request


class FakeCurrentRequest():
    """
    Implements set_fake_current_request() as a context manager. Use like this:
    with FakeCurrentRequest(some_site, some_user):
        // .. do stuff
    OR
    with FakeCurrentRequest(request=some_request):
        // .. do stuff

    When the context manager exits, the current request will be automatically reverted to its previous state.
    """
    NO_CURRENT_REQUEST = 'no_current_request'

    def __init__(self, site=None, user=None, request=None, **kwargs):
        self.site = site
        self.user = user
        self.request = request
        self.kwargs = kwargs

    def __enter__(self):
        # Store a copy of the original current request, so we can restore it when the context manager exits.
        self.old_request = CrequestMiddleware.get_request(default=self.NO_CURRENT_REQUEST)
        return set_fake_current_request(self.site, self.user, self.request, **self.kwargs)

    def __exit__(self, *args):
        if self.old_request == self.NO_CURRENT_REQUEST:
            # If there wasn't a current request when we entered the contact manager, remove the current request.
            CrequestMiddleware.del_request()
        else:
            # Otherwise, set the current request back to whatever it was when we entered.
            CrequestMiddleware.set_request(self.old_request)