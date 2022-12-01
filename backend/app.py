import datetime
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
    games = list()
    for name in os.listdir("out"):
        game_name = name.replace(".txt", "")

        if is_game_valid(game_name):
            games.append(game_name)

    games.sort(reverse=True)
    return games


def is_game_valid(game_id) -> bool:
    now = datetime.date.today()

    match = re.match(r"([0-9]{4})-([0-9]{2})-([0-9]{2})", game_id)
    if not match:
        return False

    game_day = datetime.date(
        int(match.group(1)),
        int(match.group(2)),
        int(match.group(3))
    )
    if game_day > now:
        return False

    game_path = Path("out") / f"{game_id}.txt"
    if game_path.exists() is False:
        return False

    return True


class GuessRequest(BaseModel):
    game_id: str
    word: str


@app.post("/guess")
def guess_item(r: GuessRequest):
    if not is_game_valid(r.game_id):
        return {"error": "no game found"}

    r.word = r.word.lower().strip()
    lemma = m.lemmatize(r.word)[0]
    print(f"{r.word} --> {lemma}")

    game_path = Path("out") / f"{r.game_id}.txt"
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


class TipRequest(BaseModel):
    game_id: str
    distance: int

@app.post("/tip")
def tip(r: TipRequest):
    if not is_game_valid(r.game_id):
        return {"error": "no game found"}

    r.distance = max(1, r.distance)

    game_path = Path("out") / f"{r.game_id}.txt"
    with game_path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i == r.distance:
                return {
                    "word": line.strip(),
                    "lemma": line.strip(),
                    "distance": i
                }
    return {
        "word": "",
        "lemma": "",
        "distance": -1
    }