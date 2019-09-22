from PyQt5.QtQuick import (QQuickItem, QSGFlatColorMaterial,
                           QSGGeometry, QSGGeometryNode, QSGNode, QSGTransformNode)
from PyQt5.QtCore import pyqtProperty, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QMatrix4x4, QColor
import numpy as np

from controller import Container


class EEGRender(QQuickItem):
    def __init__(self, parent=None):
        super(EEGRender, self).__init__(parent)

        self._pixel_density = float(5)
        self._showsig_trig = False  # триггер, сигнализирует о загрузке нового сигнала
        self._yscale = float(1)  # как масштабировать сигнал по оси y
        self._mm_per_sec = float(30)
        self._time_shift = float(0)
        self._container = None
        self._lineshift_y = float(0)
        self._visible_signal_sizes = None
        self._time_axes = None
        self._root_node = None
        self._xscales = None
        self._valid_shift = int(0)

        self.setFlag(QQuickItem.ItemHasContents, True)
        self.setAntialiasing(True)

    validShiftChanged = pyqtSignal(float, arguments=['valShift'])

    def _change_visible_parametres(self):
        if self._container is not None:
            self._showsig_trig = True

            def calc_visible_signal_size(in_fd):
                return int((in_fd * self.width()) / (self._pixel_density * self._mm_per_sec)) + 1

            def update_valid_shift():
                record_duration = self._container.duration
                visible_signal_duration = self.width() / self._pixel_density / self._mm_per_sec
                if record_duration == 0 or record_duration <= visible_signal_duration:
                    self._valid_shift = 0
                    self._time_shift = 0
                else:
                    self._valid_shift = record_duration - visible_signal_duration
                    if self._time_shift > self._valid_shift:
                        self._time_shift = self._valid_shift
                # отправляем сигнал об изменении допустимого сдвига
                self.validShiftChanged.emit(self._valid_shift)

            num_signals = self._container.num_signals
            if num_signals != 0:
                self._lineshift_y = self.height() / (2 * float(num_signals))

            # определение количества видимых отсчетов для каждого отведения
            self._visible_signal_sizes = np.zeros([num_signals], dtype=np.int)
            for idx, curr_fd in enumerate(self._container.fd):
                self._visible_signal_sizes[idx] = calc_visible_signal_size(curr_fd)

            # вычисление осей времени для каждого отведения
            self._time_axes = [np.arange(self._visible_signal_sizes[i], dtype=np.float32)
                               for i in range(num_signals)]

            #  определяем как масштабировать сигнал по оси X
            self._xscales = np.zeros([num_signals], dtype=np.float32)
            for idx, curr_fd in enumerate(self._container.fd):
                self._xscales[idx] = (self._mm_per_sec / curr_fd) * self._pixel_density

            # определение допустимого сдвига сигнала
            update_valid_shift()

    @pyqtSlot(Container)
    def setContainer(self, inContainer):
        self._container = inContainer
        self._time_shift = 0
        self._change_visible_parametres()
        self.update()

    @pyqtSlot()
    def changeVisibleParametres(self):
        if self._visible_signal_sizes is not None:
            self._change_visible_parametres()
            self.update()

    @pyqtSlot(float)
    def setAmplitude(self, in_amplitude):
        self._yscale = (1 / in_amplitude) * self._pixel_density
        self._showsig_trig = True
        self.update()

    @pyqtSlot(float)
    def shiftSignal(self, shift):
        self._time_shift = shift
        self.update()

    @pyqtProperty(float)
    def validShift(self):
        return self._valid_shift

    @pyqtProperty(float)
    def currentShift(self):
        return self._time_shift

    @pyqtProperty(float)
    def pixelDensity(self):
        return self._pixel_density

    @pixelDensity.setter
    def pixelDensity(self, in_pixel_density):
        self._pixel_density = in_pixel_density
        self._yscale = self._pixel_density / 10.0

    def updatePaintNode(self, old_node, node_data):
        if self._container is None:
            return self._root_node

        if self._showsig_trig:
            self._showsig_trig = False
            if self._root_node is not None:
                self._root_node.removeAllChildNodes()
                del self._root_node
                self._root_node = None

        if self._root_node is None:
            self._root_node = QSGNode()
            for i in range(self._container.num_signals):
                # создаем ноды для рисования графиков
                transform_node = QSGTransformNode()
                transform_matrix = transform_node.matrix()
                transform_matrix.translate(0, self._lineshift_y * (2 * i + 1))
                transform_matrix.scale(self._xscales[i], -self._yscale)
                transform_node.setMatrix(transform_matrix)
                transform_node.markDirty(QSGNode.DirtyMatrix)

                geometry_node = QSGGeometryNode()
                geometry = QSGGeometry(QSGGeometry.defaultAttributes_Point2D(),
                                       self._visible_signal_sizes[i])
                geometry.setLineWidth(1.0)
                geometry.setDrawingMode(QSGGeometry.GL_LINE_STRIP)
                geometry_node.setGeometry(geometry)
                geometry_node.setFlag(QSGNode.OwnsGeometry)

                material = QSGFlatColorMaterial()
                material.setColor(QColor("#4CAF50"))
                geometry_node.setMaterial(material)
                geometry_node.setFlag(QSGNode.OwnsMaterial)

                transform_node.appendChildNode(geometry_node)
                self._root_node.appendChildNode(transform_node)

        eeg_signals = self._container.signals
        fd = self._container.fd
        for i in range(self._container.num_signals):
            curr_signal = eeg_signals[i]
            curr_timeaxe = self._time_axes[i]
            curr_transform_node = self._root_node.childAtIndex(i)
            curr_geometry_node = curr_transform_node.firstChild()
            curr_geometry = curr_geometry_node.geometry()
            curr_vertexes = curr_geometry.vertexDataAsPoint2D()
            curr_shift = int(self._time_shift * fd[i])
            for j in range(self._visible_signal_sizes[i]):
                curr_vertexes[j].set(curr_timeaxe[j],
                                     curr_signal[j + curr_shift])
            curr_geometry_node.markDirty(QSGNode.DirtyGeometry)

        return self._root_node

