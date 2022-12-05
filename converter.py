import os
import json

for filename in os.listdir("out"):
    data = {}

    old_file = f"out/{filename}"
    new_file = f"frontend/public/game/{filename.replace('txt', 'json')}"

    print(f"{old_file} -> {new_file}")

    with open(old_file, encoding="utf-8") as f:
        for index, line in enumerate(f):
            data[line.strip()] = index

    with open(new_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)