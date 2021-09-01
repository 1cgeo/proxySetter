from qgis.PyQt.QtNetwork import QNetworkProxy, QNetworkProxyFactory
from qgis.core import QgsSettings, QgsNetworkAccessManager
from factories.widgetFactory import WidgetFactory
import json
import os

class ProxyCtrl:

    def __init__(
            self,
            widgetFactory=WidgetFactory()
        ):
        self.widgetFactory = widgetFactory

    PROXY_CONFIG_FILE = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        '..',
        'config.json'
    )

    def getProxyOptions(self):
        options = []
        with open(self.PROXY_CONFIG_FILE, 'r', encoding='utf-8') as f:
            options =  [ option for option in json.load(f) ]
        return options

    def getProxyOption(self, proxyName):
        option = {}
        with open(self.PROXY_CONFIG_FILE, 'r', encoding='utf-8') as f:
            option = json.load(f)[ proxyName ]
        return option

    def saveProxyOption(self, proxyName, option):
        with open(self.PROXY_CONFIG_FILE, 'w', encoding='utf-8') as f:
            data = json.load(f)
            data[ proxyName ] = option
            f.write( data )

    def getProxyComboWidget(self):
        proxyComboBox = self.widgetFactory.createWidget( 'ProxyComboBox' )
        proxyComboBox.loadProxyOptions( self.getProxyOptions() )
        proxyComboBox.currentTextChanged.connect( self.changeNetworkProxy )
        return proxyComboBox

    def getProxyDialog(self):
        proxyDialog = self.widgetFactory.createWidget( 'ProxyDialog' )
        return proxyDialog

    def encodeB64(self, text):
        temp = base64.b64decode(bytes(text['password'], 'utf-8'))
        return temp.decode('utf-8')

    def changeNetworkProxy(self, proxyName):
        option = self.getProxyOption( proxyName )
        if not (option['user'] or option['password']):
            proxyDialog = self.getProxyDialog()
            if proxyDialog.showCustom():
                inputData = proxyDialog.getData()
                option['user'] = inputData['user']
                option['password'] = self.encodeB64( inputData['password'] )
                self.saveProxyOption( proxyName, option )
        self.setCurrentNetworkProxy( option )

    def setCurrentNetworkProxy(self, option):
        proxy = QNetworkProxy(
            QNetworkProxy.HttpProxy,
            hostName = option['host'],
            port = option['port'],
            user = option['user'],
            password = option['password']
        )
        QNetworkProxy.setApplicationProxy( proxy )
        QgsNetworkAccessManager.instance().setFallbackProxyAndExcludes( proxy, [], option['noProxy'] )