from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QListWidget, QComboBox,
    QVBoxLayout, QWidget, QPushButton, QLabel, QScrollArea,
    QLineEdit, QHBoxLayout, QMessageBox, QStackedWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon
from .models import get_hotels
from .parser import get_available_cities
import requests
from io import BytesIO


class HotelItemWidget(QWidget):
    def __init__(self, hotel, index):
        super().__init__()
        self.hotel = hotel
        self.index = index
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Заголовок с номером и названием
        title_layout = QHBoxLayout()
        title_label = QLabel(f"{self.index}. {self.hotel['name']}")
        title_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        title_layout.addWidget(title_label)

        # Рейтинг
        rating_label = QLabel(f"★ {self.hotel['rating']}")
        rating_label.setStyleSheet("color: #FFA500; font-weight: bold; font-size: 14px;")
        title_layout.addWidget(rating_label)
        layout.addLayout(title_layout)

        # Адрес и расстояние
        address_label = QLabel(f"📍 {self.hotel['address']}")
        address_label.setStyleSheet("font-size: 14px; color: #555;")
        layout.addWidget(address_label)

        distance_label = QLabel(f"🚶 {self.hotel['distance']}")
        distance_label.setStyleSheet("font-size: 14px; color: #555;")
        layout.addWidget(distance_label)

        # Описание
        description_label = QLabel(self.hotel['description'])
        description_label.setWordWrap(True)
        description_label.setStyleSheet("font-size: 13px; margin-top: 5px;")
        layout.addWidget(description_label)

        # Изображение (если есть)
        if self.hotel['image_url']:
            try:
                response = requests.get(self.hotel['image_url'])
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)

                if not pixmap.isNull():
                    image_label = QLabel()
                    pixmap = pixmap.scaled(300, 200, Qt.AspectRatioMode.KeepAspectRatio)
                    image_label.setPixmap(pixmap)
                    layout.addWidget(image_label)
            except:
                pass

        # Ссылка на отель
        if self.hotel['hotel_url']:
            link_label = QLabel(f'<a href="{self.hotel["hotel_url"]}">Ссылка на Booking.com</a>')
            link_label.setOpenExternalLinks(True)
            link_label.setStyleSheet("font-size: 13px; color: #0066cc;")
            layout.addWidget(link_label)

        # Разделитель
        separator = QLabel()
        separator.setStyleSheet("border-bottom: 1px solid #ddd; margin-top: 10px; margin-bottom: 10px;")
        layout.addWidget(separator)


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
        self.setGeometry(100, 100, 900, 800)
        self.hotels = []

        self.sort_by_rating = False
        self.sort_by_distance = False

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

        self.city_combo = QComboBox()
        self.city_combo.setStyleSheet("font-size: 16px; padding: 10px;")

        # Получаем и выводим список доступных городов (для отладки)
        available_cities = get_available_cities()
        print("Найдены города в папке city:", available_cities)  # Отладочный вывод

        if not available_cities:
            QMessageBox.warning(self, "Ошибка", "Не найдены данные о городах. Добавьте JSON-файлы в папку 'city'")
        else:
            for city in available_cities:
                self.city_combo.addItem(city)
                print("Добавлен город в комбобокс:", city)  # Отладочный вывод

        self.load_btn = QPushButton("Показать отели")
        self.load_btn.setStyleSheet("font-size: 16px; padding: 10px;")
        self.load_btn.clicked.connect(self.load_hotels)

        layout.addWidget(QLabel("Hotel Finder"))
        layout.addWidget(QLabel("Выберите город:"))
        layout.addWidget(self.city_combo)
        layout.addWidget(self.load_btn)
        layout.addStretch()

        self.stacked_widget.addWidget(self.main_menu_widget)

    def init_hotels_view(self):
        self.hotels_widget = QWidget()
        layout = QVBoxLayout(self.hotels_widget)

        # Верхняя панель с кнопками
        top_panel = QHBoxLayout()

        self.back_btn = QPushButton("Назад")
        self.back_btn.setStyleSheet("font-size: 16px; padding: 10px;")
        self.back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        self.sort_rating_btn = QPushButton("Сортировать по рейтингу")
        self.sort_rating_btn.setStyleSheet("font-size: 16px; padding: 10px;")
        self.sort_rating_btn.setCheckable(True)
        self.sort_rating_btn.clicked.connect(self.toggle_sort_by_rating)

        self.sort_distance_btn = QPushButton("Сортировать по расстоянию")
        self.sort_distance_btn.setStyleSheet("font-size: 16px; padding: 10px;")
        self.sort_distance_btn.setCheckable(True)
        self.sort_distance_btn.clicked.connect(self.toggle_sort_by_distance)

        top_panel.addWidget(self.back_btn)
        top_panel.addWidget(self.sort_rating_btn)
        top_panel.addWidget(self.sort_distance_btn)
        top_panel.addStretch()

        layout.addLayout(top_panel)

        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("font-size: 14px;")
        self.list_widget.setSpacing(10)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.list_widget)

        layout.addWidget(self.back_btn)
        layout.addWidget(scroll)

        self.stacked_widget.addWidget(self.hotels_widget)

    def parse_rating(self, rating_str):
        """Извлекает числовое значение рейтинга из строки"""
        if not rating_str or rating_str == 'N/A':
            return 0.0
        try:
            # Удаляем все нечисловые символы, кроме точки
            cleaned = ''.join(c for c in rating_str if c.isdigit() or c == '.')
            return float(cleaned)
        except:
            return 0.0

    def parse_distance(self, distance_str):
        """Извлекает числовое значение расстояния в метрах из строки"""
        if not distance_str or distance_str == 'N/A':
            return float('inf')
        try:
            # Удаляем все нечисловые символы, кроме точки и запятой
            cleaned = ''.join(c for c in distance_str if c.isdigit() or c in {'.', ','})
            # Заменяем запятую на точку
            value = float(cleaned.replace(',', '.'))
            # Если в строке есть 'км' или 'km', считаем это километрами
            if 'км' in distance_str.lower() or 'km' in distance_str.lower():
                return value * 1000  # Конвертируем километры в метры
            return value  # Уже метры
        except:
            return float('inf')

    def toggle_sort_by_rating(self):
        """Переключает сортировку по рейтингу"""
        self.sort_by_rating = not self.sort_by_rating
        self.sort_rating_btn.setChecked(self.sort_by_rating)
        if self.sort_by_rating:
            self.sort_by_distance = False
            self.sort_distance_btn.setChecked(False)
        self.update_hotels_display()

    def toggle_sort_by_distance(self):
        """Переключает сортировку по расстоянию"""
        self.sort_by_distance = not self.sort_by_distance
        self.sort_distance_btn.setChecked(self.sort_by_distance)
        if self.sort_by_distance:
            self.sort_by_rating = False
            self.sort_rating_btn.setChecked(False)
        self.update_hotels_display()

    def update_hotels_display(self):
        """Обновляет отображение отелей с учетом сортировки"""
        if not self.hotels:
            return

        try:
            sorted_hotels = self.hotels.copy()

            if self.sort_by_rating:
                sorted_hotels.sort(key=lambda x: (
                    x.get('rating') == 'N/A',  # N/A будут в конце
                    -self.parse_rating(x.get('rating', 'N/A'))  # Сортировка по убыванию
                ))
            elif self.sort_by_distance:
                sorted_hotels.sort(key=lambda x: (
                    x.get('distance') == 'N/A',  # N/A будут в конце
                    self.parse_distance(x.get('distance', 'N/A'))  # Сортировка по возрастанию
                ))

            self.list_widget.clear()
            for i, hotel in enumerate(sorted_hotels, start=1):
                try:
                    item = QListWidgetItem()
                    item.setSizeHint(QSize(800, 300))
                    widget = HotelItemWidget(hotel, i)
                    self.list_widget.addItem(item)
                    self.list_widget.setItemWidget(item, widget)
                except Exception as e:
                    print(f"Ошибка при отображении отеля {i}: {e}")

        except Exception as e:
            print(f"Ошибка при сортировке: {e}")
            QMessageBox.warning(self, "Ошибка", f"Не удалось выполнить сортировку: {str(e)}")

    def load_hotels(self):
        try:
            selected_city = self.city_combo.currentText()
            if not selected_city:
                return

            self.load_btn.setEnabled(False)
            self.load_btn.setText("Загрузка...")
            QApplication.processEvents()

            # Сбрасываем сортировку
            self.sort_by_rating = False
            self.sort_by_distance = False
            self.sort_rating_btn.setChecked(False)
            self.sort_distance_btn.setChecked(False)

            self.hotels = get_hotels(selected_city)
            if not self.hotels:
                QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить отели для {selected_city}")

            self.update_hotels_display()

        except Exception as e:
            print(f"Ошибка при загрузке отелей: {e}")
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {str(e)}")

        finally:
            self.load_btn.setText("Показать отели")
            self.load_btn.setEnabled(True)
            self.stacked_widget.setCurrentIndex(1)