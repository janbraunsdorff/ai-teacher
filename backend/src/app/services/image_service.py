import base64
import io

from PIL import Image

from app.database.document import get_images_from_document


def get_image_data(pid, iid):
    files = get_images_from_document(pid, iid)
    for file in files:
        return base64.b64decode(file)
        # img = Image.open(io.BytesIO(img))
        # return
