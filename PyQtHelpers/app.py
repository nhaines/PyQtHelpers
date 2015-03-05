__author__ = 'nhaines'

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtNetwork


class BaseApp(QtGui.QApplication):
    def __init__(self, argv=[], organization="PyQtHelpers", name="Default"):
        super(BaseApp, self).__init__(argv)
        self.setOrganizationName(organization)
        self.setApplicationName(name)
        self.onLoad()
        self.__connect()

    def __connect(self):
        self.lastWindowClosed.connect(self.onExit)

    def onLoad(self):
        pass

    def onExit(self):
        pass


class HttpClientApp(BaseApp):
    def __init__(self, argv=[], organization="PyQtHelpers", name="Default"):
        self.manager = QtNetwork.QNetworkAccessManager()
        super(HttpClientApp, self).__init__(argv, organization, name)

    def onLoad(self):
        cookies = QtNetwork.QNetworkCookie.parseCookies(QtCore.QSettings().value("manager/cookies", ""))
        cookie_jar = QtNetwork.QNetworkCookieJar()
        cookie_jar.setAllCookies(cookies)
        self.manager.setCookieJar(cookie_jar)

    def onExit(self):
        cookies = QtCore.QByteArray()
        for cookie in self.manager.cookieJar().allCookies():
            cookies.append(cookie.toRawForm())
        QtCore.QSettings().setValue("manager/cookies", cookies)
