# Temp-Note

A simple, self-destructing message service for sending encrypted messages that can only be read once by the recipient.

## Features

- End-to-end encryption using AES-GCM with 256-bit keys
- Client-side encryption/decryption (the server never sees the decrypted message)
- One-time access: Messages self-destruct after being read
- Auto-expiration: Unread messages automatically delete after a configurable time period (1-14 days)

## Built with

- **Frontend**: Vue.js with Vue Router
- **Backend**: Flask REST API
- **Database**: PostgreSQL with pg_cron

## Running the application

### Prerequisites
- Docker & Docker Compose
- `.env` file in project root (copy from `example.env`)

### Development
```bash
# Clone the repository
git clone https://github.com/ppaabo/temp-note.git
cd temp-note

# Create environment file
cp example.env .env

# Start all services in development mode (With HMR for frontend & backend)
docker compose up --watch

# Access the application at http://localhost:5173
```

### Production
```bash
# Generate self-signed SSL certificate (or use your own)
mkdir -p .prod/frontend/certs
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout .prod/frontend/certs/selfsigned.key \
  -out .prod/frontend/certs/selfsigned.crt

# Configure Nginx (edit prod/frontend/nginx.conf)
# Replace server_name _ with your domain: yourdomain.com www.yourdomain.com

# Create production environment file
cp example.env prod/.env

# Deploy with SSL and production settings
docker compose -f docker-compose.prod.yml up -d

# Access the application at https://yourdomain.com
```



