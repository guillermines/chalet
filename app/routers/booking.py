from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.get("/", response_model=List[schemas.BookingOut])
def get_bookings(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    start_search: Optional[str] = "",
    end_search: Optional[str] = "",
):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()

    # posts = (
    #     db.query(models.Post)
    #     .filter(models.Post.title.contains(search))
    #     .limit(limit)
    #     .offset(offset=skip)
    #     .all()
    # )
    # The following line is used to shows only user's posts.
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    results = (
        db.query(
            models.Booking,
            func.count(models.Validation.booking_id).label("validations"),
        )
        .join(
            models.Validation,
            models.Validation.booking_id == models.Booking.id,
            isouter=True,
        )
        .group_by(models.Booking.id)
        # .filter(models.Booking.title.contains(search))
        .limit(limit)
        .offset(offset=skip)
        .all()
    )
    return results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Booking)
def create_bookings(
    booking: schemas.BookingCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    new_booking = models.Booking(owner_id=current_user.id, **booking.dict())
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking


# @app.get("/posts/latest")
# def get_post(id: int):
#     post = my_posts[-1]
#     return {"post_detail": post}


@router.get("/{id}", response_model=schemas.BookingOut)
def get_booking(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    booking = (
        db.query(
            models.Booking,
            func.count(models.Validation.booking_id).label("validations"),
        )
        .join(
            models.Validation,
            models.Validation.booking_id == models.Booking.id,
            isouter=True,
        )
        .group_by(models.Booking.id)
        .filter(models.Booking.id == id)
        .first()
    )
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking with id: {id} was not found",
        )
    # if post.owner_id != current_user.id :
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    return booking


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    # deleted_post = cursor.fetchone()
    booking_query = db.query(models.Booking).filter(models.Booking.id == id)
    booking = booking_query.first()
    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking with id: {id} does not exist",
        )
    if booking.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    booking_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Booking)
def update_booking(
    id: int,
    post: schemas.BookingCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute("""UPDATE posts SET title =%s, content =%s, published=%s
    # WHERE id =%s RETURNING * """, (post.title, post.content, post.published,
    # str(id)))
    booking_query = db.query(models.Booking).filter(models.Booking.id == id)
    booking = booking_query.first()
    # updated_post = cursor.fetchone()
    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking with id: {id} does not exist",
        )
    if booking.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    # conn.commit()
    booking_query.update(booking.dict(), synchronize_session=False)
    db.commit()
    return booking_query.first()
