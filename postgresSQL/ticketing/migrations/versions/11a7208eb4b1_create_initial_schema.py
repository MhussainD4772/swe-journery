"""create initial schema

Revision ID: 11a7208eb4b1
Revises: 
Create Date: 2026-11-07 16:50:58.981468

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '11a7208eb4b1'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    -- Venues and seats
    CREATE TABLE venues (
      id        bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
      name      text NOT NULL,
      city      text NOT NULL,
      timezone  text NOT NULL
    );

    CREATE TABLE seats (
      id          bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
      venue_id    bigint NOT NULL REFERENCES venues(id) ON DELETE CASCADE,
      section     text NOT NULL,
      row_label   text NOT NULL,
      seat_number integer NOT NULL CHECK (seat_number > 0),
      UNIQUE (venue_id, section, row_label, seat_number),
      UNIQUE (id, venue_id)
    );

    -- Events, users, tiers
    CREATE TABLE events (
      id        bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
      venue_id  bigint NOT NULL REFERENCES venues(id) ON DELETE RESTRICT,
      title     text NOT NULL,
      starts_at timestamptz NOT NULL,
      ends_at   timestamptz NOT NULL,
      CHECK (ends_at > starts_at),
      UNIQUE (id, venue_id)
    );

    CREATE TABLE users (
      id          bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
      email       text NOT NULL,
      full_name   text NOT NULL,
      created_at  timestamptz NOT NULL DEFAULT now()
    );
    CREATE UNIQUE INDEX users_email_key ON users (lower(email));

    CREATE TABLE ticket_tiers (
      id        bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
      event_id  bigint NOT NULL REFERENCES events(id) ON DELETE CASCADE,
      name      text NOT NULL,
      price     numeric(10,2) NOT NULL CHECK (price >= 0),
      UNIQUE (event_id, name),
      UNIQUE (id, event_id)
    );

    -- Per-event seat inventory
    CREATE TYPE seat_status AS ENUM ('available', 'held', 'sold');

    CREATE TABLE event_seats (
      event_id  bigint NOT NULL,
      seat_id   bigint NOT NULL,
      venue_id  bigint NOT NULL,
      tier_id   bigint NOT NULL,
      status    seat_status NOT NULL DEFAULT 'available',
      PRIMARY KEY (event_id, seat_id),
      FOREIGN KEY (event_id, venue_id) REFERENCES events(id, venue_id) ON DELETE CASCADE,
      FOREIGN KEY (seat_id, venue_id)  REFERENCES seats(id, venue_id),
      FOREIGN KEY (tier_id, event_id)  REFERENCES ticket_tiers(id, event_id)
    );

    -- Holds
    CREATE TABLE holds (
      id          bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
      user_id     bigint NOT NULL REFERENCES users(id),
      event_id    bigint NOT NULL REFERENCES events(id) ON DELETE CASCADE,
      created_at  timestamptz NOT NULL DEFAULT now(),
      expires_at  timestamptz NOT NULL,
      CHECK (expires_at > created_at),
      UNIQUE (id, event_id)
    );

    CREATE TABLE hold_seats (
      hold_id   bigint NOT NULL,
      event_id  bigint NOT NULL,
      seat_id   bigint NOT NULL,
      PRIMARY KEY (hold_id, seat_id),
      UNIQUE (event_id, seat_id),
      FOREIGN KEY (hold_id, event_id) REFERENCES holds(id, event_id) ON DELETE CASCADE,
      FOREIGN KEY (event_id, seat_id) REFERENCES event_seats(event_id, seat_id)
    );

    -- Orders and tickets
    CREATE TYPE order_status AS ENUM ('pending', 'paid', 'refunded');

    CREATE TABLE orders (
      id          bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
      user_id     bigint NOT NULL REFERENCES users(id),
      event_id    bigint NOT NULL REFERENCES events(id),
      status      order_status NOT NULL DEFAULT 'pending',
      created_at  timestamptz NOT NULL DEFAULT now(),
      UNIQUE (id, event_id)
    );

    CREATE TABLE tickets (
      id          bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
      order_id    bigint NOT NULL,
      event_id    bigint NOT NULL,
      seat_id     bigint NOT NULL,
      price_paid  numeric(10,2) NOT NULL CHECK (price_paid >= 0),
      refunded_at timestamptz,
      FOREIGN KEY (order_id, event_id) REFERENCES orders(id, event_id),
      FOREIGN KEY (event_id, seat_id)  REFERENCES event_seats(event_id, seat_id)
    );
    CREATE UNIQUE INDEX tickets_one_valid_per_seat
      ON tickets (event_id, seat_id)
      WHERE refunded_at IS NULL;

    -- Payments and refunds
    CREATE TYPE payment_status AS ENUM ('pending', 'succeeded', 'failed');

    CREATE TABLE payments (
      id               bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
      order_id         bigint NOT NULL REFERENCES orders(id),
      amount           numeric(10,2) NOT NULL CHECK (amount > 0),
      status           payment_status NOT NULL DEFAULT 'pending',
      idempotency_key  text NOT NULL UNIQUE,
      provider_payload jsonb,
      created_at       timestamptz NOT NULL DEFAULT now()
    );

    CREATE TABLE refunds (
      id          bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
      ticket_id   bigint NOT NULL UNIQUE REFERENCES tickets(id),
      payment_id  bigint NOT NULL REFERENCES payments(id),
      amount      numeric(10,2) NOT NULL CHECK (amount > 0),
      reason      text,
      created_at  timestamptz NOT NULL DEFAULT now()
    );
    """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE refunds, payments, tickets, orders, hold_seats, holds,
               event_seats, ticket_tiers, users, events, seats, venues;
    DROP TYPE payment_status, order_status, seat_status;
    """)