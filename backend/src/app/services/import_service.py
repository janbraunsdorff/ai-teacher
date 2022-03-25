import base64
import io
import os
from os import listdir
from os.path import isfile, join
from typing import Any, List

import filetype
from fastapi import HTTPException, status
from pdf2image import convert_from_path
from PIL import Image

from app.database.document import insert_document
from app.database.project import get_by_id
from app.model.document import (
    Document,
    DocumentType,
    ImageBoundingBoxTask,
    ImageClassificationTask,
    ImageExtractionTask,
    TaskType,
)
from app.model.project_model import Project

supported_image = ["image/png", "image/jpeg"]
supported_archieves = ["application/pdf"]


def import_and_convert_to_default(path: str, pid: str):
    path = os.path.abspath(path)
    files = read_dir(path)
    project = get_by_id(pid)
    unknown_filetype = []
    imported = 0
    for file_name in files:
        file = f"{path}/{file_name}"
        b64Files = []
        kind = filetype.guess(file)
        if kind is None:
            unknown_filetype.append(file)
            continue

        if kind.mime in supported_image:
            b64Files.extend(convert_img_to_png(file))

        elif kind.mime in supported_archieves:
            b64Files.extend(convert_pdf_to_png(file))

        save_document(b64Files, project, get_document_type(kind.mime), file)
        imported += 1

    return imported, unknown_filetype


def get_document_type(mime: Any) -> DocumentType:
    if mime in supported_archieves or mime in supported_image:
        return DocumentType.IMAGE
    raise ValueError(f"no dokument type for: {type}")


def read_dir(path) -> List[str]:
    try:
        return [f for f in listdir(path) if isfile(join(path, f))]
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no data under {path}",
        )


def convert_img_to_png(path: str) -> List[str]:
    img = Image.open(path)

    return [convert_pil_to_base64(img)]


def convert_pdf_to_png(path: str) -> List[str]:
    files = convert_from_path(path)
    return [convert_pil_to_base64(x) for x in files]


def convert_pil_to_base64(img=Image) -> str:
    img = img.convert("RGB")
    with io.BytesIO() as out:
        img.save(out, format="PNG")
        b64Image = base64.b64encode(out.getvalue()).decode("utf-8")
    return b64Image


def save_document(files: List[str], project: Project, type: DocumentType, original_name:str):
    tasks = []
    for task in project.tasks:
        task = TaskType(task)
        if task == TaskType.IMAGE_BOUNDINGBOX:
            tasks.append(
                ImageBoundingBoxTask(
                    type=task,
                    results=[],
                    targets=project.img_bounding_box_classes,
                    entities=[],
                )
            )
        if task == TaskType.IMAGE_CLASSIFICATION:
            tasks.append(
                ImageClassificationTask(
                    type=task,
                    results=[],
                    targets=project.img_classes,
                    classes=[],
                )
            )
        if task == TaskType.IMAGE_EXTRACTION:
            tasks.append(
                ImageExtractionTask(
                    type=task,
                    results=[],
                    targets=project.img_entities,
                    entities=[],
                )
            )

    document = Document(
        _id="",
        original_name=original_name,
        project=project.id,
        type=type,
        files=files,
        num_result=1,
        tasks=tasks,
        last_request=0
    )

    insert_document(document)
