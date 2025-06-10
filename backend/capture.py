# capture.py
import pyautogui

class CapturaDeTela:
    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo

    def captura_tela(self):
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(self.caminho_arquivo)
            print(f"Captura de tela salva em {self.caminho_arquivo}")
        except Exception as e:
            print(f"Erro ao capturar a tela: {e}")

# Função para capturar a tela automaticamente sem esperar por atalho
def capturar_tela_automaticamente(caminho_arquivo):
    captura = CapturaDeTela(caminho_arquivo)
    captura.captura_tela()
