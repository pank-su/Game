# -*- coding: utf-8 -*-

import json
import socket
import sys

import requests
from PyQt5 import QtGui, QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import (QCoreApplication, QMetaObject,
                          QSize, Qt)
from PyQt5.QtGui import (QFont)
from PyQt5.QtWidgets import *

reg_mail = ''
reg_login = ''
reg_password = ''


keyboard_en = [
    'qwertyuiop',
    'asdfghjkl',
    'zxcvbnm'
]
keyboard_ru = [
    'йцукенгшщзхъ',
    'фывапролджэё',
    'ячсмитьбю'
]
playing = False


class PasswordError(Exception):
    pass


class LengthError(PasswordError):
    pass


class LetterError(PasswordError):
    pass


class DigitError(PasswordError):
    pass


class SequenceError(PasswordError):
    pass


def check_password(password: str):
    if len(password) > 8 and lower(password) and upper(password) and num(password) and three_letters(
            password):
        return 'ok'
    elif not len(password) > 8:
        raise LengthError


def lower(string: str):
    for el in string:
        if el.islower():
            return True
    raise LetterError


def num(string: str):
    for el in string:
        if el.isnumeric():
            return True
    raise DigitError


def upper(string: str):
    for el in string:
        if el.isupper():
            return True
    raise LetterError


def three_letters(string: str):
    for i in range(3):
        for g in range(len(keyboard_en[i])):
            some_letters = keyboard_en[i][g: g + 3]
            if len(some_letters) == 3:
                if some_letters in string.lower():
                    raise SequenceError
            else:
                break
        for g in range(len(keyboard_ru[i])):
            some_letters = keyboard_ru[i][g: g + 3]
            if len(some_letters) == 3:
                if some_letters in string.lower():
                    raise SequenceError
            else:
                break
    return True


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(415, 142)
        Form.setMinimumSize(QSize(415, 140))
        Form.setStyleSheet(u"QWidget{\n"
                           "	font: 57 10pt \"PerfectDOSVGA437\";\n"
                           "}")
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.label)

        self.lineEdit = QLineEdit(Form)
        self.lineEdit.setObjectName(u"lineEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy1)
        self.lineEdit.setEchoMode(QLineEdit.Normal)

        self.horizontalLayout.addWidget(self.lineEdit)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.lineEdit_2 = QLineEdit(Form)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        sizePolicy1.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy1)
        self.lineEdit_2.setEchoMode(QLineEdit.Password)

        self.horizontalLayout_2.addWidget(self.lineEdit_2)

        self.horizontalSpacer_2 = QSpacerItem(32, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.pushButton_2 = QPushButton(Form)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_3.addWidget(self.pushButton_2)

        self.pushButton = QPushButton(Form)
        self.pushButton.setObjectName(u"pushButton")
        font = QFont()
        font.setFamily(u"PerfectDOSVGA437")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(7)
        self.pushButton.setFont(font)
        self.pushButton.setAutoFillBackground(False)
        self.pushButton.setAutoDefault(False)
        self.pushButton.setFlat(False)

        self.horizontalLayout_3.addWidget(self.pushButton)

        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Form)

        self.pushButton.setDefault(False)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Login or email", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Password", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form",
                                                             u"\u0417\u0430\u0440\u0435\u0433\u0435\u0441\u0442\u0440\u0438\u0440\u043e\u0432\u0430\u0442\u044c\u0441\u044f",
                                                             None))
        self.pushButton.setText(
            QCoreApplication.translate("Form", u"\u0412\u043e\u0439\u0442\u0438", None))
    # retranslateUi


class Ui_Form_2(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(244, 259)
        Form.setStyleSheet(u"QWidget{\n"
                           "	font: 57 10pt \"PerfectDOSVGA437\";\n"
                           "}")
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.lineEdit = QLineEdit(Form)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.lineEdit_2 = QLineEdit(Form)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.horizontalLayout_2.addWidget(self.lineEdit_2)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.lineEdit_3 = QLineEdit(Form)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setEchoMode(QLineEdit.Password)

        self.horizontalLayout_3.addWidget(self.lineEdit_3)

        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.lineEdit_4 = QLineEdit(Form)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setEchoMode(QLineEdit.Password)

        self.horizontalLayout_4.addWidget(self.lineEdit_4)

        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.pushButton = QPushButton(Form)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Email", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Login", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Password", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Password", None))
        self.pushButton.setText(QCoreApplication.translate("Form",
                                                           u"\u041e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u044c \u0447\u0438\u0441\u043b\u0430 \u043d\u0430 \u043f\u043e\u0447\u0442\u0443",
                                                           None))
    # retranslateUi


class Ui_Form_3(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(293, 94)
        Form.setStyleSheet(u"QWidget{\n"
                           "	font: 57 10pt \"PerfectDOSVGA437\";\n"
                           "}")
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.lineEdit = QLineEdit(Form)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton_2 = QPushButton(Form)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_2.addWidget(self.pushButton_2)

        self.pushButton = QPushButton(Form)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_2.addWidget(self.pushButton)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Numbers on your email", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form",
                                                             u"\u041e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u044c \u0441\u043d\u043e\u0432\u0430",
                                                             None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"\u041e\u041a", None))


# Don't work
class Ui_Form_4(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(427, 323)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setScaledContents(True)

        self.verticalLayout.addWidget(self.label)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_2)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText("")
        self.label_2.setText(QCoreApplication.translate("Form",
                                                        u"\u041f\u0440\u043e\u0432\u0435\u0440\u044f\u0435\u043c \u043f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u0435 \u043a \u0441\u0435\u0440\u0432\u0435\u0440\u0430\u043c. \u041f\u043e\u0434\u043e\u0436\u0434\u0438\u0442\u0435...",
                                                        None))


