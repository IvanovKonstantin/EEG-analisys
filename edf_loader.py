import pyedflib
import numpy as np


class EEGStorage():
    def __init__(self):
        self._num_signals = 0
        self._duration = 0  # длительность сигнала в мс
        self._raw_signals = []
        self._psignals = []
        self._signal_labels = []
        self._fd = None  # numpy array
        self._signal_sizes = None  # numpy array

    def load_signals_from_edf(self, in_path):
        edf_reader = pyedflib.EdfReader(in_path)
        self._num_signals = edf_reader.signals_in_file
        self._fd = edf_reader.getSampleFrequencies().astype(float)
        self._num_signals = edf_reader.signals_in_file
        self._raw_signals.clear()
        for i in range(edf_reader.signals_in_file):
            self._raw_signals.append(edf_reader.readSignal(i))
        self._signal_labels = edf_reader.getSignalLabels()
        self._signal_sizes = edf_reader.getNSamples()
        self._duration = edf_reader.getFileDuration()

        for i in range(self._num_signals):
            if self._fd[i] == 0:
                self._fd[i] = self._signal_sizes[i] / self._duration

    @property
    def raw_signals(self):
        return self._raw_signals

    @property
    def fd(self):
        return self._fd

    @property
    def signal_labels(self):
        return self._signal_labels

    @property
    def num_signals(self):
        return self._num_signals

    @property
    def signal_sizes(self):
        return self._signal_sizes

    @property
    def duration(self):
        return self._duration
