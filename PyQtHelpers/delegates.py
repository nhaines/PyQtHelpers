__author__ = 'nhaines'

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtCore import Qt


class ColorfulProgressDelegate(QtGui.QStyledItemDelegate):
    redraw = QtCore.pyqtSignal()

    def __init__(self, parent=None, progress_role=None, total_role=None, opacity=1.0, animate=True):
        super(ColorfulProgressDelegate, self).__init__(parent)
        self.progress_role = progress_role
        self.total_role = total_role
        self.opacity = opacity
        self.__highlight = 0.0
        self.__animate = None

        self.animation = QtCore.QPropertyAnimation(self, "highlight")
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setDuration(2000)  # 2 seconds
        self.animation.setLoopCount(-1)  # loop forever
        self.animate = animate

    @property
    def animate(self):
        return self.__animate

    @animate.setter
    def animate(self, value):
        self.__animate = value
        if value:
            self.animation.start()
        else:
            self.animation.stop()

    @QtCore.pyqtProperty(float)
    def highlight(self):
        return self.__highlight

    @highlight.setter
    def highlight(self, value):
        self.__highlight = value
        self.redraw.emit()

    def paint(self, painter, option, index):
        if self.progress_role is None or self.total_role is None:
            super(ColorfulProgressDelegate, self).paint(painter, option, index)
            return

        fill = float(index.data(self.progress_role))/float(index.data(self.total_role))
        bar_rect = QtCore.QRectF(option.rect)
        bar_rect.setRight(bar_rect.width()*fill)
        fill_color = QtGui.QColor.fromHsvF(fill / 3.0, 1.0, 1.0, self.opacity)

        if self.animate:
            fill_brush = QtGui.QLinearGradient(bar_rect.topLeft(), bar_rect.topRight())
            fill_brush.setColorAt(0.0, fill_color)
            fill_brush.setColorAt(1.0, fill_color)
            highlight_color = QtGui.qApp.palette().background().color()
            highlight_color.setAlphaF(self.opacity)
            fill_brush.setColorAt(self.highlight, highlight_color)
        else:
            fill_brush = fill_color

        painter.fillRect(bar_rect, fill_brush)
        painter.drawText(option.rect, Qt.AlignCenter, "%.01f%%" % (fill*100.0))
