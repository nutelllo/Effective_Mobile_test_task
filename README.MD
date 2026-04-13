# Effective Mobile — DevOps Test Assignment

A minimal web application running inside Docker containers.  
nginx acts as a reverse proxy and forwards all requests to a Python HTTP backend.

---

## Architecture

```
Client
  │
  │  HTTP :80
  ▼
┌─────────────────────────────┐
│  nginx  (em_nginx)          │  ← published port 80
│  reverse proxy              │
└──────────────┬──────────────┘
               │ HTTP :8080 (internal network only)
               ▼
┌─────────────────────────────┐
│  Python backend (em_backend)│  ← no published ports
│  http.server on port 8080   │
└─────────────────────────────┘

Both containers share the Docker bridge network: em_network
```

**Technologies used:**

| Component | Technology          |
|-----------|---------------------|
| Backend   | Python 3.12 alpine  |
| Proxy     | nginx 1.27 alpine   |
| Orchestration | Docker Compose  |

---

## Project structure

```
.
├── backend/
│   ├── Dockerfile   # Python image, non-root user, healthcheck
│   └── app.py       # Simple HTTP server (http.server)
├── nginx/
│   └── nginx.conf   # Reverse proxy config with upstream block
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## Quick start

### Prerequisites

- Docker ≥ 24
- Docker Compose ≥ 2.20

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

### 2. (Optional) Configure the host port

```bash
cp .env.example .env
# Edit NGINX_PORT if port 80 is already in use on your machine
```

### 3. Build and start

```bash
docker compose up -d --build
```

### 4. Verify

```bash
curl http://localhost
```

Expected response:

```
Hello from Effective Mobile!
```

### 5. Stop

```bash
docker compose down
```

---

## How it works

1. **nginx** listens on host port 80 and forwards every request to the `backend` upstream via `proxy_pass`.
2. **backend** (`em_backend`) runs a pure-Python HTTP server on port 8080 inside the `em_network` Docker network. Its port is **not** published to the host.
3. Docker Compose ensures nginx starts only after the backend passes its healthcheck (`wget` on `/`).
4. nginx forwards `Host`, `X-Real-IP`, and `X-Forwarded-For` headers so the backend can identify the original client if needed.
