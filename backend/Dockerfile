FROM python:3.12-alpine

EXPOSE 8080

WORKDIR /app

COPY app.py .

HEALTHCHECK --interval=10s --timeout=5s --start-period=15s --retries=5 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/')" || exit 1

RUN adduser -D -u 1001 appuser
USER appuser

ENTRYPOINT ["python", "-u", "app.py"]