window = ''


def open_window(obj, x, y, w, h):
    global window
    window = obj()
    window.show()
    window.setGeometry(x, y + 20, w, h)


# Don't work
class Test_conection_window(QMainWindow, Ui_Form_4):
    x_ = 1

    def __init__(self):
        super().__init__()
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.setupUi(self.central_widget)
        self.movie = QtGui.QMovie('images/loading_2.gif')
        self.movie.start()
        self.label.setMovie(self.movie)
        self.timer = QtCore.QTimer(self)

        self.timer.timeout.connect(self.check)
        self.timer.start(2000)
        self.timer_2 = QtCore.QTimer(self)
        self.timer_2.timeout.connect(self.change_text)
        self.timer_2.start(500)

    def change_text(self):
        self.label_2.setText('Проверяем подключение к серверам. Подождите' + '.' * self.x_)
        if self.x_ == 3:
            self.x_ = 0
        self.x_ += 1

    def check(self):
        self.timer.stop()
        try:
            requests.get('http://2f9f839aebbd.ngrok.io/')
        except Exception:
            self.close()
        open_window(First_window, self.x(), self.y(), self.width(), self.height())
        self.close()


class First_window(QMainWindow, Ui_Form):
    error_dialog = ''

    def __init__(self):
        super().__init__()
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.setupUi(self.central_widget)
        self.pushButton_2.pressed.connect(self.open_reg)
        self.pushButton.pressed.connect(self.login)

    def login(self):
        if requests.post('http://2f9f839aebbd.ngrok.io/login',
                         json.dumps(
                             {'version': 1.0, 'ip': socket.gethostbyname(socket.gethostname()),
                              'fast_login': '', 'login': self.lineEdit.text(),
                              'password': self.lineEdit_2.text()})).text == 'true\n':
            global playing
            playing = True
            self.close()
        else:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.showMessage('Неверный логин или пароль.')

    def open_reg(self):
        open_window(Reg_window, self.x(), self.y(), self.width(), self.height())

        self.close()


class Reg_window(QMainWindow, Ui_Form_2):

    def __init__(self):
        super().__init__()
        self.error_dialog = QtWidgets.QErrorMessage()
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.setupUi(self.central_widget)
        self.pushButton.pressed.connect(self.send_numbers)

    def send_numbers(self):
        if '@' not in self.lineEdit.text():
            self.error_dialog.showMessage('Введённая почта не является почтой')
            return
        if self.lineEdit_2.text().split() == []:
            self.error_dialog.showMessage('Логин не должен быть пустым.')
            return
        if requests.post('http://2f9f839aebbd.ngrok.io/register',
                         json.dumps(
                             {'version': 1.0, 'ip': socket.gethostbyname(socket.gethostname()),
                              'event': 'check_email', 'event_info': self.lineEdit.text()})) == 'true\n':
            self.error_dialog.showMessage('Пользователь с такой почтой уже зарегестрирован.')
            return
        if requests.post('http://2f9f839aebbd.ngrok.io/register',
                         json.dumps(
                             {'version': 1.0, 'ip': socket.gethostbyname(socket.gethostname()),
                              'event': 'check_дщпшт', 'event_info': self.lineEdit_2.text()})).text == 'true\n':
            self.error_dialog.showMessage('Пользователь с таким логином уже зарегестрирован.')
            return
        if self.lineEdit_3.text() != self.lineEdit_4.text():
            self.error_dialog.showMessage('Пароли не совпадают.')
            return
        try:
            if check_password(self.lineEdit_3.text()) == 'ok':
                requests.post('http://2f9f839aebbd.ngrok.io/register',
                              json.dumps(
                                  {'version': 1.0, 'ip': socket.gethostbyname(socket.gethostname()),
                                   'event': 'wait_mail', 'event_info': self.lineEdit.text()}))
                global reg_password, reg_mail, reg_login
                reg_mail = self.lineEdit.text()
                reg_login = self.lineEdit_2.text()
                reg_password = self.lineEdit_3.text()
                open_window(Numbers, self.x(), self.y(), self.width(), self.height())
                self.close()
        except Exception as error:
            if error.__class__.__name__ == 'LengthError':
                self.error_dialog.showMessage('Пароль должен быть больше 8 символов.')
            elif error.__class__.__name__ == 'LetterError':
                self.error_dialog.showMessage('В пароле должны быть строчные и заглавные буквы.')
            elif error.__class__.__name__ == 'DigitError':
                self.error_dialog.showMessage('В пароле должно быть хотя бы одно число.')
            elif error.__class__.__name__ == 'SequenceError':
                self.error_dialog.showMessage('Пароль слишком лёгкий.:-)')


class Numbers(QMainWindow, Ui_Form_3):
    def __init__(self):
        super().__init__()
        self.error_dialog = QtWidgets.QErrorMessage()
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.setupUi(self.central_widget)
        self.pushButton.pressed.connect(self.return_first_window)

    def return_first_window(self):
        if requests.post('http://2f9f839aebbd.ngrok.io/register',
                            json.dumps(
                                {'version': 1.0, 'ip': socket.gethostbyname(socket.gethostname()),
                                 'event': 'send_numbers',
                                 'event_info': [self.lineEdit.text(), reg_login, reg_password,
                                                reg_mail]})).text == 'true\n':
            open_window(First_window, self.x(), self.y(), self.width(), self.height())
            self.close()
        else:
            self.error_dialog.showMessage('Ты ввёл неправильные числа.')




def main():
    app = QApplication(sys.argv)
    ex = Test_conection_window()
    ex.show()
    app.exec_()
    return playing
