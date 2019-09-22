from PyQt5.QtQuick import QQuickPaintedItem
from PyQt5.QtCore import pyqtProperty, pyqtSlot, Qt, pyqtSignal
from PyQt5.QtGui import QColor, QPen, QPainter, QBrush, QFont, QFontMetricsF
from controller import Container
import numpy as np

class AxesRender(QQuickPaintedItem):
    def __init__(self, parent=None):
        super(AxesRender, self).__init__()
        self._num_signals = None
        self._yaxes_positions = None
        self._xaxes_positions = None
        self._mm_per_sec = None

    def paint(self, painter):
        if self._num_signals is None:
            return None
        self._calc_visual_parametres()
        pen = QPen()
        pen.setStyle(Qt.DashLine)
        pen.setWidth(1)
        pen.setBrush(QColor('#565656'))

        painter.setPen(pen)
        for i in range(self._num_signals):
            painter.drawLine(0, self._yaxes_positions[i],
                             self.width(), self._yaxes_positions[i])

    def _calc_visual_parametres(self):
        self._yaxes_positions = np.zeros([self._num_signals], dtype=np.float)
        yaxe_shift = float(self.height()) / float(self._num_signals) / float(2)
        for i in range(self._num_signals):
            self._yaxes_positions[i] = (i * 2 + 1) * yaxe_shift

    @pyqtSlot(Container)
    def setContainer(self, inContainer):
        self._num_signals = inContainer.num_signals
        self.update()

