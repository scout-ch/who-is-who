FROM python:3.13.9 AS develop

WORKDIR /app

# Dependencies
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

# Copy source files
COPY . /app

ENV FLASK_ENV=development
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 3000

CMD ["flask", "--app", "api/app", "run", "--debug", "--port", "3000"]

FROM develop AS prod
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install gunicorn
ENV FLASK_ENV=production
CMD ["gunicorn", "-b", "0.0.0.0:3000"]
