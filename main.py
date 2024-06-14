import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PyQt5.QtGui import QColor

class RPGWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RPG Simples")
        self.setGeometry(100, 100, 300, 150)  # Diminuir pela metade a altura da janela

        self.map_size = 200  # Manter o número de linhas e colunas em 200
        self.current_row = 100
        self.current_col = 100

        self.map_data = {}  # Dicionário para armazenar as áreas visitadas

        cell_size = 2  # Definir o tamanho da célula (2.5x2.5 pixels)

        self.table_widget = QTableWidget(self.map_size, self.map_size, self)
        self.table_widget.setHorizontalHeaderLabels(['' for _ in range(self.map_size)])
        self.table_widget.setVerticalHeaderLabels(['' for _ in range(self.map_size)])
        self.table_widget.verticalHeader().setDefaultSectionSize(cell_size)
        self.table_widget.horizontalHeader().setDefaultSectionSize(cell_size)
        self.table_widget.setMinimumHeight(self.map_size * cell_size)
        self.table_widget.setMinimumWidth(self.map_size * cell_size)

        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.generate_map()

        # Iniciar a mensagem como vazia
        self.message = ""

    def generate_map(self):
        for i in range(self.map_size):
            for j in range(self.map_size):
                # Gera um número aleatório entre 1 e 10
                area_type = random.randint(1, 10)
                self.map_data[(i, j)] = area_type

        # Aglomeração dos valores próximos com 60% de chance de receberem o mesmo valor
        for i in range(self.map_size):
            for j in range(self.map_size):
                if random.random() < 0.6:
                    area_type = self.map_data[(i, j)]
                    for dx in range(-1, 2):
                        for dy in range(-1, 2):
                            new_i = i + dx
                            new_j = j + dy
                            if 0 <= new_i < self.map_size and 0 <= new_j < self.map_size:
                                # Define o valor da célula vizinha com a mesma probabilidade (60%)
                                if random.random() < 0.6:
                                    self.map_data[(new_i, new_j)] = area_type

        self.display_map()

    def display_map(self):
        start_row = max(0, self.current_row - 100)
        end_row = min(self.map_size, self.current_row + 101)

        start_col = max(0, self.current_col - 100)
        end_col = min(self.map_size, self.current_col + 101)

        color_palette = {
            1: QColor(0, 0, 255),      # Agua
            2: QColor(0, 0, 255),    # Agua
            3: QColor(128, 128, 128),      # mont
            4: QColor(0, 0, 255),      # Agua
            5: QColor(0, 0, 255),    # Agua
            6: QColor(0, 0, 255),    # Agua
            7: QColor(0, 100, 0),  # terra
            8: QColor(0, 100, 0),  # terra
            9: QColor(0, 100, 0),    # terra
            10: QColor(0, 100, 0)  # terra
        }

        for i in range(start_row, end_row):
            for j in range(start_col, end_col):
                area_type = self.map_data.get((i, j), 0)
                item = QTableWidgetItem(str(area_type))
                item.setBackground(color_palette.get(area_type, QColor(255, 255, 255)))  # Branco para valores não mapeados
                self.table_widget.setItem(i - start_row, j - start_col, item)

    def keyPressEvent(self, event):
        key = event.key()

        if key == 16777235:  # Setinha para cima
            self.move_character('up')

        elif key == 16777237:  # Setinha para direita
            self.move_character('right')

        elif key == 16777236:  # Setinha para baixo
            self.move_character('down')

        elif key == 16777234:  # Setinha para esquerda
            self.move_character('left')

        # Mostrar a mensagem quando o cursor estiver sobre a célula
        self.show_message()

        def move_character(self, direction):
            if direction == 'up':
                if self.current_row > 0:
                    self.current_row -= 1

            elif direction == 'right':
                if self.current_col < self.map_size - 1:
                    self.current_col += 1

            elif direction == 'down':
                if self.current_row < self.map_size - 1:
                    self.current_row += 1

            elif direction == 'left':
                if self.current_col > 0:
                    self.current_col -= 1

            self.display_map()

            # Chamar a função create_path para criar o caminho aleatório em vermelho
            self.create_path()

    def create_path(self):
        # Definir o número de focos em vermelho que serão criados
        num_focos = 300

        # Definir o tamanho máximo que cada foco pode ter (em células)
        max_tamanho_foco = 15

        # Definir a probabilidade de ocorrer um foco em cada célula (em percentual)
        probabilidade_foco = 5  # 5% de chance de ocorrer um foco em cada célula

        for _ in range(num_focos):
            # Escolher uma posição aleatória para começar um foco
            row = random.randint(0, self.map_size - 1)
            col = random.randint(0, self.map_size - 1)

            # Definir o tamanho do foco aleatoriamente (entre 1 e max_tamanho_foco)
            tamanho_foco = random.randint(1, max_tamanho_foco)

            # Definir a probabilidade de cada célula do foco ser vermelha (em percentual)
            probabilidade_vermelho = 80  # 80% de chance de cada célula do foco ser vermelha

            # Percorrer as células do foco e definir a cor como vermelha com a probabilidade definida
            for _ in range(tamanho_foco):
                # Verificar se a posição está dentro dos limites da tabela
                if 0 <= row < self.map_size and 0 <= col < self.map_size:
                    item = self.table_widget.item(row, col)
                    if random.randint(1, 100) <= probabilidade_vermelho:
                        item.setForeground(QColor(255, 0, 0))  # Cor vermelha (RGB: 255, 0, 0)
                # Mover para a próxima célula do foco
                dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
                row += dx
                col += dy


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RPGWindow()
    window.show()
    window.create_path()  # Chamar a função create_path ao exibir a janela
    sys.exit(app.exec_())

