import jieba
from pathlib import Path
import re

def parcourir_arborescence(sample: str) -> list[str]:
    """Parcours récursif avec pathlib via iterdir()."""
    p = Path(sample)
    fichiers_trouves = []
    if p.is_file() and p.suffix.lower() == ".txt":
        fichiers_trouves.append(str(p))
    elif p.is_dir():
        for element in p.iterdir():
            fichiers_trouves.extend(parcourir_arborescence(element))
    return fichiers_trouves


def reader(files: list[str]) -> str:
    """
    Lecture des fichiers et concaténation du contenu
    """
    if not files:
        return ""

    corpus = ""

    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            corpus += f.read() + "\n"  # lire le contenu

    return corpus

def nettoyage(corpus:str)->str:
    corpus = re.sub(r"简介\([^)]*\)","",corpus)
    corpus = re.sub(r"目录\([^)]*\)", "", corpus)

    corpus = re.sub(r"\b\d+\s*/\s*\d+\b", "", corpus)
    corpus = re.sub(r"\b\d+\s* /\s* \d+\b", "", corpus)

    bruits = [
        r"加大减小",
        r"跳转",
        r"字号",
        r"夜间",
        r"跳章",
        r"点击进入",
        r"上一页",
        r"下一页",
        r"点击呼出",
        r"功能菜单"
    ]
    for p in bruits:
        corpus = re.sub(p, "", corpus)


    lines = [line.strip() for line in corpus.splitlines() if line.strip()]
    nettoye = []
    seen = set()
    for line in lines:
        if line not in seen:
            nettoye.append(line)
            seen.add(line)

    return "\n".join(nettoye)

chemin = "docs/"
corpus = reader(parcourir_arborescence(chemin))
corpus_net = nettoyage(corpus)

tokens = jieba.lcut(corpus_net)

for tok in tokens:
    print(tok)
print(len(tokens))
