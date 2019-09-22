from PyQt5.QtQuick import QQuickPaintedItem
from PyQt5.QtCore import pyqtProperty, pyqtSlot, Qt, pyqtSignal
from PyQt5.QtGui import QColor, QPen, QPainter, QBrush, QFont, QFontMetricsF
from controller import Container
import numpy as np


class SignalLabelsRender(QQuickPaintedItem):
    def __init__(self, parent=None):
        super(SignalLabelsRender, self).__init__(parent)
        self._signal_labels = None  # Container object
        self._num_signals = None  # int
        self._vertical_rect_margin = float(1)  # поле снизу и сверху прямоугольника
        self._rect_height = None
        self._text_height = None
        self._rect_inceptions_y = None
        self._text_inceptions_y = None
        self._text_font = None
        self._maximum_text_width = None
        self._rect_pen = QPen(Qt.NoPen)
        self._rect_color = QColor('#3700B3')
        self._rect_brush = QBrush(self._rect_color)
        self._text_pen = QPen(Qt.white)
        self._font = QFont('Calibri')
        self._font.setItalic(True)

    widgetTextChanged = pyqtSignal(int, arguments=['widgetWidth'])

    def _calc_visual_parametres(self):
        self._rect_height = (float(self.height()) / float(self._num_signals)) - 2 * self._vertical_rect_margin
        text_widths = np.zeros([self._num_signals], dtype=np.float)
        self._rect_inceptions_y = np.zeros([self._num_signals], dtype=np.float)
        self._text_inceptions_y = np.zeros([self._num_signals], dtype=np.float)
        for idx, item in enumerate(self._signal_labels):
            rect_inc_y = float((idx * 2 + 1) * self._vertical_rect_margin + float(idx) * self._rect_height)
            self._rect_inceptions_y[idx] = rect_inc_y
            self._text_height = self._rect_height - 2
            if self._text_height > 12:
                self._text_height = 12
            padding = (self._rect_height - self._text_height) / 2
            self._text_inceptions_y[idx] = rect_inc_y + padding + self._text_height
            self._text_font = QFont('Calibri')
            self._text_font.setPointSize(self._text_height)
            fm = QFontMetricsF(self._text_font)
            text_widths[idx] = fm.horizontalAdvance(item)
        self._maximum_text_width = np.max(text_widths)
        self.widgetTextChanged.emit(self._maximum_text_width + 5)

    def paint(self, painter):
        if self._signal_labels is not None:
            self._calc_visual_parametres()
            painter.setBrush(self._rect_brush)
            self._font.setPointSize(self._text_height)
            for i in range(self._num_signals):
                painter.setPen(self._rect_pen)
                painter.drawRect(0, self._rect_inceptions_y[i], self.width(), self._rect_height)
                painter.setFont(self._font)
                painter.setPen(self._text_pen)
                painter.drawText(3, self._text_inceptions_y[i], self._signal_labels[i])

    @pyqtSlot(Container)
    def setContainer(self, inContainer):
        self._signal_labels = inContainer.signal_labels
        self._num_signals = len(self._signal_labels)
        self._calc_visual_parametres()
        self.update()
