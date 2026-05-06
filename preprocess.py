import os
import jieba
from tokenisation_chinois import nettoyage

chemin = "data/deepseek/"
final_file = "final_ds_corpus.txt"
chapitre = [16, 18, 29, 30, 31, 38]



def union_file(path:str, final_file:str, chapitre:list[int]) :
    """
        Réuni les fichiers écrites par IA avec tokenisation
    """
    final_path = path + final_file

    with open(final_path, "w", encoding="utf-8") as final:
        for i in chapitre:
            file = f"{path}chap_{i}.txt"
            if os.path.isfile(file):
                with open(file, "r", encoding="utf-8") as f:
                    content = "".join(line for line in f if line.strip())
                    clean_content = nettoyage(content) # nettoyage du contenu (au cas où)
                    tokens = " ".join(jieba.lcut(clean_content)) # tokenisation
                    tokens = "\n".join(line.strip() for line in tokens.splitlines()) # enlève les espaces en début et fin de ligne
                    final.write(tokens)

chemins = {
    "deepseek" : "ds", 
    "chatgpt" : "gpt", 
    "claude" : "cld", 
    "qwen" : "qw"
}

for chemin, file in chemins.items() :
    path = f"date/{chemin}/"
    final_file = f"final_{file}_corpus.txt"

    print(f"Dossier {chemin} en cours de traitement.")
    union_file(path, final_file, chapitre)
    print(f"Sauvegardé dans : {final_file}")
    