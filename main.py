import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from stockfish import Stockfish

DESCRIPTION = """
This API does one thing only: it takes a chess game and returns the
best next move. This project will grow, but for now it is intended to
be a REST API to interface with the Stockfish chess engine.
"""

app = FastAPI(
    title='Chess API',
    description=DESCRIPTION,
    version='1.0.0'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


class MoveSuggestionBody(BaseModel):
    fen: str
    skill_level: int = 10
    elo_level: int | None = None


@app.get('/', tags=['Default'])
def index():
    """
    Simple GET request that returns a helpful message.
    """
    return {'message': 'Go to \'/docs\' in your browser to view the documentation.'}


@app.post('/suggest-move', tags=['Chess Engine'])
def test_chess_engine(body: MoveSuggestionBody):
    """
    Suggests a move given a chess game and skill level.

    **Body Parameters**
    - `fen` (string, required): The current board state in FEN notation.
    - `skill_level` (integer, optional): Engine strength from 0 (weakest) to 20 (strongest). Defaults to 10.
    - `elo_level` (integer, optional): Target ELO rating for the engine. When provided, takes precedence over `skill_level`.

    **Response**
    - `best_move` (string): The recommended move in UCI notation (e.g. `e2e4`), or `null` if no legal move is available.
    """
    STOCKFISH_PATH = os.getenv('STOCKFISH_PATH') or 'stockfish'

    stockfish = Stockfish(
        path=STOCKFISH_PATH,
        parameters={
            "Threads": 2, 
            "Hash": 256,
            "Skill Level": body.skill_level})
    
    if body.elo_level:
        # ELO takes precident over skill level if LimitStrength is True
        stockfish.update_engine_parameters({"UCI_LimitStrength": True, "UCI_Elo": body.elo_level})

    stockfish.set_fen_position(body.fen)
    best_move = stockfish.get_best_move()

    return {'best_move': best_move}
