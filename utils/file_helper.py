# utils/file_utils.py
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import current_app
import logging

logger = logging.getLogger(__name__)

def save_uploaded_file(file, prefix: str = "import") -> str:
    if not file or not file.filename:
        raise ValueError("Invalid file")

    original_name = secure_filename(file.filename)
    name, ext = os.path.splitext(original_name)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    new_filename = f"{prefix}_{timestamp}_{name}{ext}"
    upload_path = os.path.join(current_app.config["UPLOAD_FOLDER"], new_filename)

    os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)

    file.save(upload_path)
    logger.info(f"Saved uploaded file: {upload_path}")

    return upload_path