import sys
import csv
import sqlite3
from PyQt5.QtWidgets import QInputDialog, QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QListWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class StockControlApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.initDatabase()

    def initUI(self):
        self.setWindowTitle("Sistema de Controle de Estoque")
        self.setGeometry(100, 100, 600, 400)

        # Defina a cor de fundo do widget principal (QWidget) usando folhas de estilo
        self.central_widget = QWidget(self)
        self.central_widget.setStyleSheet("background-color: lightblue;")
        self.setCentralWidget(self.central_widget)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        logo_pixmap = QPixmap("logotwo.png")
        logo_pixmap = logo_pixmap.scaled(500, 500, aspectRatioMode=Qt.KeepAspectRatio)

        # Adicione o logotipo da empresa
        logo_label = QLabel(self)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(logo_label)

        self.item_input = QLineEdit(self)
        self.quantity_input = QLineEdit(self)

        self.add_button = QPushButton("Adicionar Item", self)
        self.add_button.clicked.connect(self.addItem)

        self.update_button = QPushButton("Atualizar Item", self)
        self.update_button.clicked.connect(self.updateItem)

        self.delete_button = QPushButton("Excluir Item", self)
        self.delete_button.clicked.connect(self.deleteItem)

        self.report_button = QPushButton("Gerar Relatório", self)
        self.report_button.clicked.connect(self.generateStockReport)

        self.item_list = QListWidget(self)

        self.layout.addWidget(QLabel("Item:"))
        self.layout.addWidget(self.item_input)
        self.layout.addWidget(QLabel("Quantidade:"))
        self.layout.addWidget(self.quantity_input)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.update_button)
        self.layout.addWidget(self.delete_button)
        self.layout.addWidget(self.report_button)
        self.layout.addWidget(self.item_list)

        self.central_widget.setLayout(self.layout)

    def initDatabase(self):
        self.conn = sqlite3.connect("stock.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS stock (
            id INTEGER PRIMARY KEY,
            item TEXT,
            quantity INTEGER
        )''')

        self.conn.commit()

        self.loadItems()

    def addItem(self):
        item = self.item_input.text()
        quantity = self.quantity_input.text()

        if item and quantity:
            self.cursor.execute("INSERT INTO stock (item, quantity) VALUES (?, ?)", (item, quantity))
            self.conn.commit()
            self.item_input.clear()
            self.quantity_input.clear()
            self.loadItems()

    def loadItems(self):
        self.item_list.clear()
        self.cursor.execute("SELECT * FROM stock")
        items = self.cursor.fetchall()
        for item in items:
            self.item_list.addItem(f"{item[1]} - {item[2]} unidades")

    def updateItem(self):
        selected_item = self.item_list.currentItem()
        if selected_item:
            new_quantity, ok = QInputDialog.getInt(self, "Atualizar Quantidade", "Nova Quantidade:")
            if ok:
                item_name = selected_item.text().split('-')[0].strip()
                self.cursor.execute("UPDATE stock SET quantity = ? WHERE item = ?", (new_quantity, item_name))
                self.conn.commit()
                self.loadItems()

    def deleteItem(self):
        selected_item = self.item_list.currentItem()
        if selected_item:
            item_name = selected_item.text().split('-')[0].strip()
            self.cursor.execute("DELETE FROM stock WHERE item = ?", (item_name,))
            self.conn.commit()
            self.loadItems()

    def generateStockReport(self):
        self.cursor.execute("SELECT * FROM stock")
        items = self.cursor.fetchall()
        with open("Relatorio Estoque.csv", "w", newline="", encoding="utf-8") as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(["Item", "Quantidade"])
            for item in items:
                csvwriter.writerow([item[1], item[2]])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StockControlApp()
    window.show()
    sys.exit(app.exec_())
