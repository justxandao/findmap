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

def aguardar_e_capturar(atalho, caminho_arquivo):
    import keyboard
    print(f"Pressione {atalho} para capturar a tela...")
    keyboard.wait(atalho)  # Aguarda o atalho ser pressionado
    captura = CapturaDeTela(caminho_arquivo)
    captura.captura_tela()
