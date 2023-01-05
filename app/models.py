from cgi import print_arguments
from time import timezone
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, text
from sqlalchemy.sql.expression import null
from sqlalchemy.orm import relationship


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, nullable=False)
    start_date = Column(TIMESTAMP(timezone=True), nullable=False)
    end_date = Column(TIMESTAMP(timezone=True), nullable=False)
    number_of_people = Column(Integer, nullable=False, server_default="1")
    validated = Column(Boolean, server_default="FALSE", nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )  # foreign key constraint
    # The following line is fetching user data.
    owner = relationship("User")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    admin = Column(Boolean, server_default="FALSE", nullable=False)
    validated = Column(Boolean, server_default="FALSE", nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Validation(Base):
    __tablename__ = "validations"
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    booking_id = Column(
        Integer,
        ForeignKey("bookings.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
