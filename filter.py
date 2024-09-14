import json
import os
from PIL import Image
import numpy as np
import cv2
from compare import comparar_imagens

def carregar_cores(file_path):
    if not os.path.exists(file_path):
        print(f"O arquivo {file_path} não existe.")
        return {}
    with open(file_path, 'r') as file:
        return json.load(file)

def verificar_cores(imagem_path, pontos):
    if not os.path.exists(imagem_path):
        print(f"A imagem {imagem_path} não existe.")
        return []
    
    imagem = Image.open(imagem_path).convert('RGB')
    largura, altura = imagem.size
    cores_encontradas = []

    for ponto in pontos:
        x, y = ponto
        if x < 0 or y < 0 or x >= largura or y >= altura:
            print(f"Coordenada {ponto} fora dos limites da imagem ({largura}, {altura}).")
            continue
        cor = imagem.getpixel((x, y))
        cores_encontradas.append(cor)

    return cores_encontradas

def cor_proxima(cor1, cor2, margem):
    return np.linalg.norm(np.array(cor1) - np.array(cor2)) <= margem

def buscar_pastas_por_cores(cores_encontradas, cores_referencia, margem):
    pastas_correspondentes = []
    for pasta, cores_ref in cores_referencia.items():
        for cor_encontrada in cores_encontradas:
            if any(cor_proxima(cor_encontrada, cor_ref, margem) for cor_ref in cores_ref):
                pastas_correspondentes.append(pasta)
                break
    return pastas_correspondentes

def carregar_imagens(pasta):
    if not os.path.exists(pasta):
        print(f"A pasta {pasta} não existe.")
        return {}

    imagens = {}
    for root, _, files in os.walk(pasta):
        for nome_arquivo in files:
            if nome_arquivo.endswith(".png"):
                caminho = os.path.join(root, nome_arquivo)
                if not os.path.exists(caminho):
                    print(f"O arquivo {caminho} não existe.")
                    continue
                imagem = Image.open(caminho).convert('RGB')
                imagens[caminho] = imagem
    return imagens

def executar_comparacao(recorte_path):
    typemap_colors = carregar_cores('typemap.json')
    tiles_colors = carregar_cores('tiles.json')

    pontos_typemap = [(20, 20), (29, 20), (25, 30)]
    margem = 20
    
    cores_encontradas_typemap = verificar_cores(recorte_path, pontos_typemap)
    pasta_tipo_mapa = buscar_pastas_por_cores(cores_encontradas_typemap, typemap_colors, margem)
    
    if pasta_tipo_mapa:
        print(f"Tipo de mapa correspondente encontrado. Buscando na pasta: {pasta_tipo_mapa}")
        pasta_mapas = os.path.join('maps', pasta_tipo_mapa[0])
    else:
        print("Nenhum tipo de mapa específico encontrado. Buscando em todas as pastas.")
        pasta_mapas = 'maps'
    
    pontos_tiles = [(227, 165), (222, 178), (230, 174), (218, 170), (218, 190), (218, 185), (228, 160), (235, 178), (214, 168), (235, 170), (214, 174)]
    
    cores_encontradas_tiles = verificar_cores(recorte_path, pontos_tiles)
    pastas_tile = buscar_pastas_por_cores(cores_encontradas_tiles, tiles_colors, margem)
    
    imagens_referencia = {}
    if pastas_tile:
        print(f"Cores dos tiles correspondentes encontradas. Buscando nas pastas: {pastas_tile}")
        for pasta_tile in pastas_tile:
            caminho_pasta_tile = os.path.join(pasta_mapas, pasta_tile)
            if not os.path.exists(caminho_pasta_tile):
                print(f"A pasta do tile {caminho_pasta_tile} não existe.")
            else:
                imagens_referencia.update(carregar_imagens(caminho_pasta_tile))
    else:
        imagens_referencia = carregar_imagens(pasta_mapas)
    
    pontuacoes = comparar_imagens(recorte_path, imagens_referencia)
    
    if not pontuacoes:
        print("Nenhuma imagem correspondente encontrada na fase inicial.")
        return None

    melhor_imagem = max(pontuacoes, key=pontuacoes.get, default=None)
    
    if melhor_imagem:
        melhor_imagem_nome = os.path.basename(melhor_imagem).replace(".png", "")
        import pyperclip
        pyperclip.copy(melhor_imagem_nome)
        print(f"O nome da imagem '{melhor_imagem_nome}' foi copiado para a área de transferência.")
        return melhor_imagem_nome
    else:
        print("Nenhuma correspondência encontrada na fase final.")
        return None
