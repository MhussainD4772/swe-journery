# Start from the slim Python image
FROM python:3.14-slim

# Create /app inside the image and make it the current folder.
# Every instruction after this runs inside /app.

WORKDIR /app

# Copy the uv program out of uv's official image into ours
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy ONLY the dependency files first
COPY pyproject.toml uv.lock ./

# Install the dependencies (not your code yet)
RUN uv sync --frozen --no-dev --no-install-project

# Copy the app code 
COPY . .

# Put the image's .venv first on the PATH, so "uvicorn" and "python"
# refer to the ones inside /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# The command that runs when a container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]