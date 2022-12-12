import json
import logging
import os

from navec import Navec

logging.basicConfig(level=logging.INFO)

import argparse
import requests
import navec

from zipfile import ZipFile
from tqdm import tqdm
from pathlib import Path
from gensim.models import KeyedVectors


parser = argparse.ArgumentParser(
    prog="Processor",
    description="Create list of similar words"
)

parser.add_argument("-o", "--out", help="Path for output dir", default=".")
parser.add_argument("-n", "--name", help="Name for output file", default="word")
parser.add_argument("-m", "--model", help="Path for directory with model", default=".")
parser.add_argument("word", help="")

args = parser.parse_args()

model_dir = Path(args.model)
out_dir = Path(args.out)
word = str(args.word)
out_name = str(args.name)

# Create directories if necessary
model_dir.mkdir(parents=True, exist_ok=True)
out_dir.mkdir(parents=True, exist_ok=True)
assert out_dir.is_dir() is True

noun_only_model_txt = model_dir / "noun_model.txt"

if noun_only_model_txt.exists() is False:
    logging.info("Downloading model...")
    # Download model
    # http://vectors.nlpl.eu/repository/20/180.zip - 116
    # http://vectors.nlpl.eu/repository/20/182.zip -
    zip_path = model_dir / "182.zip"
    response = requests.get("http://vectors.nlpl.eu/repository/20/182.zip", stream=True)
    with zip_path.open("wb") as f:
        for data in tqdm(response.iter_content(chunk_size=4*1024*1024), total=153):
            f.write(data)

    logging.info("Unzipping...")
    with ZipFile(zip_path) as archive:
        archive.extractall(model_dir)

    navec_model_tar = model_dir / "navec_hudlit_v1_12B_500K_300d_100q.tar"
    response = requests.get("https://storage.yandexcloud.net/natasha-navec/packs/navec_hudlit_v1_12B_500K_300d_100q.tar", stream=True)
    with navec_model_tar.open("wb") as f:
        for data in tqdm(response.iter_content(chunk_size=4*1024*1024), total=13):
            f.write(data)

    navec = Navec.load(navec_model_tar)

    original_model_txt = model_dir / "model.txt"

    logging.info("Extracting nouns...")
    nouns = []
    # mystem = pymystem3.Mystem()
    with original_model_txt.open("r", encoding="utf-8") as f:
        for line in tqdm(f, total=185925):
            if "_NOUN" not in line or "::" in line:
                continue

            clear_line = line.replace("_NOUN", "")
            clear_word = line.split('_')[0].strip()

            if "-" in clear_word:
                continue

            if clear_word not in navec:
                print(f"Strange word: {clear_word}")
                continue

            nouns.append(clear_line)

    with noun_only_model_txt.open("w", encoding="utf-8") as f:
        f.write(f"{len(nouns)} 300\n")
        for line in nouns:
            f.write(line)
else:
    logging.info("Model found!")

logging.info("Loading model...")
model = KeyedVectors.load_word2vec_format(noun_only_model_txt, binary=False)


def create_dictionary(word: str, out_dir: Path, filename: str):
    out_txt_file: Path = out_dir / f"{filename}.txt"
    out_json_file: Path = out_dir / f"{filename}.json"
    words = {
        word: 0
    }

    with out_txt_file.open("w", encoding="utf-8") as f:
        f.write(f"{word}\n")

        for i, (similar_word, _) in enumerate(model.most_similar(positive=[word], topn=50000), 1):
            f.write(f"{similar_word}\n")
            words[similar_word] = i

    with out_json_file.open("w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False)


create_dictionary(word, out_dir, out_name)