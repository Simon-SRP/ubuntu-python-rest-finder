from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QListWidget,
    QVBoxLayout, QWidget, QPushButton, QLabel, QScrollArea,
    QLineEdit, QHBoxLayout, QMessageBox, QStackedWidget
)
from PyQt6.QtCore import Qt
from .models import get_hotels


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
        self.setWindowTitle("Hotel Finder")
        self.setGeometry(100, 100, 800, 800)
        self.hotels = []

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        self.init_main_menu()
        self.init_hotels_view()

        self.stacked_widget.setCurrentIndex(0)

    def init_main_menu(self):
        self.main_menu_widget = QWidget()
        layout = QVBoxLayout(self.main_menu_widget)

        self.count_input = QLineEdit()
        self.count_input.setPlaceholderText("Введите количество отелей (по умолчанию 50)")
        self.count_input.setStyleSheet("font-size: 16px; padding: 10px;")

        self.load_btn = QPushButton("Показать отели")
        self.load_btn.setStyleSheet("font-size: 16px; padding: 10px;")
        self.load_btn.clicked.connect(self.load_hotels)

        layout.addWidget(QLabel("Hotel Finder"))
        layout.addWidget(self.count_input)
        layout.addWidget(self.load_btn)
        layout.addStretch()

        self.stacked_widget.addWidget(self.main_menu_widget)

    def init_hotels_view(self):
        self.hotels_widget = QWidget()
        layout = QVBoxLayout(self.hotels_widget)

        self.back_btn = QPushButton("Назад")
        self.back_btn.setStyleSheet("font-size: 16px; padding: 10px;")
        self.back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("font-size: 14px;")

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.list_widget)

        layout.addWidget(self.back_btn)
        layout.addWidget(scroll)

        self.stacked_widget.addWidget(self.hotels_widget)

    def load_hotels(self):
        try:
            count_text = self.count_input.text()
            count = int(count_text) if count_text else 50

            if count <= 0:
                QMessageBox.warning(self, "Ошибка", "Количество отелей должно быть положительным числом")
                return

        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите корректное число")
            return

        self.load_btn.setEnabled(False)
        self.load_btn.setText("Загрузка...")
        QApplication.processEvents()
        self.hotels = get_hotels(count=count)
        self.list_widget.clear()

        for i, hotel in enumerate(self.hotels, start=1):
            self.list_widget.addItem(
                f"{i}. {hotel['name']}\n"
                f"Адрес: {hotel['address']}\n"
                f"Рейтинг: {hotel['rating']} | Расстояние: {hotel['distance']}\n"
                f"{'-' * 50}"
            )

        # Переключаемся на экран с отелями
        self.stacked_widget.setCurrentIndex(1)
        self.load_btn.setText("Показать отели")
        self.load_btn.setEnabled(True)