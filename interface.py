from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QLineEdit
from PyQt5.QtGui import QPixmap
import sys
import subprocess
import pyperclip

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('FindMap Interface')
        self.setGeometry(100, 100, 800, 600)

        # Criar widgets
        self.image_label = QLabel(self)
        self.coord_input = QLineEdit(self)
        self.coord_input.setReadOnly(True)
        self.copy_button = QPushButton('Copiar', self)
        self.activate_button = QPushButton('Ativar', self)
        self.create_list_button = QPushButton('Criar Lista', self)

        # Configurar layout
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.coord_input)
        layout.addWidget(self.copy_button)
        layout.addWidget(self.activate_button)
        layout.addWidget(self.create_list_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Conectar botões
        self.activate_button.clicked.connect(self.start_main_script)
        self.create_list_button.clicked.connect(self.create_list_script)
        self.copy_button.clicked.connect(self.copy_to_clipboard)

        # Inicializar variáveis
        self.resultado_inicial = ""

    def start_main_script(self):
        # Executar o main.py e atualizar a interface
        process = subprocess.Popen(['python', 'main.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if stderr:
            print(f"Erro ao executar main.py: {stderr.decode()}")
        else:
            self.resultado_inicial = stdout.decode().strip()  # Definindo resultado_inicial com a saída do main.py
            # Atualizar a imagem e coordenadas
            self.image_label.setPixmap(QPixmap('example_image.png'))  # Atualizar com a imagem correta
            self.coord_input.setText(self.resultado_inicial)  # Exibir as coordenadas da imagem carregada

    def create_list_script(self):
        # Executar o script de criação de lista
        subprocess.Popen(['python', 'criar_lista.py'])

    def copy_to_clipboard(self):
        # Copiar texto para a área de transferência
        pyperclip.copy(self.coord_input.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
