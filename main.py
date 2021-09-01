import os, sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from controllers.proxyCtrl import ProxyCtrl

class Main:
    
    def __init__(
            self,
            iface,
            proxyCtrl=ProxyCtrl()
        ):
        self.iface = iface
        self.proxyCtrl = proxyCtrl
        self.proxyComboBox = None

    def initGui(self):
        self.proxyComboBox = self.iface.addToolBarWidget(
            self.proxyCtrl.getProxyComboWidget()
        )

    def unload(self):
        self.iface.removeToolBarIcon(self.proxyComboBox) if self.proxyComboBox else ''
        del self.comboBox