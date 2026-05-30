FROM python:3.13

RUN apt-get update
RUN apt-get install stockfish

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV STOCKFISH_PATH='/usr/games/stockfish'
ENV PORT=8000
ENV HOST=0.0.0.0

ENV UVICORN_PORT=$PORT
ENV UVICORN_HOST=$HOST

EXPOSE $PORT

CMD ["uvicorn", "main:app"]