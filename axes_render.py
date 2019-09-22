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
        self._xaxes_positions = []
        self._mm_per_sec = 30
        self._pixel_density = float(5)

    def paint(self, painter):
        if self._num_signals is None:
            return None
        self._calc_visual_parametres()
        pen = QPen()
        pen.setStyle(Qt.DashLine)
        pen.setWidth(1)
        pen.setBrush(QColor('#565656'))

        painter.setPen(pen)
        for curr_yaxe_position in self._yaxes_positions:
            painter.drawLine(0, curr_yaxe_position,
                             self.width(), curr_yaxe_position)
        for curr_xaxe_position in self._xaxes_positions:
            painter.drawLine(curr_xaxe_position, 0,
                             curr_xaxe_position, self.height())

    def _calc_visual_parametres(self):
        self._yaxes_positions = np.zeros([self._num_signals], dtype=np.float)
        yaxe_shift = float(self.height()) / float(self._num_signals) / float(2)
        for i in range(self._num_signals):
            self._yaxes_positions[i] = (i * 2 + 1) * yaxe_shift
        self._xaxes_positions.clear()
        sch = float(0)
        while True:
            sch += 1
            curr_axe_coord = sch * self._mm_per_sec * self._pixel_density
            if curr_axe_coord >= self.width():
                break
            self._xaxes_positions.append(curr_axe_coord)

    @pyqtSlot(Container)
    def setContainer(self, inContainer):
        self._num_signals = inContainer.num_signals
        self.update()

    @pyqtProperty(float)
    def pixelDensity(self):
        return self._pixel_density

    @pixelDensity.setter
    def pixelDensity(self, in_pixel_density):
        self._pixel_density = in_pixel_density



