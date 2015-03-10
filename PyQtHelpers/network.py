__author__ = 'nhaines'

from PyQt4 import QtCore
from PyQt4 import QtNetwork


class HttpRequestHandler(QtCore.QRunnable, QtCore.QObject):
    finished = QtCore.pyqtSignal(QtNetwork.QTcpSocket, QtCore.QByteArray)

    def __init__(self, socket):
        super(HttpRequestHandler, self).__init__()
        self.socket = socket

    def run(self):
        request = QtNetwork.QHttpRequestHeader()
        # data = QtCore.QByteArray()

        print request.readAll()


class HttpServer(QtNetwork.QTcpServer):
    def __init__(self, parent=None):
        super(HttpServer, self).__init__(parent)
        self.__pool = QtCore.QThreadPool(self)
        self.__connect()

    def __connect(self):
        self.newConnection.connect(self.handle_connection)

    def handle_connection(self):
        print 'handle it'
        sock = self.nextPendingConnection()
        runner = HttpRequestHandler(socket)
        # self.__pool.