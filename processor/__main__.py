import logging

logging.basicConfig(level=logging.INFO)

import argparse
import requests

from zipfile import ZipFile
from tqdm import tqdm
from pathlib import Path
from gensim.models import KeyedVectors


parser = argparse.ArgumentParser(
    prog="Processor",
    description="Create list of similar words"
)

parser.add_argument("-o", "--out", help="Path for output text file", default="out.txt")
parser.add_argument("-m", "--model", help="Path for directory with model", default=".")
parser.add_argument("word", help="")

args = parser.parse_args()

model_dir = Path(args.model)
out_file = Path(args.out)
word = str(args.word)

# Create directories if necessary
model_dir.mkdir(parents=True, exist_ok=True)
out_dir = out_file.parent
out_dir.mkdir(parents=True, exist_ok=True)

noun_only_model_txt = model_dir / "noun_model.txt"

if noun_only_model_txt.exists() is False:
    logging.info("Downloading model...")
    # Download model
    # http://vectors.nlpl.eu/repository/20/180.zip
    zip_path = model_dir / "180.zip"
    response = requests.get("http://vectors.nlpl.eu/repository/20/180.zip", stream=True)
    with zip_path.open("wb") as f:
        for data in tqdm(response.iter_content(chunk_size=4*1024*1024), total=116):
            f.write(data)

    logging.info("Unzipping...")
    with ZipFile(zip_path) as archive:
        archive.extractall(model_dir)

    original_model_txt = model_dir / "model.txt"

    logging.info("Extracting nouns...")
    nouns = []
    with original_model_txt.open("r") as f:
        for line in f:
            if "_NOUN" in line and "::" not in line:
                nouns.append(line.replace("_NOUN", ""))

    with noun_only_model_txt.open("w") as f:
        f.write(f"{len(nouns)} 300\n")
        for line in nouns:
            f.write(line)
else:
    logging.info("Model found!")


logging.info("Loading model...")
model = KeyedVectors.load_word2vec_format(noun_only_model_txt, binary=False)

with out_file.open("w", encoding="utf-8") as f:
    f.write(f"{word}\n")
    for similar_word, _ in model.most_similar(positive=[word], topn=50000):
        f.write(f"{similar_word}\n")