"""
File: NwSeries.py
Series of network parameters organized in a frequency axis.
"""
import numpy as np

class NwSeries(np.ndarray):
    def __init__(self, src:np.ndarray):
        self.series = src

    def __mul__(self, another:NwSeries):
        if len(self.series.shape) != 3 or len(another.series.shape) != 3:
            raise("type mismatch")
        if self.series.shape != another.series.shape:
            raise("size mismatch")
        """declare result series object"""
        result = np.zeros(self.series.shape, complex)
        for i in range(self.series.shape[0]):
            result[i] = np.asmatrix(self.series[i]) * np.asmatrix(another.series[i])
        return NwSeries(result)

    def inv(self):
        if len(self.series.shape) != 3 or len(another.series.shape) != 3:
            raise("type mismatch")
        if self.series.shape != another.series.shape:
            raise("size mismatch")
        """declare result series object"""
        result = np.zeros(self.series.shape, complex)
        for i in range(self.series.shape[0]):
            result[i] = np.linalg.inv(np.asmatrix(self.series[i]))
        return NwSeries(result)

    """
    Read TouchStone v2.x file.
    """
    def readTSV2(self, w:np.ndarray):
