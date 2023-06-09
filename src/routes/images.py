from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status

from schemas import ImageCreateRequest, ImageUpdateRequest, ImageResponse
from src.database.db import get_db
from src.database.models import Image, Tag

router = APIRouter(prefix="/images", tags=["images"])


@router.post("/", response_model=ImageResponse)
def create_image(image_data: ImageCreateRequest, db: Session = Depends(get_db)):
    try:
        image = Image(image=image_data.image, description=image_data.description)

        for tag_data in image_data.tags:
            tag = db.query(Tag).filter_by(name=tag_data).first()
            if not tag:
                tag = Tag(name=tag_data)
                db.add(tag)
            image.tags.append(tag)

        db.add(image)
        db.commit()
        db.refresh(image)
        return ImageResponse(
            image=image.image,
            description=image.description,
            tags=image_data.tags
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{image_id}")
def delete_image(image_id: int, db: Session = Depends(get_db)):
    try:
        image = db.query(Image).filter(Image.id == image_id).first()
        if not image:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

        db.delete(image)
        db.commit()
        return {"message": "Image deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{image_id}", response_model=ImageResponse)
def update_image(image_id: int, image_data: ImageUpdateRequest, db: Session = Depends(get_db)):
    try:
        image = db.query(Image).filter_by(id=image_id).first()
        if not image:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

        image.description = image_data.description

        for tag_data in image_data.tags:
            tag = db.query(Tag).filter_by(name=tag_data).first()
            if not tag:
                tag = Tag(name=tag_data)
                db.add(tag)
            image.tags.append(tag)

        db.commit()
        db.refresh(image)
        return ImageResponse(
            image=image.image,
            description=image.description,
            tags=image_data.tags,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{image_id}", response_model=ImageResponse)
def get_image(image_id: int, db: Session = Depends(get_db)):
    try:
        image = db.query(Image).filter(Image.id == image_id).first()
        if not image:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

        return ImageResponse(
            image=image.image,
            description=image.description,
            tags=[tag.name for tag in image.tags],
            comments=[comment.content for comment in image.comments]
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
