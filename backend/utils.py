import os
from PIL import Image

def carregar_imagens(pasta):
    imagens = {}
    for root, _, files in os.walk(pasta):
        for nome_arquivo in files:
            if nome_arquivo.endswith(".png"):
                caminho = os.path.join(root, nome_arquivo)
                imagem = Image.open(caminho).convert('RGB')
                imagens[caminho] = imagem
    return imagens
