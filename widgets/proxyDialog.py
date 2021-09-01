from PyQt5.QtWidgets import QDialog, QLineEdit, QLabel, QFormLayout, QPushButton
from PyQt5.QtCore import pyqtSignal


class ProxyDialog(QDialog):

    triggerUpdate = pyqtSignal(str)

    def __init__(self):
        super(ProxyDialog, self).__init__()
        layout = QFormLayout()
        btn = QPushButton("Enviar dados")
        btn.clicked.connect(self.accept)
        label_username = QLabel('Insira o usuário do Proxy:')
        self.username = QLineEdit()
        label_password = QLabel('Insira a senha do Proxy:')
        self.password = QLineEdit()
        self.password.setEchoMode(2)

        layout.addRow(label_username)
        layout.addRow(self.username)
        layout.addRow(label_password)
        layout.addRow(self.password)
        layout.addRow(btn)

        self.setLayout(layout)

        self.setWindowTitle('Inserir dados do Proxy')

    def getData(self):
        return {
            'user': self.username.text(),
            'password': self.password.text()
        }

    def showCustom(self):
        result = self.exec_()
        return result == QDialog.Accepted
