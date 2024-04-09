from urllib.parse import urlparse

from bs4 import BeautifulSoup
from django import template
from wagtail.embeds.embeds import get_embed
from wagtail.embeds.exceptions import EmbedException

register = template.Library()

@register.simple_tag()
def get_embed_code(url):
    try:
        embed = get_embed(url)
        soup = BeautifulSoup(embed.html, 'html.parser')
        iframe = soup.find('iframe')
        src = urlparse(iframe['src']).path

        return {
            'video_id': src.split('/')[-1:][0],
            'thumbnail_url': embed.thumbnail_url,
            'title': embed.title,
            'author_name': embed.author_name,
            'last_updated': embed.last_updated,
        }
    
    except EmbedException:
        pass