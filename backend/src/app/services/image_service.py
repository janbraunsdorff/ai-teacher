import base64
import io
from typing import Optional, Tuple
from PIL import Image

from app.database.document import get_images_from_document, get_latest_request, update_class
from app.model.document import ImageClassificationResult, TaskType
from app.model.image_model import NextImage, ClassificationTargets


def get_image_data(pid, iid):
    files = get_images_from_document(pid, iid)
    for file in files:
        return base64.b64decode(file)
        # img = Image.open(io.BytesIO(img))
        # return

def get_image_size(data: bytes) -> Tuple[int, int]:
    img = base64.b64decode(data)
    shape = Image.open(io.BytesIO(img)).size
    return shape[0], shape[1]



def get_next_image(pid: str, type: TaskType) -> Optional[NextImage]:
    doc = get_latest_request(pid, type)
    if not doc:
        return None

    task = list(filter(lambda x: x.type == type.value, doc.tasks))[0]
    classes = [ClassificationTargets(name=x.name, desc=x.describtion) for x in task.targets]
    width, height = get_image_size(doc.files[0])
    res = NextImage(id=doc.id, width=width, height=height, classes=classes)
    return res


def classifiy(pid: str, did: str, uid: str, clazz: str, task_type: TaskType):
    res = ImageClassificationResult(worker_id=uid, clazz=clazz)
    update_class(pid, did, res, task_type)