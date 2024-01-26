import fitz
from PIL import Image
from io import BytesIO
from utils import save_and_upload_image
from utils import get_bounding_box

def CropPdf(res, s3, target_s3_bucket, target_s3_key, file_stream):
  pdf_document = fitz.open(stream=file_stream, filetype="pdf")
  i = 0
  for item in res["Blocks"]:
    if item["BlockType"] == "SIGNATURE":
      if item['Page']==None:
        page_num=1
      else:
        page_num=item['Page']
      page = pdf_document[page_num-1]
      left, top, width, height = get_bounding_box(item['Geometry']['BoundingBox'], page.rect)
      key = f'{target_s3_key}_signature_of_page_{page_num}_item_{i}.png'
      keys.append(key)
      img_matrix = fitz.Matrix(4, 4)
      pix = page.get_pixmap(matrix=img_matrix, clip=(left, top, left + width, top + height))
      signature_image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
      save_and_upload_image(s3, signature_image, target_s3_bucket, key)
      i += 1
  pdf_document.close()
