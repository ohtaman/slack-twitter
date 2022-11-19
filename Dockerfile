FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY ./ /src
RUN pip install /src/

EXPOSE 8080
ENV PYTHONUNBUFFERED True

CMD gunicorn \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind :$PORT \
    --workers 1 \
    --threads 8 \
    --timeout 0 \
    slack_twitter.main:app



