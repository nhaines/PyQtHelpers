__author__ = 'nhaines'

from PyQt4 import QtCore
from PyQt4 import QtNetwork


class HttpRequestSignals(QtCore.QObject):
    finished = QtCore.pyqtSignal(QtNetwork.QTcpSocket, QtCore.QByteArray)


class HttpRequestHandler(QtCore.QRunnable):
    def __init__(self, socket):
        super(HttpRequestHandler, self).__init__()
        self.signals = HttpRequestSignals()
        self.socket = socket
        self.request = QtNetwork.QHttpRequestHeader()
        self.response = QtNetwork.QHttpResponseHeader()
        self.data = QtCore.QByteArray()

    def handle_request(self):
        # override this in subclasses to do custom logic
        self.response.setStatusLine(404)
        self.data.append(self.response.toString())

    def run(self):
        count = 0
        while self.socket.canReadLine():
            line = str(self.socket.readLine())
            self.request.parseLine(line, count)
            count += 1

        self.handle_request()
        self.signals.finished.emit(self.socket, self.data)


class HttpServer(QtNetwork.QTcpServer):
    RUNNER_CLASS = HttpRequestHandler

    def __init__(self, parent=None):
        super(HttpServer, self).__init__(parent)
        self.__pool = QtCore.QThreadPool(self)
        self.__connect()

    def __connect(self):
        self.newConnection.connect(self.handle_connection)

    def finish_socket(self, socket, response):
        socket.write(response)
        socket.disconnectFromHost()

    def handle_connection(self):
        sock = self.nextPendingConnection()
        runner = self.RUNNER_CLASS(sock)
        runner.signals.finished.connect(self.finish_socket)
        self.__pool.start(runner)