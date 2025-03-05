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
        
        # Redimensionar a imagem de referência para o mesmo tamanho da imagem de captura
        if imagem_captura.shape != imagem_referencia.shape:
            print(f"Redimensionando {referencia_file} para corresponder ao tamanho da captura.")
            imagem_referencia = cv2.resize(imagem_referencia, (imagem_captura.shape[1], imagem_captura.shape[0]))
        
        # Verificar o tamanho da imagem para definir win_size
        min_side = min(imagem_captura.shape[0], imagem_captura.shape[1])
        win_size = min(7, min_side)  # win_size deve ser ímpar e menor que o menor lado da imagem
        if win_size % 2 == 0:  # Garantir que win_size seja ímpar
            win_size -= 1
        
        # Comparar imagens coloridas usando SSIM com channel_axis
        try:
            score, _ = ssim(
                imagem_captura,
                imagem_referencia,
                win_size=win_size,
                channel_axis=-1,  # Usar channel_axis para imagens coloridas
                full=True
            )
            pontuacoes[referencia_file] = score
        except ValueError as e:
            print(f"Erro ao comparar {referencia_file}: {e}")
            continue
    
    return pontuacoes