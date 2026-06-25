"""
applications.py

CRUD routes for internship applications.

Now protected by authentication:
each user can only access their own applications.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import InternshipApplication, User
from app.schemas import ApplicationCreate, ApplicationRead, ApplicationUpdate
from app.security import get_current_user


router = APIRouter(prefix="/applications", tags=["applications"])


def get_owned_application_or_404(
    application_id: int,
    current_user: User,
    db: Session,
) -> InternshipApplication:
    """
    Fetch one application owned by the logged-in user.

    This enforces authorization.

    If the application does not exist OR belongs to another user,
    return 404.
    """

    statement = select(InternshipApplication).where(
        InternshipApplication.id == application_id,
        InternshipApplication.owner_id == current_user.id,
    )

    application = db.scalar(statement)

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found.",
        )

    return application


@router.post(
    "",
    response_model=ApplicationRead,
    status_code=status.HTTP_201_CREATED,
)
def create_application(
    payload: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new internship application for the logged-in user.
    """

    application = InternshipApplication(
        **payload.model_dump(),
        owner_id=current_user.id,
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return application


@router.get("", response_model=list[ApplicationRead])
def list_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Return only the logged-in user's applications.
    """

    statement = (
        select(InternshipApplication)
        .where(InternshipApplication.owner_id == current_user.id)
        .order_by(InternshipApplication.created_at.desc())
    )

    applications = db.scalars(statement).all()

    return applications


@router.get("/{application_id}", response_model=ApplicationRead)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Return one application owned by the logged-in user.
    """

    return get_owned_application_or_404(
        application_id=application_id,
        current_user=current_user,
        db=db,
    )


@router.patch("/{application_id}", response_model=ApplicationRead)
def update_application(
    application_id: int,
    payload: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update one application owned by the logged-in user.
    """

    application = get_owned_application_or_404(
        application_id=application_id,
        current_user=current_user,
        db=db,
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
    current_user: User = Depends(get_current_user),
):
    """
    Delete one application owned by the logged-in user.
    """

    application = get_owned_application_or_404(
        application_id=application_id,
        current_user=current_user,
        db=db,
    )

    db.delete(application)
    db.commit()

    return None