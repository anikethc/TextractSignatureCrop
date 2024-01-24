from PIL import Image
from io import BytesIO

def CropSingleImage(res, target_s3_bucket, target_s3_key, file_stream):
    original_image = Image.open(file_stream)
    for i, item in enumerate(res["Blocks"]):
        if item["BlockType"] == "SIGNATURE":
            left, top, width, height = get_bounding_box(item['Geometry']['BoundingBox'], original_image)
            left, top, right, bottom = map(int, (left, top, left + width, top + height))
            signature_image = original_image.crop((left, top, right, bottom))
            save_and_upload_image(signature_image, target_s3_bucket, target_s3_key)
          
def save_and_upload_image(image, bucket, key):
    cropped_stream = BytesIO()
    image.save(cropped_stream, format='PNG')
    s3.put_object(Body=cropped_stream.getvalue(), Bucket=bucket, Key=key)

def get_bounding_box(geometry, img):
    left = geometry['Left'] * img.width
    top = geometry['Top'] * img.height
    width = geometry['Width'] * img.width
    height = geometry['Height'] * img.height
    return left, top, width, height
