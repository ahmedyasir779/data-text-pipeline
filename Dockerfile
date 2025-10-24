# Stage 1: Builder
FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy Docker-specific requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt
RUN pip install --no-cache-dir --user streamlit
# Download NLTK data
RUN python -c "import nltk; \
    nltk.download('punkt', quiet=True); \
    nltk.download('punkt_tab', quiet=True); \
    nltk.download('stopwords', quiet=True); \
    nltk.download('wordnet', quiet=True); \
    nltk.download('omw-1.4', quiet=True); \
    nltk.download('averaged_perceptron_tagger', quiet=True); \
    nltk.download('averaged_perceptron_tagger_eng', quiet=True)"

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Download TextBlob corpora (FIXED METHOD)
RUN python -m textblob.download_corpora


# Stage 2: Runtime
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local
COPY --from=builder /root/nltk_data /root/nltk_data

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data output logs .cache

# Set Python to run in unbuffered mode (see output in real-time)
ENV PYTHONUNBUFFERED=1

# Expose port (for future web interface)
EXPOSE 8501

# Health check
# HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
#     CMD python -c "import sys; sys.exit(0)"

# Default command

# Expose Streamlit port
EXPOSE 8501

# Health check for Streamlit
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run Streamlit app by default
CMD streamlit run app.py \
    --server.port=${PORT:-8501} \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --browser.serverAddress="0.0.0.0" \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false