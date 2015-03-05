__author__ = 'nhaines'

from PyQt4 import QtCore
from PyQt4 import QtNetwork


class NetworkAccessModel(QtCore.QAbstractItemModel):
    def __init__(self, parent=None):
        super(NetworkAccessModel, self).__init__(parent)
        self.manager = QtNetwork.QNetworkAccessManager(self)
