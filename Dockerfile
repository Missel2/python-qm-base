FROM python:3.13-slim-bookworm
LABEL org.opencontainers.image.source="https://github.com/Missel2/python-qm-base" \
      org.opencontainers.image.description="Python 3.13 with Django, PostgreSQL driver and scientific dependencies"
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_DISABLE_PIP_VERSION_CHECK=1
COPY requirements.txt /opt/python-qm-base/requirements.txt
RUN python -m pip install --no-cache-dir --only-binary=:all: -r /opt/python-qm-base/requirements.txt \
    && python -m pip check \
    && python -m pip freeze > /opt/python-qm-base/installed.txt
CMD ["python"]
