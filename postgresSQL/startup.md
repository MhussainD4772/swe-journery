# Start the Shop Database

This guide explains how to run the local shop database with Docker and connect to it from pgAdmin or `psql`.

## Prerequisites

- Docker Desktop must be installed and running.
- The `pg16` container must already exist.

## Connection parameters

| Setting | Value |
| --- | --- |
| Host name/address | `localhost` |
| Port | `5432` |
| Database | `shop` |
| Username | `postgres` |
| Password | `pw` |
| Container name | `pg16` |
| Docker image | `postgres:16` |
| Data volume | `pgdata` |
| pgAdmin server name | `shop` |

## Connection string

Use this format with your local credentials:

`postgresql://<username>:<password>@localhost:5432/<database>`

## Normal start (every time you reopen your laptop)

1. Open Docker Desktop. Wait until it says it's running.
2. Run:

   ```sh
   docker start pg16
   sleep 5
   docker exec pg16 pg_isready -U postgres
   ```

   Expect `accepting connections`. If you see `no response`, wait 5 seconds and rerun the last line.

3. In pgAdmin, right-click the `shop` server, choose **Connect Server**, and enter the configured password.

## Troubleshooting

### If pgAdmin says: role "postgres" does not exist

Another PostgreSQL service, such as Homebrew `postgresql@18`, may already be using port `5432`.

1. See who owns the port:

   lsof -nP -iTCP:5432 -sTCP:LISTEN

2. If it's postgres from Homebrew, stop it:

   brew services stop postgresql@18

3. Confirm the port is free (should print nothing):

   lsof -nP -iTCP:5432 -sTCP:LISTEN

4. Start the container:

   docker start pg16
   sleep 5
   docker exec pg16 pg_isready -U postgres

## If docker start says "port is already allocated"

Same cause. Do the steps in the section above.

## Sanity check the data

   docker exec pg16 psql -U postgres -d shop -c "SELECT count(*) FROM orders;"

Expect 500000.

## Open psql (for \timing and EXPLAIN)

   docker exec -it pg16 psql -U postgres -d shop

## Never run these (they delete all data)

   docker rm -v pg16
   docker volume rm pgdata

## Reload from scratch (only if the data is gone)

   docker exec pg16 psql -U postgres -c "CREATE DATABASE shop"
   docker exec -i pg16 psql -U postgres -d shop -v ON_ERROR_STOP=1 < seed.sql

## Optional: auto-start the container with Docker Desktop

   docker update --restart unless-stopped pg16