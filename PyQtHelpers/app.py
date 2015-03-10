__author__ = 'nhaines'

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtNetwork

import network


class BaseApp(QtGui.QApplication):
    def __init__(self, argv=[], organization="PyQtHelpers", name="Default"):
        super(BaseApp, self).__init__(argv)
        self.setOrganizationName(organization)
        self.setApplicationName(name)
        self.onLoad()
        self.lastWindowClosed.connect(self.onExit)

    def onLoad(self):
        pass

    def onExit(self):
        pass


class HttpClientApp(BaseApp):
    def __init__(self, argv=[], organization="PyQtHelpers", name="Default"):
        self.client = QtNetwork.QNetworkAccessManager()
        super(HttpClientApp, self).__init__(argv, organization, name)

    def onLoad(self):
        cookies = QtNetwork.QNetworkCookie.parseCookies(QtCore.QSettings().value("network/client/cookies", ""))
        cookie_jar = QtNetwork.QNetworkCookieJar()
        cookie_jar.setAllCookies(cookies)
        self.client.setCookieJar(cookie_jar)

    def onExit(self):
        cookies = QtCore.QByteArray()
        for cookie in self.client.cookieJar().allCookies():
            cookies.append(cookie.toRawForm())
        QtCore.QSettings().setValue("network/client/cookies", cookies)


class HttpServerApp(BaseApp):
    def __init__(self, argv=[], organization="PyQtHelpers", name="Default", port=80):
        self.server = network.HttpServer()
        super(HttpServerApp, self).__init__(argv, organization, name)
        self.server.listen(port=port)
