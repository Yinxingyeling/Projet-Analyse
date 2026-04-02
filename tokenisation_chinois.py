import jieba
from pathlib import Path

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


chemin = "docs/"
corpus = reader(parcourir_arborescence(chemin))

tokens = jieba.lcut(corpus)

for tok in tokens:
    print(tok)
print(len(tokens))