from proxySetter.widgets.proxyComboBox import ProxyComboBox
from proxySetter.widgets.proxyDialog import ProxyDialog

class WidgetFactory:

    def createWidget(self, widgetName):
        widgetNames = {
            'ProxyComboBox': ProxyComboBox,
            'ProxyDialog': ProxyDialog
        }
        return widgetNames[ widgetName ]()