import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from wordcloud import WordCloud


def masked_wordcloud(corpus, mask_image):
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