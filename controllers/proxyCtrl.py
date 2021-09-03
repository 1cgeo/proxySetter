from qgis.PyQt.QtNetwork import QNetworkProxy, QNetworkProxyFactory
from qgis.core import QgsSettings, QgsNetworkAccessManager
from proxySetter.factories.widgetFactory import WidgetFactory
import json
import os
import base64

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
        data = {}
        with open(self.PROXY_CONFIG_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        with open(self.PROXY_CONFIG_FILE, 'w', encoding='utf-8') as f:
            data[ proxyName ] = option
            json.dump(data, f)

    def getProxyComboWidget(self):
        proxyComboBox = self.widgetFactory.createWidget( 'ProxyComboBox' )
        proxyComboBox.loadProxyOptions( self.getProxyOptions() )
        proxyComboBox.currentTextChanged.connect( self.changeNetworkProxy )
        return proxyComboBox

    def getProxyDialog(self):
        proxyDialog = self.widgetFactory.createWidget( 'ProxyDialog' )
        return proxyDialog

    def encryptNetworkPassword(self, text):
        return base64.b64encode(bytes(text, 'utf-8')).decode('utf-8')
    
    def decryptNetworkPassword(self, text):
        return base64.b64decode(text).decode('utf-8')

    def changeNetworkProxy(self, proxyName):
        option = self.getProxyOption( proxyName )
        if not (option['user'] or option['password']):
            proxyDialog = self.getProxyDialog()
            if proxyDialog.showCustom():
                inputData = proxyDialog.getData()
                option['user'] = inputData['user']
                option['password'] = self.formatNetworkPassword( inputData['password'] )
                self.saveProxyOption( proxyName, option )
        self.setCurrentNetworkProxy( option )

    def setCurrentNetworkProxy(self, option):
        s = QgsSettings()
        s.setValue('proxy/proxyEnabled', 'true')
        s.setValue('proxy/proxyHost', option['host'])
        s.setValue('proxy/proxyPort', option['port'])
        s.setValue('proxy/proxyUser', option['user'])
        s.setValue('proxy/proxyPassword', self.decryptNetworkPassword( option['password'] ))
        s.setValue('proxy/proxyType', option['proxyType'])
        s.setValue('proxy/noProxyUrls', option['noProxy'])
        s.sync()
        proxy = QNetworkProxy(
            QNetworkProxy.HttpProxy,
            hostName = option['host'],
            port = option['port'],
            user = option['user'],
            password = option['password']
        )
        QNetworkProxy.setApplicationProxy( proxy )
        QgsNetworkAccessManager.instance().setFallbackProxyAndExcludes( proxy, [], option['noProxy'] )

        