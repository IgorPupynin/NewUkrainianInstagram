import cloudinary.uploader

from src.conf.config import settings


class UploadService:
    cloudinary.config(
        cloud_name=settings.cloud_name,
        api_key=settings.cloud_api_key,
        api_secret=settings.cloud_api_secret,
        secure=True
    )


