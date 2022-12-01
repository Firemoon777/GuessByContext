import os
import re
from pathlib import Path
from typing import Union

from pymystem3 import Mystem
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

m = Mystem()


@app.get("/game")
def read_root():
    games = [name.replace(".txt", "") for name in os.listdir("out")]
    games.sort(reverse=True)
    return games


class GuessRequest(BaseModel):
    game_id: str
    word: str


@app.post("/guess")
def guess_item(r: GuessRequest):
    if not re.match(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", r.game_id):
        return {"error": "no game found"}

    game_path = Path("out") / f"{r.game_id}.txt"
    if game_path.exists() is False:
        return {"error": "no game found"}

    print(f"before {r.word}")
    r.word = r.word.lower()
    lemma = m.lemmatize(r.word)[0]
    print(f"{r.word} --> {lemma}")

    with game_path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if line[:-1] == lemma:
                return {
                    "word": r.word,
                    "lemma": lemma,
                    "distance": i
                }
    return {
        "word": r.word,
        "distance": -1
    }