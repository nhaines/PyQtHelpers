__author__ = 'nhaines'

import sip

for qt_class in ["QDate", "QDateTime", "QString", "QTextStream", "QTime", "QUrl", "QVariant"]:
    sip.setapi(qt_class, 2)