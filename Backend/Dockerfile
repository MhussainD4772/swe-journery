# ================= Stage 1: builder =================
# "AS builder" gives this stage a name, so stage 2 can copy from it later
FROM python:3.14-slim AS builder

# uv is only needed in this stage, to install packages
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Make uv put real copies of package files into .venv (explained below)
ENV UV_LINK_MODE=copy

# Dependency files first — same caching reason as before
COPY pyproject.toml uv.lock ./

# Install dependencies into /app/.venv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project



# ================= Stage 2: runtime =================
# A brand-new, clean slim image. Nothing from stage 1 comes along
# unless we explicitly copy it.
FROM python:3.14-slim

# Regular user — early, so it stays cached
RUN useradd --system --no-create-home --shell /usr/sbin/nologin app

WORKDIR /app

# Take ONLY the finished virtual environment from the builder stage
COPY --from=builder /app/.venv /app/.venv

# Your code
COPY . .

# Use the .venv's python and uvicorn
ENV PATH="/app/.venv/bin:$PATH"

# Build steps are done — run as the regular user from here
USER app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]