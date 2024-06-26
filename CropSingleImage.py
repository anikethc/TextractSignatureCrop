from PIL import Image
from io import BytesIO
from utils import save_and_upload_image
from utils import get_bounding_box

def CropSingleImage(res, s3, target_s3_bucket, target_s3_key, file_stream):
    original_image = Image.open(file_stream)
    for i, item in enumerate(res["Blocks"]):
        if item["BlockType"] == "SIGNATURE":
            left, top, width, height = get_bounding_box(item['Geometry']['BoundingBox'], original_image)
            left, top, right, bottom = map(int, (left, top, left + width, top + height))
            signature_image = original_image.crop((left, top, right, bottom))
            key = f'{target_s3_key}_item_{i}.png'
            save_and_upload_image(s3, signature_image, target_s3_bucket, key)
