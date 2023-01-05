from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, oauth2, database


router = APIRouter(prefix="/validation", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def validation(
    validation: schemas.Validation,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    booking = (
        db.query(models.Booking)
        .filter(models.Booking.id == validation.booking_id)
        .first()
    )
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"booking with id {validation.booking_id} does not exist.",
        )
    validation_query = db.query(models.Validation).filter(
        models.Validation.booking_id == validation.booking_id,
        models.Validation.user_id == current_user.id,
    )
    found_validation = validation_query.first()
    if validation.dir == 1:
        if found_validation:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user.id} has already validated booking {validation.booking_id}",
            )
        new_validation = models.Validation(
            booking_id=validation.booking_id, user_id=current_user.id
        )
        db.add(new_validation)
        db.commit()
        return {"message": "Booking successfully validated"}

    else:
        if not found_validation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Validation does not exist",
            )
        validation_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully canceled validation"}
