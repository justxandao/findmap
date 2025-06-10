import cv2
from PIL import Image
import numpy as np

def encontrar_e_recortar_imagem_referencia(captura_path, referencia_path):
    imagem_captura = cv2.imread(captura_path)
    imagem_referencia = cv2.imread(referencia_path)

    if imagem_captura is None or imagem_referencia is None:
        print("Erro ao carregar as imagens.")
        return None

    captura_gray = cv2.cvtColor(imagem_captura, cv2.COLOR_BGR2GRAY)
    referencia_gray = cv2.cvtColor(imagem_referencia, cv2.COLOR_BGR2GRAY)

    resultado = cv2.matchTemplate(captura_gray, referencia_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(resultado)

    threshold = 0.3
    if max_val >= threshold:
        top_left = max_loc
        h, w = referencia_gray.shape[:2]
        bottom_right = (top_left[0] + w, top_left[1] + h)
        recorte = imagem_captura[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
        cv2.imwrite('recorte.png', recorte)
        cv2.imshow("Recorte", recorte)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return recorte
    else:
        print("Imagem de referência não encontrada na captura.")
        return None

def verificar_cores(imagem_path, pontos):
    imagem = Image.open(imagem_path).convert('RGB')
    largura, altura = imagem.size
    cores_encontradas = []

    for ponto in pontos:
        x, y = ponto
        if 0 <= x < largura and 0 <= y < altura:
            cor = imagem.getpixel((x, y))
            cores_encontradas.append(cor)

    return cores_encontradas
