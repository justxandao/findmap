from PIL import Image
import os
import numpy as np

def carregar_imagens(pasta):
    imagens = {}
    for root, _, files in os.walk(pasta):  # Percorre todas as subpastas
        for nome_arquivo in files:
            if nome_arquivo.endswith(".png"):
                caminho = os.path.join(root, nome_arquivo)
                imagem = Image.open(caminho).convert('RGB')  # Converte para RGB
                imagens[caminho] = imagem
    return imagens

def imagem_para_array(imagem):
    return np.array(imagem)  # Mantém a imagem em RGB

def comparar_pixel_a_pixel(imagem1_array, imagem2_array):
    """
    Compara duas imagens pixel a pixel e calcula a soma das diferenças absolutas.
    """
    if imagem1_array.shape != imagem2_array.shape:
        raise ValueError("As imagens devem ter o mesmo tamanho para comparação pixel a pixel.")
    diferenca_total = np.sum(np.abs(imagem1_array - imagem2_array))
    return diferenca_total

def comparar_imagens(imagem_capturada, imagens_referencia):
    imagem_capturada = Image.open(imagem_capturada).convert('RGB')  # Converte para RGB
    imagem_capturada_array = imagem_para_array(imagem_capturada)

    scores = []

    for caminho, imagem_referencia in imagens_referencia.items():
        imagem_referencia_array = imagem_para_array(imagem_referencia)

        # Verifica as dimensões das imagens
        if imagem_capturada_array.shape != imagem_referencia_array.shape:
            continue  # Ignora imagens com dimensões diferentes

        # Calcula a diferença total pixel a pixel
        try:
            diferenca_total = comparar_pixel_a_pixel(imagem_capturada_array, imagem_referencia_array)
        except ValueError as e:
            print(f"Erro na comparação pixel a pixel: {e}")
            continue
        
        # Calcula a pontuação como o inverso da diferença total
        score = 1 / (1 + diferenca_total)  # Quanto menor a diferença, maior o score

        print(f"Score para {caminho}: {score}")
        scores.append((caminho, score))

    # Ordena as imagens com base no score em ordem decrescente e seleciona as 3 melhores
    melhores_imagens = sorted(scores, key=lambda x: x[1], reverse=True)[:3]

    return melhores_imagens

def comparar_completo(imagem_capturada_path, pontuacoes):
    imagem_capturada = Image.open(imagem_capturada_path).convert('RGB')
    imagem_capturada_array = np.array(imagem_capturada)

    melhor_imagem = None
    melhor_score = -1
    melhor_diferenca_total = None

    for imagem_referencia_path, score in pontuacoes:
        imagem_referencia = Image.open(imagem_referencia_path).convert('RGB')
        imagem_referencia_array = np.array(imagem_referencia)

        # Comparação pixel a pixel
        try:
            diferenca_total = comparar_pixel_a_pixel(imagem_capturada_array, imagem_referencia_array)
        except ValueError as e:
            print(f"Erro na comparação pixel a pixel: {e}")
            continue

        # Atualiza a melhor correspondência
        if score > melhor_score:
            melhor_score = score
            melhor_imagem = imagem_referencia_path
            melhor_diferenca_total = diferenca_total

    return melhor_imagem, melhor_score, melhor_diferenca_total