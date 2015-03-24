__author__ = 'nhaines'

from PyQtHelpers import app, network
from PyQt4 import QtGui


class MyHandler(network.HttpRequestHandler):
    def handle_request(self):
        # override this in subclasses to do custom logic
        self.response.setStatusLine(200)
        self.data.append(self.response.toString())

        print "using custom handler"


myapp = app.HttpServerApp()
myapp.server.RUNNER_CLASS = MyHandler
wind = QtGui.QMainWindow()
wind.show()
myapp.exec_()