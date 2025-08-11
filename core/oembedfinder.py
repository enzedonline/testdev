from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from django.core.exceptions import ImproperlyConfigured

from bs4 import BeautifulSoup
from wagtail.embeds.finders.oembed import OEmbedFinder
from wagtail.embeds.oembed_providers import youtube
import requests

def _extract_youtube_id(url: str):
    u = urlparse(url)
    host = u.netloc.lower()
    if 'youtu.be' in host:
        return u.path.lstrip('/').split('/')[0] or None
    if 'youtube.com' in host:
        if u.path.startswith('/watch'):
            return parse_qs(u.query).get('v', [None])[0]
        parts = [p for p in u.path.split('/') if p]
        if len(parts) >= 2 and parts[0] in ('shorts', 'embed', 'v'):
            return parts[1]
    return None

def _best_youtube_thumbnail(video_id: str) -> str | None:
    for name in ("maxresdefault.jpg", "sddefault.jpg", "hqdefault.jpg", "mqdefault.jpg", "default.jpg"):
        url = f"https://img.youtube.com/vi/{video_id}/{name}"
        try:
            r = requests.get(url, stream=True, timeout=3)
            if r.ok and r.headers.get("Content-Type") == "image/jpeg":
                size = int(r.headers.get("Content-Length", 0))
                if size > 5000:  # Placeholder is usually small
                    return url
        except requests.RequestException:
            pass
    return None


# class YouTubeShortsFinder(OEmbedFinder):
#     def __init__(self, providers=None, options=None):
#         youtube['urls'].append(r"^https?://(?:[-\w]+\.)?youtube\.com/shorts/.+$")
#         providers = [youtube] if providers is None else providers.append[youtube]
#         super().__init__(providers=providers, options=options)

class YouTubeResponsiveFinder(OEmbedFinder):
    """
    A specialized OEmbedFinder for YouTube that ensures responsive embeds and improved thumbnail selection.
    This finder:
    - Restricts itself to only operate with the YouTube provider.
    - Attempts to retrieve oEmbed data using the parent class, falling back to a direct YouTube oEmbed API call if necessary.
    - Modifies the returned HTML to make the embedded iframe responsive by removing fixed width/height and applying CSS styles.
    - Attempts to select the best available YouTube thumbnail for the video.
    - Returns a dictionary containing embed metadata and the modified HTML.
    Args:
        providers (list, optional): List of oEmbed providers. Must be [youtube] or None.
        options (dict, optional): Additional options for the finder.
    Raises:
        ImproperlyConfigured: If providers is not [youtube].
    Methods:
        find_embed(url, max_width=None):
            Retrieves and modifies the oEmbed data for a given YouTube URL, ensuring responsive HTML and optimal thumbnail selection.
    """

    def __init__(self, providers=None, options=None):
        if providers is None:
            providers = [youtube]

        if providers != [youtube]:
            raise ImproperlyConfigured(
                'YouTubeResponsiveFinder only operates on the youtube provider'
            )
        super().__init__(providers=providers, options=options)

    def find_embed(self, url, max_width=None):
        try:
            embed = super().find_embed(url, max_width)
        except:
            response = requests.get('https://www.youtube.com/oembed/?url=' + url)   
            result = response.json()
            embed = {
                'title': result['title'], 
                'author_name': result['author_name'], 
                'provider_name': result['provider_name'], 
                'type': result['type'], 
                'thumbnail_url': result['thumbnail_url'], 
                'width': result['width'],  
                'height': result['height'], 
                'html': result['html'], 
            }

        try:
            soup = BeautifulSoup(embed['html'], 'html.parser')
            iframe = soup.find('iframe')
            if iframe:
                del iframe.attrs['height']
                del iframe.attrs['width']
                aspect_ratio = embed['width'] / embed['height']
                iframe.attrs['style'] = f'aspect-ratio: {aspect_ratio};'
                iframe.attrs['class'] = ['youtube-responsive-item']
            embed['html'] = str(soup)
        except:
            pass

        # Prefer a larger thumbnail, without assuming aspect ratio
        video_id = _extract_youtube_id(url)
        if video_id:
            best = _best_youtube_thumbnail(video_id)
            if best:
                embed['thumbnail_url'] = best
                # Do not set thumbnail_width/height; let the client decide sizing

        return embed

