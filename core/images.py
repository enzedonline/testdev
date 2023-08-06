import io
import math

from PIL import Image
from wagtail.images.models import Filter


def reduce_image_file_size(image_path, max_file_size_kb = 1024, min_quality = 75):
    # Load the image
    image = Image.open(image_path)
    image_format = image.format or 'PNG'

    # Calculate the file sizes
    max_file_size = max_file_size_kb * 1024
    with io.BytesIO() as temp_buffer:
        image.save(temp_buffer, format=image_format)
        current_file_size = temp_buffer.tell()

    # If the current file size is already below the maximum, return the image as is
    if current_file_size <= max_file_size:
        return image

    # Get the starting quality from the original image
    quality = getattr(image, 'info', {}).get('quality', 100)

    # create new buffer to save resized image to
    resized_image = image
    resized_buffer = io.BytesIO()

    # Define the boundaries for quality and dimensions
    while current_file_size > max_file_size and quality > min_quality:

        reduce_ratio = max_file_size / current_file_size

        # Reduce the quality
        quality = int(reduce_ratio * quality)
        if quality < min_quality: quality = min_quality

        try:
            # Resize the image using ANTIALIAS and save to resized_buffer with the current quality
            resized_image = image.resize(image.size, Image.ANTIALIAS)
            resized_image.save(resized_buffer, format=image_format, quality=quality)

            # Calculate the file size of the resized image
            resized_buffer.seek(0)
            current_file_size = len(resized_buffer.getvalue())
        except:
            # file type does not support quality attribute
            break

    # If further reduction is needed, reduce image dimensions
    while current_file_size > max_file_size:
        # Reduce the dimensions by square root of the reduce ratio
        # (reduce area by ratio, not dimensions)
        reduce_ratio = max_file_size / current_file_size
        width = int(math.sqrt(reduce_ratio) * resized_image.width)
        height = int(math.sqrt(reduce_ratio) * resized_image.height)

        # Resize the image using ANTIALIAS and save to a new BytesIO buffer
        resized_buffer = io.BytesIO()
        resized_image = resized_image.resize((width, height), Image.ANTIALIAS)
        resized_image.save(resized_buffer, format=image_format)

        # Calculate the file size of the resized image
        resized_buffer.seek(0)
        current_file_size = len(resized_buffer.getvalue())

    # Convert the final resized and compressed image from the BytesIO buffer to PIL Image
    resized_buffer.seek(0)
    return Image.open(resized_buffer)

def check_image_size(image, max_file_size_kb = 1024, min_quality = 75):

    if image.file_size <= max_file_size_kb * 1024:
        return True
    else:
        # resize image, save and update metadata
        resized_image = reduce_image_file_size(image.file.path, max_file_size_kb, min_quality)
        resized_image.save(image.file.path)
        image._set_image_file_metadata()
        # delete 'original' rendition if exists
        flt = Filter(spec='original')
        try:
            rnd=image.find_existing_rendition(flt)
            rnd.delete()
        except:
            pass
        return False


