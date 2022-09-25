import os, random
from PIL import Image
from flask import current_app

def add_gallery_image(pic_upload, user_id, pass_date, image_tag):

    filename = pic_upload.filename
    ext_type = filename.split('.')[-1]
    storage_filename = f'img_{random.randint(1000, 9000)}_{image_tag}_{user_id}_{pass_date}' \
                        f'.{ext_type}'
    filepath = os.path.join(current_app.root_path, 'static/img/gallery',
                            storage_filename)
    output_size = (400,400)

    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)
    pic.save(filepath)

    return storage_filename
  
