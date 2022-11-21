import argparse

parser = argparse.ArgumentParser(
    prog="Processor",
    description="Create list of similar words"
)

parser.add_argument("-o", "--out", help="Path for output text file", default="out.txt")
parser.add_argument("-m", "--model", help="Path for directory with model", default=".")
parser.add_argument("word", help="")

parser.parse_args()