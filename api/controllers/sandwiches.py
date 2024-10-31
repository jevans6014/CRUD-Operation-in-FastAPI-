from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import models, schemas


def create(db: Session, sandwich: schemas.SandwichCreate):
    # Create a new instance of the Sandwich model with the provided data
    db_sandwich = models.Sandwich(
        name=sandwich.name,
        description=sandwich.description,
        price=sandwich.price
    )
    # Add the newly created Sandwich object to the database session
    db.add(db_sandwich)
    # Commit the changes to the database
    db.commit()
    # Refresh the Sandwich object to ensure it reflects the current state in the database
    db.refresh(db_sandwich)
    # Return the newly created Sandwich object
    return db_sandwich


def read_all(db: Session):
    # Retrieve all Sandwich records from the database
    return db.query(models.Sandwich).all()


def read_one(db: Session, sandwich_id: int):
    # Retrieve a specific Sandwich record by its ID
    db_sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id).first()
    # Check if the Sandwich exists, and raise a 404 error if not found
    if db_sandwich is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich not found")
    return db_sandwich


def update(db: Session, sandwich_id: int, sandwich: schemas.SandwichUpdate):
    # Query the database for the specific sandwich to update
    db_sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id)
    if db_sandwich.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich not found")
    # Extract the update data from the provided 'sandwich' object
    update_data = sandwich.model_dump(exclude_unset=True)
    # Update the database record with the new data, without synchronizing the session
    db_sandwich.update(update_data, synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return the updated sandwich record
    return db_sandwich.first()


def delete(db: Session, sandwich_id: int):
    # Query the database for the specific sandwich to delete
    db_sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id)
    if db_sandwich.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich not found")
    # Delete the database record without synchronizing the session
    db_sandwich.delete(synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return a response with a status code indicating success (204 No Content)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
