import jieba

corpus = open("corpus.txt", "r", encoding="utf-8").read()

tokens = jieba.lcut(corpus)
for tok in tokens :
    print(tok)