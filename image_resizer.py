import PIL.Image
import io
import base64

import urllib.request
from PIL import Image
import os

def download_image(album_name, url):
    image_path = album_name + ".png"
    urllib.request.urlretrieve(url, image_path)
    return image_path

def resize_image(resize, url, album_name, delete):

    if delete:
        image_path = download_image(album_name, url)
    else:
        image_path = url

    if isinstance(image_path, str):
        img = PIL.Image.open(image_path)
    else:
        try:
            img = PIL.Image.open(io.BytesIO(base64.b64decode(image_path)))
        except Exception as e:
            data_bytes_io = io.BytesIO(image_path)
            img = PIL.Image.open(data_bytes_io)

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height/cur_height, new_width/cur_width)
        img = img.resize((int(cur_width*scale), int(cur_height*scale)), PIL.Image.Resampling.LANCZOS)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img

    if delete:
        os.remove(image_path)

    return bio.getvalue()