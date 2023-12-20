import sqlite3
import sys

from PyQt6.QtWidgets import QTableWidgetItem, QHBoxLayout, QTableWidget, QDialog, QVBoxLayout, QPushButton, QComboBox, \
    QLabel, QApplication


class EmployeeWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Окно сотрудника')

        self.conn = sqlite3.connect('legal_company.db')
        self.cur = self.conn.cursor()

        self.cur.execute('''
                   CREATE TABLE IF NOT EXISTS employee (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   firstname TEXT NOT NULL,
                   lastname TEXT NOT NULL,
                   post TEXT,
                   phone TEXT
                   )
               ''')

        # Элементы управления
        self.label_service_type = QLabel('Выберите услугу:')
        self.combo_service_type = QComboBox()
        self.combo_service_type.addItems(['Юридическое консультирование', 'Представительство в суде'])

        self.btn_show_applications = QPushButton('Показать заявки')
        self.btn_show_applications.clicked.connect(self.show_applications)

        # Размещение элементов на форме
        layout = QVBoxLayout()
        layout.addWidget(self.label_service_type)
        layout.addWidget(self.combo_service_type)
        layout.addWidget(self.btn_show_applications)

        self.setLayout(layout)

        # Создание или подключение к базе данных
        self.conn = sqlite3.connect('legal_company.db')
        self.cur = self.conn.cursor()

    def show_applications(self):
        service_type = self.combo_service_type.currentText()

        # Получение заявок по выбранной услуге
        self.cur.execute('''
            SELECT application.id, application.name, application.description, application.date 
            FROM application 
            JOIN client ON client.application_id = application.id 
            WHERE client.service_type = ? 
        ''', (service_type,))

        applications = self.cur.fetchall()

        # Создание и отображение окна с заявками для выбранной услуги
        self.applications_window = QDialog()
        self.applications_window.setWindowTitle(f'Заявки на услугу: {service_type}')

        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(['ID', 'Название', 'Описание', 'Дата'])

        for row, application in enumerate(applications):
            table.insertRow(row)
            for col, data in enumerate(application):
                table.setItem(row, col, QTableWidgetItem(str(data)))

        layout = QHBoxLayout()
        layout.addWidget(table)
        self.applications_window.setLayout(layout)

        self.applications_window.exec()

def run():
    app = QApplication(sys.argv)
    window = EmployeeWindow()
    window.exec()
    sys.exit(app.exec())

if __name__ == '__main__':
    run()