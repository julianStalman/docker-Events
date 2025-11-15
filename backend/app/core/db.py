from sqlalchemy import select
from sqlalchemy.orm import Session

from .config import settings

from app.database.session import Base, engine
from app.schemas import user as schemas
from app.crud import user as crud

# models must be imported and registered from app.models to create the tables
from app.models.user import User


from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import Base, engine
from app.models.user import User
from app.schemas.user import UserCreate
from app.crud.user import create_user
from app.core.config import settings
from enums.UserRole import UserRole


def init_db(session: Session) -> None:
    """
    Initialize the database: create tables and bootstrap an initial admin user.
    """

    Base.metadata.create_all(bind=engine)

    admin_user = session.execute(
        select(User).where(User.email == "admin@admin.com")
    ).scalar_one_or_none()

    if not admin_user:
        admin_in = UserCreate(
            email= "admin@admin.com",
            name= "admin",         
            password="admin",
            role=UserRole.ADMIN                      
        )

        create_user(db=session, user=admin_in)

        session.commit()

