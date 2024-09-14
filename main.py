from capture import aguardar_e_capturar
from recorte import encontrar_e_recortar_imagem_referencia
from filter import executar_comparacao

def executar_comparacao_completa():
    captura_path = 'screenshot.png'
    referencia_path = 'basefull.png'

    # Passo 1: Captura de tela
    aguardar_e_capturar('ctrl+m', captura_path)

    # Passo 2: Recorte da imagem
    recorte_path = encontrar_e_recortar_imagem_referencia(captura_path, referencia_path)
    
    if recorte_path is None:
        print("Não foi possível encontrar a imagem de referência.")
        return

    # Passo 3: Identificação e comparação
    resultado_inicial = executar_comparacao(recorte_path)

    if resultado_inicial:
        print(f"Mapa econtrado: {resultado_inicial}")
    else:
        print("Nenhum resultado encontrado.")

if __name__ == "__main__":
    executar_comparacao_completa()
