from io import BytesIO
import boto3

s3 = boto3.client('s3')
def save_and_upload_image(image, bucket, key):
    cropped_stream = BytesIO()
    image.save(cropped_stream, format='PNG')
    s3.put_object(Body=cropped_stream.getvalue(), Bucket=bucket, Key=key)
