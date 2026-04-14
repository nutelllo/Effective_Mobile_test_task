# Effective Mobile — Тестовое задание DevOps

Минимальное веб-приложение, запущенное в Docker-контейнерах.  
nginx выступает reverse proxy и проксирует все запросы на Python HTTP бэкенд.

---

## Архитектура

```
Клиент
  │
  │  HTTP :80
  ▼
┌─────────────────────────────┐
│  nginx  (em_nginx)          │  ← публикует порт 80
│  reverse proxy              │
└──────────────┬──────────────┘
               │ HTTP :8080 (только внутри docker-сети)
               ▼
┌─────────────────────────────┐
│  Python backend (em_backend)│  ← порт не публикуется
│  http.server на порту 8080  │
└─────────────────────────────┘

Оба контейнера находятся в одной Docker bridge-сети: em_network
```

**Используемые технологии:**

| Компонент     | Технология          |
|---------------|---------------------|
| Backend       | Python 3.12 alpine  |
| Proxy         | nginx 1.27 alpine   |
| Оркестрация   | Docker Compose v2   |

---

## Структура проекта

```
.
├── backend/
│   ├── Dockerfile   # Python-образ: non-root пользователь, healthcheck, без .pyc
│   └── app.py       # Простой HTTP-сервер (http.server)
├── nginx/
│   ├── Dockerfile   # Удаляет дефолтный конфиг, копирует свой
│   └── nginx.conf   # Reverse proxy: proxy_pass, заголовки, server_tokens off
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## Быстрый старт

### Требования

- Docker ≥ 24
- Docker Compose ≥ 2.20

### 1. Клонировать репозиторий

```bash
git clone https://github.com/<ваш-username>/<репозиторий>.git
cd <репозиторий>
```

### 2. (Опционально) Настроить порт

```bash
cp .env.example .env
# Отредактируйте NGINX_PORT если порт 80 уже занят
```

### 3. Собрать и запустить

```bash
docker compose up -d --build
```

### 4. Проверить результат

```bash
curl http://localhost
```

Ожидаемый ответ:

```
Hello from Effective Mobile!
```

### 5. Остановить

```bash
docker compose down
```

---

## Как это работает

1. **nginx** слушает порт 80 на хосте и проксирует все запросы на бэкенд через `proxy_pass http://backend:8080`.
2. **backend** (`em_backend`) запускает чистый Python HTTP-сервер на порту 8080 внутри сети `em_network`. Порт **не публикуется** на хост.
3. Docker Compose запускает nginx только после того, как бэкенд прошёл healthcheck (проверка через `urllib` на `/`).
4. nginx передаёт заголовки `Host`, `X-Real-IP` и `X-Forwarded-For` для корректной идентификации клиента.
5. Оба контейнера работают с ограничениями безопасности: `no-new-privileges`, запуск не от root, `read_only` файловая система у бэкенда.
