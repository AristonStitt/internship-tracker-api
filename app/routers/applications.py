"""
applications.py

This file contains the API routes for internship applications.

CRUD means:
- Create
- Read
- Update
- Delete
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import InternshipApplication
from app.schemas import ApplicationCreate, ApplicationRead, ApplicationUpdate

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post(
    "",
    response_model=ApplicationRead,
    status_code=status.HTTP_201_CREATED,
)
def create_application(
    payload: ApplicationCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new internship application.

    Flow:
    1. Client sends JSON.
    2. FastAPI validates it using ApplicationCreate.
    3. We convert it into a SQLAlchemy model.
    4. We save it to PostgreSQL.
    5. We return the saved object.
    """

    application = InternshipApplication(**payload.model_dump())

    db.add(application)
    db.commit()
    db.refresh(application)

    return application


@router.get("", response_model=list[ApplicationRead])
def list_applications(
    db: Session = Depends(get_db),
):
    """
    Return all internship applications.
    """

    statement = select(InternshipApplication).order_by(
        InternshipApplication.created_at.desc()
    )

    applications = db.scalars(statement).all()

    return applications


@router.get("/{application_id}", response_model=ApplicationRead)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
):
    """
    Return one application by id.

    If the id does not exist, return a 404 error.
    """

    application = db.get(InternshipApplication, application_id)

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found.",
        )

    return application


@router.patch("/{application_id}", response_model=ApplicationRead)
def update_application(
    application_id: int,
    payload: ApplicationUpdate,
    db: Session = Depends(get_db),
):
    """
    Update part of an application.

    exclude_unset=True means:
    only update the fields the client actually sent.
    """

    application = db.get(InternshipApplication, application_id)

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found.",
        )

    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(application, field, value)

    db.commit()
    db.refresh(application)

    return application


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete one application by id.
    """

    application = db.get(InternshipApplication, application_id)

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found.",
        )

    db.delete(application)
    db.commit()

    return None