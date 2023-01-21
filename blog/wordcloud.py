import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from wordcloud import WordCloud
from bs4 import BeautifulSoup
from core.utils import plt_to_png_string

def masked_wordcloud(
    corpus, 
    mask_image, 
    export_as_svg=False,
    wordcloud_options={
        'background_color':'rgba(255, 255, 255, 0)',
        'random_state':1,
        'mode':'RGBA',
        'margin':0
        }
    ):
    # Get JPEG PIL Image for mask, convert to numpy array
    pillow = Image.open(mask_image.file.path)
    if pillow.format != 'JPEG':
        pillow = Image.open(mask_image.get_rendition("original|format-jpeg").file.path)
    mask=np.array(pillow)

    # Generate Wordcloud plot
    wordcloud = WordCloud(
        width=mask_image.width, 
        height=mask_image.height, 
        mask=mask, 
        **wordcloud_options
        ).generate(corpus)
    
    if export_as_svg:
        # generate svg string
        svg = wordcloud.to_svg()
        soup = BeautifulSoup(svg,"html.parser")
        svg = soup.find('svg')
        # remove hardcoded width/height and replace with viewbox for dynamic sizing
        svg.attrs['viewbox']=f"0 0 {svg.attrs.pop('width')} {svg.attrs.pop('height')}"
        svg.attrs['preserveAspectRatio']="xMidYMid meet"
        # bug returns font-family:\'font-name'\ - replace single quotes with double
        style = svg.find('style').string
        style.replace_with(style.replace("'", "\""))
        return str(soup)
    else:
        # generate pyplot - no axes or margins
        # figsize must be in inches - get dpi and convert mask pixel dimesions to inches
        px = 1/plt.rcParams['figure.dpi']
        plt.figure(figsize=(mask_image.width*px, mask_image.height*px), dpi=plt.rcParams['figure.dpi'])
        plt.axis("off")
        plt.margins(x=0, y=0)
        plt.imshow(wordcloud, interpolation="bilinear")
        png = plt_to_png_string(plt)
        plt.close()
        return png