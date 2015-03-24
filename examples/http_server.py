__author__ = 'nhaines'

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from PyQtHelpers import app, network
from PyQt4 import QtGui


class MyHandler(network.HttpRequestHandler):
    def handle_request(self):
        print "using custom handler"
        if self.request.method() == "GET":
            print "getting..."
        self.response.setStatusLine(200)
        self.data.append(self.response.toString())


if __name__ == "__main__":
    myapp = app.HttpServerApp()
    myapp.server.RUNNER_CLASS = MyHandler
    wind = QtGui.QMainWindow()
    wind.show()
    sys.exit(myapp.exec_())