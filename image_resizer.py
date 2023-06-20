# Tristan Caetano
# Vinyl Record Tracker Image Downloader/Comverter
# Script that downloads album art from spotify after API call

# *MOST OF THIS CODE IS NOT MINE*

# Imports
import PIL.Image
import io
import base64
import urllib.request
import os

# Doanloading image to device
def download_image(album_name, url):

    # Creating local image path name
    image_path = album_name + ".png"

    # Downloading the image to the path
    urllib.request.urlretrieve(url, image_path)

    # Returning the name of the image path
    return image_path

# Converting the image to PNG and resizing it to fit in GUI
def resize_image(resize, url, album_name, delete):

    # If statement for whether or not the image given is local or to be downloaded
    if delete:
        image_path = download_image(album_name, url)
    else:
        image_path = url

    # Converting image data into a format that can be properly displayed
    if isinstance(image_path, str):
        img = PIL.Image.open(image_path)
    else:
        try:
            img = PIL.Image.open(io.BytesIO(base64.b64decode(image_path)))
        except Exception as e:
            data_bytes_io = io.BytesIO(image_path)
            img = PIL.Image.open(data_bytes_io)

    # Resizing image
    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height/cur_height, new_width/cur_width)
        img = img.resize((int(cur_width*scale), int(cur_height*scale)), PIL.Image.LANCZOS)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img

    # Deleting the downloaded image
    if delete:
        os.remove(image_path)

    # Returning image data to be displayed
    return bio.getvalue()