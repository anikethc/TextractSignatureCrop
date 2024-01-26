from PIL import Image
from io import BytesIO

def save_and_upload_image(s3,image, bucket, key):
    cropped_stream = BytesIO()
    image.save(cropped_stream, format='PNG')
    s3.put_object(Body=cropped_stream.getvalue(), Bucket=bucket, Key=key)

def get_bounding_box(geometry, img):
    left = geometry['Left'] * img.width
    top = geometry['Top'] * img.height
    width = geometry['Width'] * img.width
    height = geometry['Height'] * img.height
    return left, top, width, height
