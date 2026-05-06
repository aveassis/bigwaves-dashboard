# BigWaves Dashboard — Docker
# Gebruik: docker compose up -d
FROM python:3.13-slim

WORKDIR /app

# Installeer systeem fonts voor PDF
RUN apt-get update && apt-get install -y --no-install-recommends \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Installeer Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopieer app
COPY . .

# Kopieer fonts voor fpdf2
RUN mkdir -p fonts && \
    cp /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf fonts/ && \
    cp /usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf fonts/

EXPOSE 8501

CMD ["streamlit", "run", "dashboard.py", "--server.port", "8501", "--server.headless", "true", "--server.enableCORS", "false"]
