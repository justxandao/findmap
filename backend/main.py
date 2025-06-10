import time
import os
from capture import capturar_tela_automaticamente
from recorte import encontrar_e_recortar_imagem_referencia
from filter import executar_comparacao

RESULTADOS_TXT = "resultados.txt"

# Função para capturar tela automaticamente
def executar_comparacao_completa():
    captura_path = 'screenshot.png'
    referencia_path = 'basefull.png'

    # Captura de tela
    capturar_tela_automaticamente(captura_path)

    # Verifica se o arquivo foi salvo corretamente
    if not os.path.exists(captura_path):
        print(f"[ERRO] Falha na captura: {captura_path} não existe.")
        return None

    # Recorte da imagem
    recorte_path = encontrar_e_recortar_imagem_referencia(captura_path, referencia_path)

    if not recorte_path or not os.path.exists(recorte_path):
        print("[ERRO] Falha ao recortar a imagem.")
        return None

    # Realiza a comparação da imagem
    resultado = executar_comparacao(recorte_path)

    if resultado:
        print(f"[✔] Mapa encontrado: {resultado}")
        return resultado
    else:
        print("[!] Nenhum resultado encontrado.")
        return None

# Função para carregar os resultados existentes
def carregar_resultados_existentes(path=RESULTADOS_TXT):
    resultados = set()
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            for linha in f:
                nome_imagem = linha.strip()  # Agora, o arquivo só vai armazenar o nome da imagem
                resultados.add(nome_imagem)
    return resultados

# Função para salvar apenas o nome da imagem
def salvar_resultado(nome_imagem, path=RESULTADOS_TXT):
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"{nome_imagem}\n")

# Função principal que executa tudo
def main():
    print("🔁 FindMap rodando em loop infinito (Ctrl+C para sair).")
    resultados_existentes = carregar_resultados_existentes()

    try:
        while True:
            resultado = executar_comparacao_completa()
            if resultado:
                # Verifica se o nome da imagem já está salvo
                if resultado not in resultados_existentes:
                    salvar_resultado(resultado)
                    resultados_existentes.add(resultado)
                    print(f"[✔] Resultado salvo: {resultado}")
                else:
                    print(f"[ℹ] Resultado já registrado: {resultado}")
            time.sleep(2)  # Tempo entre iterações
    except KeyboardInterrupt:
        print("\n[⛔] Execução encerrada pelo usuário.")

if __name__ == "__main__":
    main()
