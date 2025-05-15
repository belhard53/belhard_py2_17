from celery import Celery
import PIL
from PIL import Image

app = Celery('image_processor', broker='pyamqp://guest@localhost//')

@app.task
def resize_image(image_path, output_path, size):
    with Image.open(image_path) as img:
        img.thumbnail(size, PIL.Image.ANTIALIAS)
        img.save(output_path)

@app.task
def crop_image(image_path, output_path, crop_box):
    with Image.open(image_path) as img:
        cropped_img = img.crop(crop_box)
        cropped_img.save(output_path)

# юзаем
resize_image.delay('path/to/image.jpg', 'path/to/resized_image.jpg', (800, 600))
crop_image.delay('path/to/image.jpg', 'path/to/cropped_image.jpg', (100, 100, 400, 400))