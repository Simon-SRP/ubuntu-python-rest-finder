from PyQt6.QtWidgets import (QApplication, QMainWindow, QListWidget,
                             QVBoxLayout, QWidget, QPushButton, QLabel)
from PyQt6.QtCore import Qt
from .models import get_rest_places
import webbrowser


class RestFinderApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.main_window = MainWindow()

    def run(self):
        self.main_window.show()
        return self.exec()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ubuntu Rest Finder")
        self.setGeometry(100, 100, 800, 600)

        self.places = get_rest_places()
        self.init_ui()

    def init_ui(self):
        # Основной виджет и layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Заголовок
        title = QLabel("Выберите место для отдыха:")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        # Список мест
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("font-size: 14px;")
        for place in self.places:
            self.list_widget.addItem(f"{place['name']} - {place['location']}")
        layout.addWidget(self.list_widget)

        # Кнопка для открытия ссылки
        self.open_btn = QPushButton("Открыть страницу бронирования")
        self.open_btn.setStyleSheet("font-size: 14px; padding: 8px;")
        self.open_btn.clicked.connect(self.open_booking_page)
        layout.addWidget(self.open_btn)

        # Описание выбранного места
        self.description_label = QLabel("")
        self.description_label.setWordWrap(True)
        self.description_label.setStyleSheet("font-size: 14px; padding: 10px;")
        layout.addWidget(self.description_label)

        # Обновляем описание при выборе элемента
        self.list_widget.currentRowChanged.connect(self.update_description)

    def update_description(self, index):
        if 0 <= index < len(self.places):
            self.description_label.setText(self.places[index]['description'])

    def open_booking_page(self):
        current_row = self.list_widget.currentRow()
        if current_row >= 0 and current_row < len(self.places):
            webbrowser.open(self.places[current_row]['link'])