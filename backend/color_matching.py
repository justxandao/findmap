import json

def carregar_cores(caminho_arquivo):
    """
    Carrega as cores de um arquivo JSON.
    
    Args:
        caminho_arquivo (str): Caminho para o arquivo JSON contendo as cores.
        
    Returns:
        dict: Dicionário com as cores carregadas.
    """
    with open(caminho_arquivo, 'r') as arquivo:
        cores = json.load(arquivo)
    return cores

def buscar_pastas_por_cores(cores_encontradas, cores_referencia, margem):
    """
    Busca pastas que correspondem às cores encontradas com base em uma margem de erro.
    
    Args:
        cores_encontradas (dict): Dicionário de cores encontradas.
        cores_referencia (dict): Dicionário de cores de referência.
        margem (int): Margem de erro para correspondência de cores.
        
    Returns:
        list: Lista de pastas correspondentes.
    """
    pastas_correspondentes = []
    for ponto, cor in cores_encontradas.items():
        if cor is None:
            continue
        for cor_referencia in cores_referencia:
            if verificar_cor(cor, cor_referencia, margem):
                pasta = cores_referencia[cor_referencia]
                if pasta not in pastas_correspondentes:
                    pastas_correspondentes.append(pasta)
    return pastas_correspondentes

def verificar_cor(cor1, cor2, margem):
    """
    Verifica se duas cores são semelhantes dentro de uma margem de erro.
    
    Args:
        cor1 (tuple): Cor 1 (R, G, B).
        cor2 (tuple): Cor 2 (R, G, B).
        margem (int): Margem de erro.
        
    Returns:
        bool: True se as cores são semelhantes, False caso contrário.
    """
    return all(abs(c1 - c2) <= margem for c1, c2 in zip(cor1, cor2))
