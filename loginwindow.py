import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QComboBox, \
    QMessageBox
import sqlite3

from adminwindow import AdminWindow
from clientwindow import ClientWindow
from employeewindow import EmployeeWindow

class AuthWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Авторизация')

        # Создание виджетов для ввода логина и пароля
        self.label_login = QLabel('Логин:')
        self.input_login = QLineEdit()

        self.label_password = QLabel('Пароль:')
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)  # Скрытие вводимых символов

        # Создание выпадающего списка для выбора роли
        self.label_role = QLabel('Роль:')
        self.combo_role = QComboBox()
        self.combo_role.addItems(['Администратор', 'Клиент', 'Сотрудник'])

        # Кнопка для входа
        self.btn_login = QPushButton('Войти')
        self.btn_login.clicked.connect(self.login)  # Подключение метода для обработки нажатия кнопки

        # Размещение элементов на форме
        layout = QVBoxLayout()
        layout.addWidget(self.label_login)
        layout.addWidget(self.input_login)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(self.label_role)
        layout.addWidget(self.combo_role)
        layout.addWidget(self.btn_login)

        # Создание виджета для размещения компонентов
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Создание или подключение к базе данных
        self.conn = sqlite3.connect('legal_company.db')
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        # Создание таблицы пользователей, если она не существует
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')

        # Добавление пользователей
        users_list = [
            ('admin', 'admin123', 'Администратор'),
            ('client', 'client123', 'Клиент'),
            ('employee', 'employee123', 'Сотрудник')
        ]
        self.cur.executemany('''
            INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)
        ''', users_list)

        self.conn.commit()

    def login(self):
        login_text = self.input_login.text()
        password_text = self.input_password.text()
        role_text = self.combo_role.currentText()

        # Поиск пользователя в базе данных
        self.cur.execute('SELECT * FROM users WHERE username=? AND password=? AND role=?', (login_text, password_text, role_text))
        user = self.cur.fetchone()

        if user:
            QMessageBox.information(self, 'Успешная авторизация', f'Добро пожаловать, {user[3]} {user[1]}!')
            if role_text == 'Администратор' and login_text == 'admin' and password_text == 'admin123':
                self.admin_window = AdminWindow()
                self.admin_window.show()
            elif role_text == 'Сотрудник' and login_text == 'employee' and password_text == 'employee123':
                self.employee_window = EmployeeWindow()
                self.employee_window.show()
            elif role_text == 'Клиент':
                self.client_window = ClientWindow()
                self.client_window.show()
        else:
            QMessageBox.warning(self, 'Ошибка авторизации', 'Неправильный логин или пароль.')


    def open_client_window(self):
        user_window = ClientWindow()
        user_window.exec()

    def open_admin_window(self):
        admin_window = AdminWindow()
        admin_window.exec()

    def open_employee_window(self):
        admin_window = EmployeeWindow()
        admin_window.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AuthWindow()
    window.show()
    sys.exit(app.exec())
