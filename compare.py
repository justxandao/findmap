import os
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

def comparar_imagens(captura_path, imagens_referencia):
    pontuacoes = {}
    
    if not os.path.exists(captura_path):
        print(f"O arquivo de captura {captura_path} não existe.")
        return pontuacoes

    imagem_captura = cv2.imread(captura_path)
    if imagem_captura is None:
        print(f"Erro ao carregar a imagem de captura: {captura_path}")
        return pontuacoes
    
    for referencia_file, referencia_img in imagens_referencia.items():
        if not os.path.exists(referencia_file):
            print(f"O arquivo de referência {referencia_file} não existe.")
            continue
        
        imagem_referencia = cv2.imread(referencia_file)
        if imagem_referencia is None:
            print(f"Erro ao carregar a imagem de referência: {referencia_file}")
            continue
        
        imagem_referencia = cv2.cvtColor(imagem_referencia, cv2.COLOR_BGR2GRAY)
        imagem_captura_gray = cv2.cvtColor(imagem_captura, cv2.COLOR_BGR2GRAY)
        
        score, _ = ssim(imagem_captura_gray, imagem_referencia, full=True)
        pontuacoes[referencia_file] = score
    
    return pontuacoes
