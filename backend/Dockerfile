FROM python:3.13.7-slim AS develop

# User configuration
#RUN useradd -ms /bin/sh -u 1001 app
#USER app
WORKDIR /app

# Dependencies
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

# Copy source files
#COPY --chown=app:app . /app
COPY . /app

ENV FLASK_ENV=development
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

CMD ["flask", "--app", "api/app", "run", "--debug"]

FROM develop AS prod
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install gunicorn
ENV FLASK_ENV=production
CMD ["gunicorn", "-b", "0.0.0.0:5000"]
