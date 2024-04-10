import os
import argparse
import re
import pandas as pd

def extract_content(text, tag_l, tag_r):
    pattern = rf'<{tag_l}[^>]*>(.*?)</{tag_r}>'
    matches = re.findall(pattern, text)
    if matches:
        return matches
    else:
        return []


def main(folder, filename):
    filepath = os.path.join(folder, filename)
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()

    data = {
        "Nom fichier": [filename],
        "Numero phrase": [""],  # 填充一个空字符串以保证列长度一致
        "Dynamique": [""],
        "Lieu_objet": [""],
        "Lieu_loc": [""],
        "Temps": [""],
        "Acteur": [""],
        "Perc": [""],
        "Doc": [""]
    }


    all_tags = [
        ("dyn", "dyn"),
        ('lieu type="obj"', "lieu"),
        ('lieu type="loc"', "lieu"),
        ("tps", "tps"),
        ("act", "act"),
        ("perc", "perc"),
        ("doc", "doc")
    ]

    for tag_l, tag_r in all_tags:
        content = extract_content(content, tag_l, tag_r)
        data[tag_l] = content

    df = pd.DataFrame(data)
    print(df)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read and extract content from a txt file.")
    parser.add_argument("-fd","--folder", help="Path to the folder containing the txt file.")
    parser.add_argument("-fn", "--filename", help="Name of the txt file to be read.")

    args = parser.parse_args()
    main(args.folder, args.filename)
