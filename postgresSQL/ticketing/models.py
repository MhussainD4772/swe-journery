from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, Text, func
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import DateTime


class Base(DeclarativeBase):
    pass


class Venue(Base):
    __tablename__ = "venues"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    city: Mapped[str] = mapped_column(Text)
    timezone: Mapped[str] = mapped_column(Text)

    seats: Mapped[list["Seat"]] = relationship(back_populates="venue")
    events: Mapped[list["Event"]] = relationship(back_populates="venue")


class Seat(Base):
    __tablename__ = "seats"

    id: Mapped[int] = mapped_column(primary_key=True)
    venue_id: Mapped[int] = mapped_column(ForeignKey("venues.id"))
    section: Mapped[str] = mapped_column(Text)
    row_label: Mapped[str] = mapped_column(Text)
    seat_number: Mapped[int]

    venue: Mapped["Venue"] = relationship(back_populates="seats")


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    venue_id: Mapped[int] = mapped_column(ForeignKey("venues.id"))
    title: Mapped[str] = mapped_column(Text)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    venue: Mapped["Venue"] = relationship(back_populates="events")
    tiers: Mapped[list["TicketTier"]] = relationship(back_populates="event")


class TicketTier(Base):
    __tablename__ = "ticket_tiers"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    name: Mapped[str] = mapped_column(Text)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    event: Mapped["Event"] = relationship(back_populates="tiers")
    

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(Text)
    full_name: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class EventSeat(Base):
    __tablename__ = "event_seats"

    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), primary_key=True)
    seat_id: Mapped[int] = mapped_column(ForeignKey("seats.id"), primary_key=True)
    venue_id: Mapped[int]
    tier_id: Mapped[int] = mapped_column(ForeignKey("ticket_tiers.id"))
    status: Mapped[str] = mapped_column(
        ENUM("available", "held", "sold", name="seat_status", create_type=False),
        server_default="available",
    )


class Hold(Base):
    __tablename__ = "holds"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class HoldSeat(Base):
    __tablename__ = "hold_seats"

    hold_id: Mapped[int] = mapped_column(ForeignKey("holds.id"), primary_key=True)
    event_id: Mapped[int]
    seat_id: Mapped[int] = mapped_column(primary_key=True)