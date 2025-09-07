from litestar.datastructures import UploadFile
from litestar.params import Body
import uuid
from pathlib import Path
from app.core.config import settings
import os

class FileUploadUtils:
    @staticmethod
    def allowed_file(filename):
        ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    @staticmethod
    def save_file(file, upload_folder):
        ...

    staticmethod
    def save_image( file: UploadFile, folder: str=None) -> str:
        """Save uploaded image and return its URL/path."""
        ext = Path(file.filename).suffix or ".jpg"
        unique_name = f"{uuid.uuid4()}{ext}"
        if folder:
            upload_folder  = settings.UPLOAD_FOLDER / folder

        else:
            upload_folder = settings.UPLOAD_FOLDER 
        os.makedirs(upload_folder, exist_ok=True)
        save_path = upload_folder / unique_name

        with open(save_path, "wb") as f:
            f.write(file.file.read())

        if folder:
            return f"/media/{folder}/{unique_name}"
        else:
            return f"/media/{unique_name}"
    
    def remove_file(self, file_path: str):
        """Remove a file from the file system."""
        os.remove(file_path)
        print("File removed successfully.")