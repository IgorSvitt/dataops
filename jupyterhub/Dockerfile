FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends npm nodejs \
    && npm install -g configurable-http-proxy \
    && pip install --no-cache-dir jupyterhub jupyterlab \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /srv/jupyterhub
COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py

EXPOSE 8000
CMD ["jupyterhub", "-f", "/srv/jupyterhub/jupyterhub_config.py"]
