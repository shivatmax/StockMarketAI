from bing_image_downloader import downloader
import os
from PIL import Image

def CompanyLogo(Topic):
    querystring = f"{Topic} Company logo"
    downloader.download(querystring, limit=1,  output_dir='images\company', adult_filter_off=True, force_replace=True, timeout=20, verbose=True)
    
    downloaded_images = os.listdir(f'images\company\{Topic} Company logo')
    # print(downloaded_images)
    if len(downloaded_images) == 0:
        print("No images were downloaded. Trying again...")
        downloader.download(querystring, limit=1,  output_dir='images\company', adult_filter_off=True, force_replace=True, timeout=20, verbose=True)
        downloaded_images = os.listdir(f'images\company\{Topic} Company logo')
    
    # Rename the downloaded image to "image.png"
    image_path = os.path.join('images\company', f"{Topic} Company logo")
    # print(image_path)
    new_image_path = None  # Initialize new_image_path variable
    for file in os.listdir(image_path):
        if file.startswith('Image_'):
            os.path.splitext(file)[1]
            new_image_path = os.path.join(image_path, 'Image.png')
            os.rename(os.path.join(image_path, file), new_image_path)
            break
    
    # Convert the image to PNG format
    if new_image_path:
        image = Image.open(new_image_path)
        image.save(new_image_path, 'PNG')
    else:
        return "images\default\Company_logo.png"
    
    return new_image_path
