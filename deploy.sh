#!/usr/bin/env bash
# BigWaves Dashboard — VPS Deployment Script
# Usage: bash deploy.sh
# Dit script installeert alles wat nodig is om het dashboard in productie te draaien.
set -euo pipefail

echo "🌊 BigWaves Dashboard Deployment"
echo "================================"
echo ""

# ─── Configuratie ──────────────────────────────────────
DOMAIN="${DOMAIN:-dashboard.bigwaves.ai}"
PORT="${PORT:-8501}"
ADMIN_EMAIL="${ADMIN_EMAIL:-tristan@bigwaves.ai}"
DASHBOARD_DIR="${DASHBOARD_DIR:-/opt/bigwaves-dashboard}"

# ─── 1. Systeem updates ────────────────────────────────
echo "[1/6] Systeem updates..."
apt-get update -qq
apt-get upgrade -y -qq

# ─── 2. Installeer dependencies ────────────────────────
echo "[2/6] Installeren dependencies..."
apt-get install -y -qq \
    python3 \
    python3-pip \
    python3-venv \
    nginx \
    certbot \
    python3-certbot-nginx \
    git \
    curl

# ─── 3. Maak project directory ─────────────────────────
echo "[3/6] Project directory..."
mkdir -p "$DASHBOARD_DIR"

# Kopieer dashboard bestanden (verwacht dat dit script in dezelfde dir staat)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ "$SCRIPT_DIR" != "$DASHBOARD_DIR" ]; then
    echo "Kopieren bestanden naar $DASHBOARD_DIR..."
    cp -r "$SCRIPT_DIR"/* "$DASHBOARD_DIR/"
fi

cd "$DASHBOARD_DIR"

# ─── 4. Python virtual environment ─────────────────────
echo "[4/6] Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
pip install -q --upgrade pip
pip install -q streamlit plotly fpdf2

# Check fonts voor PDF
mkdir -p fonts
if [ -d "/usr/share/fonts/truetype/dejavu" ]; then
    cp /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf fonts/
    cp /usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf fonts/
    echo "  Fonts gekopieerd"
fi

# ─── 5. Nginx configuratie ─────────────────────────────
echo "[5/6] Nginx configuratie..."
cat > /etc/nginx/sites-available/bigwaves-dashboard <<NGINX
server {
    listen 80;
    server_name $DOMAIN;

    # Streamlit draait op localhost:$PORT
    location / {
        proxy_pass http://127.0.0.1:$PORT;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;

        # Timeouts voor streaming responses
        proxy_read_timeout 86400;
        proxy_send_timeout 86400;
    }

    # Health check
    location /health {
        access_log off;
        return 200 "OK";
    }
}
NGINX

# Activeer site
ln -sf /etc/nginx/sites-available/bigwaves-dashboard /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx

# ─── 6. Systemd service ───────────────────────────────
echo "[6/6] Systemd service..."
cat > /etc/systemd/system/bigwaves-dashboard.service <<SERVICE
[Unit]
Description=BigWaves Performance Dashboard
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$DASHBOARD_DIR
ExecStart=$DASHBOARD_DIR/venv/bin/streamlit run dashboard.py --server.port $PORT --server.headless true --server.enableCORS false
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
SERVICE

systemctl daemon-reload
systemctl enable bigwaves-dashboard
systemctl start bigwaves-dashboard

echo ""
echo "✅ Dashboard is live!"
echo "   http://$DOMAIN"
echo ""
echo "Wil je HTTPS (SSL) inschakelen? Voer dan uit:"
echo "   certbot --nginx -d $DOMAIN --non-interactive --agree-tos -m $ADMIN_EMAIL"
echo ""
echo "Status checken:"
echo "   systemctl status bigwaves-dashboard"
echo "   journalctl -u bigwaves-dashboard -f"
