import sqlite3
import sys

from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, \
    QApplication


class AdminWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Окно администратора')

        # Элементы управления
        self.btn_show_all_applications = QPushButton('Показать все заявки')
        self.btn_show_all_applications.clicked.connect(self.show_all_applications)

        # Размещение элементов на форме
        layout = QVBoxLayout()
        layout.addWidget(self.btn_show_all_applications)

        self.setLayout(layout)

        # Создание или подключение к базе данных
        self.conn = sqlite3.connect('legal_company.db')
        self.cur = self.conn.cursor()

    def show_all_applications(self):
        # Получение всех заявок из базы данных
        self.cur.execute('''
            SELECT application.id, application.name, application.description, application.date, client.email, client.phone 
            FROM application
            JOIN client ON client.application_id = application.id
        ''')

        applications = self.cur.fetchall()

        # Создание и отображение окна со всеми заявками
        self.applications_window = QDialog()
        self.applications_window.setWindowTitle('Все заявки')

        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(['ID', 'Название', 'Описание', 'Дата', 'Email', 'Телефон'])

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
    window = AdminWindow()
    window.exec()
    sys.exit(app.exec())

if __name__ == '__main__':
    run()