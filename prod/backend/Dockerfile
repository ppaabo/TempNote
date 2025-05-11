FROM python:3.11-slim

RUN pip install --upgrade pip
RUN adduser --disabled-password --gecos "" worker
WORKDIR /home/worker
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

USER worker
COPY --chown=worker:worker backend/ .

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src:create_app()", "--access-logfile=-", "--error-logfile=-"]
