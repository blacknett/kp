import sys
from PyQt6.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QDialog, \
    QComboBox, QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout
import sqlite3

class ClientWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Окно клиента')

        # Создаем элементы управления для ввода данных о заявке
        self.label_name = QLabel('Имя:')
        self.input_name = QLineEdit()

        self.label_email = QLabel('Email:')
        self.input_email = QLineEdit()

        self.label_phone = QLabel('Телефон:')
        self.input_phone = QLineEdit()

        self.label_description = QLabel('Описание проблемы:')
        self.input_description = QLineEdit()

        self.label_service_type = QLabel('Выберите услугу:')
        self.combo_service_type = QComboBox()
        self.combo_service_type.addItems(['Юридическое консультирование', 'Представительство в суде', 'Другое'])

        self.btn_submit_application = QPushButton('Создать заявку')
        self.btn_submit_application.clicked.connect(self.submit_application)

        self.btn_show_applications = QPushButton('Показать мои заявки')
        self.btn_show_applications.clicked.connect(self.show_applications)

        # Размещение элементов на форме
        layout = QVBoxLayout()
        layout.addWidget(self.label_name)
        layout.addWidget(self.input_name)
        layout.addWidget(self.label_email)
        layout.addWidget(self.input_email)
        layout.addWidget(self.label_phone)
        layout.addWidget(self.input_phone)
        layout.addWidget(self.label_description)
        layout.addWidget(self.input_description)
        layout.addWidget(self.label_service_type)
        layout.addWidget(self.combo_service_type)
        layout.addWidget(self.btn_submit_application)
        layout.addWidget(self.btn_show_applications)

        self.setLayout(layout)

        # Создание или подключение к базе данных
        self.conn = sqlite3.connect('legal_company.db')
        self.cur = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Создание таблицы клиентов, если она не существует
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS client (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                service_type TEXT,
                application_id INTEGER,
                FOREIGN KEY(application_id) REFERENCES application(id)
            )
        ''')

        # Создание таблицы заявок, если она не существует
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS application (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                date TEXT
            )
        ''')

        self.conn.commit()

    def submit_application(self):
        name = self.input_name.text()
        email = self.input_email.text()
        phone = self.input_phone.text()
        description = self.input_description.text()
        service_type = self.combo_service_type.currentText()

        # Проверка заполнения всех полей
        if not all([name, email, phone, description]):
            QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, заполните все поля.')
            return

        # Вставка данных заявки в базу данных
        self.cur.execute('INSERT INTO application (name, description, date) VALUES (?, ?, DATETIME("now"))',
                         (name, description))
        application_id = self.cur.lastrowid  # Получаем ID последней добавленной записи

        # Вставка данных клиента в базу данных
        self.cur.execute('INSERT INTO client (name, email, phone, service_type, application_id) VALUES (?, ?, ?, ?, ?)',
                         (name, email, phone, service_type, application_id))

        self.conn.commit()
        QMessageBox.information(self, 'Успешно', 'Заявка успешно создана!')

    def show_applications(self):
        # Получение всех заявок данного пользователя из базы данных
        self.cur.execute(
            'SELECT application.id, application.name, application.description, application.date FROM application JOIN client ON client.application_id = application.id WHERE client.name = ?',
            (self.input_name.text(),))
        applications = self.cur.fetchall()

        # Создание и отображение окна с заявками пользователя
        self.applications_window = QDialog()
        self.applications_window.setWindowTitle('Мои заявки')

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
    window = ClientWindow()
    window.exec()
    sys.exit(app.exec())

if __name__ == '__main__':
    run()
