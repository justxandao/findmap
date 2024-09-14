import cv2
import numpy as np

def encontrar_e_recortar_imagem_referencia(captura_path, referencia_path):
    # Carregar as imagens
    imagem_captura = cv2.imread(captura_path)
    imagem_referencia = cv2.imread(referencia_path)
    
    if imagem_captura is None:
        print(f"Erro ao carregar a captura de tela: {captura_path}")
        return None
    
    if imagem_referencia is None:
        print(f"Erro ao carregar a imagem de referência: {referencia_path}")
        return None

    # Obter as dimensões da imagem de referência
    w, h = imagem_referencia.shape[1], imagem_referencia.shape[0]

    # Realizar a correspondência de modelo
    resultado = cv2.matchTemplate(imagem_captura, imagem_referencia, cv2.TM_CCOEFF_NORMED)

    # Encontrar a localização com a maior correspondência
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(resultado)

    threshold = 0.3  # Ajuste o limiar conforme necessário
    if max_val >= threshold:
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        recorte = imagem_captura[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

        recorte_path = 'recorte.png'
        cv2.imwrite(recorte_path, recorte)
        print(f"Recorte da imagem salvo em {recorte_path}")
        return recorte_path
    else:
        print("A imagem de referência não foi encontrada na captura de tela.")
        return None
