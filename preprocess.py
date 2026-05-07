import os
import re
import csv
import jieba
from tokenisation_chinois import nettoyage

chemin = "data/deepseek/"
final_file = "final_ds_corpus.txt"
# chapitre = [16, 18, 29, 30, 31, 38]
chapitre = [16, 18, 29, 38]



def union_file(path:str, final_file:str, chapitre:list[int], ia:str, meta:bool=False) :
    """
        Réuni les fichiers écrites par IA avec tokenisation
    """
    final_path = path + final_file
    metadata = []

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

                    if meta:
                        metadata.append({
                        "fichier": final_path,
                        "chapitre": i,
                        "ia": ia
                })
            else :  
                continue

def tokenizer_file(path:str, chapitre:list[int], ia:str, meta:bool=False) :
    """ 
        Prétraitement pour TXM :
        - Tokenise tous le fichier d'origine 
        - Sauvegarde dans un nouveau fichier
    """
    metadata = []

    for i in chapitre :
        inputfile = f"{path}chap_{i}.txt"
        outputfile = f"{path}{ia}_chap_{i}.txt"
        if os.path.isfile(inputfile) :
            with open(inputfile, "r", encoding="utf-8") as entry, open(outputfile, "w", encoding="utf-8") as out :
                texte = entry.read()

                texte = nettoyage(texte)

                # Uniformiser les retours ligne
                texte = texte.replace("\r\n", "\n").replace("\r", "\n")

                # Supprimer les lignes vides multiples
                # -> conserve un seul saut de paragraphe
                texte = re.sub(r"\n\s*\n+", "\n\n", texte)

                # Supprimer espaces inutiles
                texte = re.sub(r"[ \t]+", " ", texte)

                # Tokenisation jieba
                tokens = jieba.lcut(texte)

                out.write(" ".join(tokens))

            print(f"\n Fichier traité : {outputfile}")

            # Métadonnées
            if meta:
                metadata.append({
                    "fichier": f"{ia}_chap_{i}.txt",
                    "chapitre": i,
                    "ia": ia
                })

        else:
            print(f"Fichier introuvable : {inputfile}")

chemins = {
    "deepseek" : "ds", 
    "chatgpt" : "gpt", 
    "claude" : "cld", 
    "qwen" : "qw"
}

for chemin, file in chemins.items() :
    path = f"data/{chemin}/"
    final_file = f"final_{file}_corpus.txt"

    print(f"Dossier {chemin} en cours de traitement.\n")
    union_file(path, final_file, chapitre, file)
    tokenizer_file(path, chapitre, file)
    print(f"\n Sauvegardé dans : {final_file}")
    