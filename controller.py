from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty
from edf_loader import EEGStorage


class Container(QObject):
    def __init__(self, parent=None):
        super(Container, self).__init__()
        self._signal_labels = None  # list
        self.signals = None  # list
        self.fd = None  # ndarray
        self._num_signals = 0  # int
        self.signal_sizes = None  # ndarray
        self.duration = 0  # int

    @pyqtProperty(list)
    def signal_labels(self):
        return self._signal_labels

    @signal_labels.setter
    def signal_labels(self, in_labels):
        self._signal_labels = in_labels

    @pyqtProperty(int)
    def num_signals(self):
        return self._num_signals

    @num_signals.setter
    def num_signals(self, in_signals):
        self._num_signals = in_signals


class Controller(QObject):

    def __init__(self, parent=None):
        super(Controller, self).__init__()
        self._container = Container()
        self._eeg_storage = EEGStorage()

    eegSignalsChanged = pyqtSignal(Container, arguments=['currContainer'])

    @pyqtSlot(str)
    def loadSignalsFromEdf(self, inPath):
        path = self.string_process(inPath)
        self._eeg_storage.load_signals_from_edf(path)
        self._write_data_to_container()

    def _write_data_to_container(self):
        self._container.signals = self._eeg_storage.raw_signals
        self._container.fd = self._eeg_storage.fd
        self._container.signal_labels = self._eeg_storage.signal_labels
        self._container.num_signals = self._eeg_storage.num_signals
        self._container.signal_sizes = self._eeg_storage.signal_sizes
        self._container.duration = self._eeg_storage.duration

        self.eegSignalsChanged.emit(self._container)

    @staticmethod
    def string_process(in_string):
        pattern = "file:///"
        return in_string.replace(pattern, "")