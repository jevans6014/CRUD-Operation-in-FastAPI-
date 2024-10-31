from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import models, schemas


def create(db: Session, order_detail: schemas.OrderDetailCreate):
    # Create a new instance of the OrderDetail model with the provided data
    db_order_detail = models.OrderDetail(
        order_id=order_detail.order_id,
        sandwich_id=order_detail.sandwich_id,
        quantity=order_detail.quantity,
        price=order_detail.price
    )
    # Add the newly created OrderDetail object to the database session
    db.add(db_order_detail)
    # Commit the changes to the database
    db.commit()
    # Refresh the OrderDetail object to ensure it reflects the current state in the database
    db.refresh(db_order_detail)
    # Return the newly created OrderDetail object
    return db_order_detail


def read_all(db: Session):
    # Query and return all OrderDetail records from the database
    return db.query(models.OrderDetail).all()


def read_one(db: Session, order_detail_id: int):
    # Query the database for a specific OrderDetail by its ID
    return db.query(models.OrderDetail).filter(models.OrderDetail.id == order_detail_id).first()


def update(db: Session, order_detail_id: int, order_detail: schemas.OrderDetailUpdate):
    # Query the database for the specific order detail to update
    db_order_detail = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_detail_id)
    if db_order_detail.first() is None:
        raise HTTPException(status_code=404, detail="Order Detail not found")

    # Extract the update data from the provided 'order_detail' object
    update_data = order_detail.model_dump(exclude_unset=True)
    # Update the database record with the new data, without synchronizing the session
    db_order_detail.update(update_data, synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return the updated order detail record
    return db_order_detail.first()


def delete(db: Session, order_detail_id: int):
    # Query the database for the specific order detail to delete
    db_order_detail = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_detail_id)
    if db_order_detail.first() is None:
        raise HTTPException(status_code=404, detail="Order Detail not found")

    # Delete the database record without synchronizing the session
    db_order_detail.delete(synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return a response with a status code indicating success (204 No Content)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


