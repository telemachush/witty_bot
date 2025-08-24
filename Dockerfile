# Use Ubuntu as base image for Ollama compatibility
FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV OLLAMA_HOST=0.0.0.0
ENV OLLAMA_ORIGINS=*

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    wget \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.ai/install.sh | sh

# Create app directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Create virtual environment and install Python dependencies
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create a startup script
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
# Start Ollama in the background\n\
echo "Starting Ollama..."\n\
ollama serve &\n\
OLLAMA_PID=$!\n\
\n\
# Wait for Ollama to be ready\n\
echo "Waiting for Ollama to start..."\n\
for i in {1..30}; do\n\
    if curl -s http://127.0.0.1:11434/api/tags > /dev/null 2>&1; then\n\
        echo "Ollama is ready!"\n\
        break\n\
    fi\n\
    echo "Waiting for Ollama... ($i/30)"\n\
    sleep 2\n\
done\n\
\n\
# Pull the model if not already present\n\
echo "Setting up Ollama model..."\n\
ollama pull tinyllama:1b || echo "Model pull failed, will use templates"\n\
\n\
# Start the Flask app\n\
echo "Starting Witty Bot..."\n\
exec python app_http.py\n\
' > /app/start.sh && chmod +x /app/start.sh

# Expose port
EXPOSE 5500

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:5500/health || exit 1

# Start the application
CMD ["/app/start.sh"]
