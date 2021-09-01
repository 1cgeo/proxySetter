from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import pyqtSignal


class ProxyComboBox(QComboBox):

    def __init__(self):
        super(ProxyComboBox, self).__init__()

    def loadProxyOptions(self, options):
        self.addItems( options )
       
