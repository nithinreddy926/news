# Use official slim Python image
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies required by some Python packages (FAISS, Torch, numpy)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       git \
       curl \
       ca-certificates \
       libgomp1 \
       libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*

# Create app user and set working directory
RUN useradd -m app
WORKDIR /home/app/news

# Copy project files and give ownership to the non-root user
COPY --chown=app:app . /home/app/news

# Switch to non-root user
USER app

# Upgrade packaging tools and install Python dependencies
RUN python -m pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# Expose port used by Streamlit (optional) if you later add a web UI
EXPOSE 8501

# Default entrypoint: run the CLI search script in interactive mode
# You can override this at runtime to run any of the project's scripts, for example:
# docker run -it --rm news-search python rss_to_supabase.py
ENTRYPOINT ["python", "search_news.py"]
