__author__ = 'nhaines'

from PyQtHelpers import app, delegates
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtCore import Qt


class ProgressListModel(QtCore.QAbstractListModel):
    PROGRESS_ROLE = Qt.UserRole + 1
    TOTAL_ROLE = Qt.UserRole + 2

    def __init__(self, parent=None):
        super(ProgressListModel, self).__init__(parent)
        self.__data = [
            {'progress': 10,
             'total': 100,
             },
            {'progress': 90,
             'total': 100
             },
        ]

    def rowCount(self, index=QtCore.QModelIndex()):
        return len(self.__data)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return

        item = self.__data[index.row()]
        if role == Qt.DisplayRole:
            role = self.PROGRESS_ROLE

        if role == self.PROGRESS_ROLE:
            return item.get('progress', 0)
        elif role == self.TOTAL_ROLE:
            return item.get('total', 0)

if __name__ == "__main__":
    import sys
    myapp = app.BaseApp()
    model = ProgressListModel()

    delegate = delegates.ColorfulProgressDelegate(progress_role=model.PROGRESS_ROLE, total_role=model.TOTAL_ROLE,
                                                  opacity=0.5)
    delegate.animate = False

    view = QtGui.QListView()
    view.setModel(model)
    view.setItemDelegate(delegate)

    delegate.redraw.connect(view.viewport().update)
    view.show()
    sys.exit(myapp.exec_())