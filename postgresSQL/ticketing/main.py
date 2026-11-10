from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy import delete, func, select, tuple_, update
from sqlalchemy.orm import Session, joinedload

from db import get_session
from models import Event, EventSeat, Hold, HoldSeat, Seat, TicketTier
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

app = FastAPI()


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(Path(__file__).parent / "static" / "index.html")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/events")
def list_events(session: Session = Depends(get_session)):
    events = session.scalars(
        select(Event).options(joinedload(Event.venue)).order_by(Event.starts_at)
    ).all()
    return [
        {
            "id": e.id,
            "title": e.title,
            "venue": e.venue.name,
            "starts_at_utc": e.starts_at.isoformat(),
            "starts_at_local": e.starts_at.astimezone(ZoneInfo(e.venue.timezone)).isoformat(),
        }
        for e in events
    ]


@app.get("/events/{event_id}/seats")
def list_event_seats(event_id: int, session: Session = Depends(get_session)):
    seats = session.execute(
        select(EventSeat, Seat, TicketTier)
        .join(Seat, EventSeat.seat_id == Seat.id)
        .join(TicketTier, EventSeat.tier_id == TicketTier.id)
        .where(EventSeat.event_id == event_id)
        .order_by(Seat.section, Seat.row_label, Seat.seat_number)
    ).all()
    return [
        {
            "id": event_seat.seat_id,
            "section": seat.section,
            "row": seat.row_label,
            "number": seat.seat_number,
            "status": event_seat.status,
            "tier": tier.name,
            "price": str(tier.price),
        }
        for event_seat, seat, tier in seats
    ]


class HoldRequest(BaseModel):
    user_id: int
    event_id: int
    seat_ids: list[int]


@app.post("/holds")
def create_hold(req: HoldRequest, session: Session = Depends(get_session)):
    seat_ids = sorted(set(req.seat_ids))
    if not seat_ids:
        raise HTTPException(status_code=400, detail="Pick at least one seat")

    # 1. Lock the seat rows. Anyone else touching them waits here.
    rows = session.scalars(
        select(EventSeat)
        .where(EventSeat.event_id == req.event_id, EventSeat.seat_id.in_(seat_ids))
        .order_by(EventSeat.seat_id)
        .with_for_update()
    ).all()

    # 2. Check they all exist and are still available.
    if len(rows) != len(seat_ids) or any(r.status != "available" for r in rows):
        session.rollback()
        raise HTTPException(status_code=409, detail="One or more seats are not available")

    try:
        # 3. Create the hold, expiring in 10 minutes.
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)
        hold = Hold(user_id=req.user_id, event_id=req.event_id, expires_at=expires_at)
        session.add(hold)
        session.flush()
        hold_id = hold.id

        # 4 and 5. Record the seats in the hold and mark them held.
        for r in rows:
            session.add(HoldSeat(hold_id=hold_id, event_id=req.event_id, seat_id=r.seat_id))
            r.status = "held"

        # 6. Save everything and release the lock.
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Invalid user or seats")

    return {"hold_id": hold_id, "seat_ids": seat_ids, "expires_at": expires_at.isoformat()}

def release_expired_holds(session: Session) -> int:
    # Lock expired holds. SKIP LOCKED means other workers skip rows we already have.
    expired_ids = session.scalars(
        select(Hold.id)
        .where(Hold.expires_at < func.now())
        .with_for_update(skip_locked=True)
    ).all()
    if not expired_ids:
        return 0

    # Put their seats back on sale.
    session.execute(
        update(EventSeat)
        .where(
            tuple_(EventSeat.event_id, EventSeat.seat_id).in_(
                select(HoldSeat.event_id, HoldSeat.seat_id)
                .where(HoldSeat.hold_id.in_(expired_ids))
            )
        )
        .values(status="available")
    )

    # Delete the holds. Their hold_seats rows are deleted by the database (cascade).
    session.execute(delete(Hold).where(Hold.id.in_(expired_ids)))
    session.commit()
    return len(expired_ids)


@app.post("/admin/expire-holds")
def expire_holds(session: Session = Depends(get_session)):
    return {"released": release_expired_holds(session)}