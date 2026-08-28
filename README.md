# Satis API

Satis API is a backend service powered by FastAPI and RQ (Redis Queue). It receives GitHub push webhooks and automatically updates and builds a private PHP Composer [Satis](https://github.com/composer/satis) repository.

## Features

- **FastAPI Endpoints**: Handlers for receiving GitHub `push` event webhooks.
- **RQ Async Workers**: Sequentially executes `composer satis:add` and `composer satis:build` inside a worker queue to prevent race conditions.
- **Exclusive Lock**: Employs `fcntl` file locking to ensure only one build job runs at a time, protecting the integrity of your Satis registry.
- **Environment Configuration**: Easy environment setup via `.env` files.

---

## Prerequisites

Before running this project, ensure you have the following installed on your system:

1. **Python 3.14+** (using [uv](https://github.com/astral-sh/uv) is highly recommended for package management)
2. **Redis** (required by RQ for queue and job management)
3. **Composer** & **Satis** (installed globally or accessible in your shell, matching the `SATIS_DIR` path)

---

## Installation & Setup

### 1. Install `uv` (Fast Python Package Installer)

If `uv` is not installed on your server, you can install it using the official script:

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Configure shell environment (or restart terminal)
source $HOME/.local/bin/env
```

### 2. Install Project Dependencies

Once `uv` is installed, run `uv sync` to automatically create a virtual environment (`.venv`) and install all required dependencies:

```bash
uv sync
```

### 3. Configure the Environment

Copy the example configuration to create your local `.env` file:

```bash
cp .env.example .env
```

Open and edit the `.env` file to match your environment settings:

```ini
# Path to your Satis registry directory
SATIS_DIR="/path/to/satis"

# Redis connection settings
REDIS_HOST="127.0.0.1"
REDIS_PORT=6379

# RQ Queue Name
QUEUE_NAME="satis"
```

---

## Running the Application

It is recommended to run the API server and the RQ worker in separate terminal windows.

### 1. Run the FastAPI Server

```bash
uv run uvicorn main:app --reload --port 9000
```

Once running, you can access the interactive Swagger API documentation at [http://localhost:9000/docs](http://localhost:9000/docs).

### 2. Run the RQ Worker

```bash
uv run python worker.py
```

---

## API Endpoints & Testing

### GitHub Webhook

- **URL**: `POST /github/webhook`
- **Header**: `X-GitHub-Event: push`
- **Payload**: JSON format, containing the SSH URL of the pushed repository.

#### Testing with cURL

```bash
curl -X POST http://localhost:9000/github/webhook \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: push" \
  -d '{"repository":{"ssh_url":"git@github.com:vendor/repo.git"}}'
```

---

## Production Deployment (systemd)

To deploy the API and the background worker in a production environment (e.g., Ubuntu/Debian server), you can set them up as systemd services.

Assuming your project is deployed at `/var/www/satis-api` and runs under the `www-data` user:

### 1. API Service Unit File

Create a service file at `/etc/systemd/system/satis-api.service`:

```ini
[Unit]
Description=Satis API Application
After=network.target redis.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/satis-api
ExecStart=/var/www/satis-api/.venv/bin/uvicorn main:app --host 127.0.0.1 --port 9000
Restart=always

[Install]
WantedBy=multi-user.target
```

### 2. Worker Service Unit File

Create a service file at `/etc/systemd/system/satis-worker.service`:

```ini
[Unit]
Description=Satis API RQ Worker
After=network.target redis.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/satis-api
ExecStart=/var/www/satis-api/.venv/bin/python worker.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### 3. Enable and Start Services

Reload the systemd daemon, then start and enable both services:

```bash
# Reload systemd configuration
sudo systemctl daemon-reload

# Start services
sudo systemctl start satis-api satis-worker

# Enable services to run on boot
sudo systemctl enable satis-api satis-worker

# Check service status
sudo systemctl status satis-api satis-worker
```
