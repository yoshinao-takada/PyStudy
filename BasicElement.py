"""
File:   BasicElement.py
Basic two-terminal element definition and admittance evaluation.
"""
import numpy as np
from enum import Enum
class ElementType(Enum):
    Resistance = 0
    Inductance = 1
    Capacitance = 2

class NetworkType(Enum):
    SeriesY = 0
    ShuntZ = 1

class BasicElement(object):
    """Constructor defines a two terminal element with parasitic elements."""
    def __init__(self, etype: ElementType, \
             r: float, l: float, c: float, g: float = 0):
        self.mytype = etype
        self.r = r
        self.l = l
        self.c = c
        self.g = g

    """Admittance of a two terminal elemeent at an angular frequency w"""
    def Y(self, w: float):
        y : complex = 0
        s : complex = complex(0, w)
        if self.mytype == ElementType.Resistance:
            y = s * self.c + 1 / (self.r + s * self.l)
        elif self.mytype == ElementType.Inductance:
            y = s * self.c + 1 / (self.r + s * self.l)
        elif self.mytype == ElementType.Capacitance:
            y = self.g + 1/(self.r + s * self.l + 1/(s * self.c))
        return y
    
    """Admittance or impedance matrix of series or shunt 2-port network
        at an angular frequency w"""
    def Mat2Port(self, nwType: NetworkType, w: float):
        m = object
        if (nwType == NetworkType.SeriesY):
            y: float = self.Y(w)
            m = np.array([[y, -y], [-y, y]])
        elif (nwType == NetworkType.ShuntZ):
            z: float = 1/self.Y(w)
            m = np.array([[z, z], [z, z]])
        return m
        
    """Array of admittance or impedance matrices over angular frequencies w[]"""
    def MatArray2Port(self, nwType: NetworkType, w):
        point: int = len(w)
        marray = np.zeros((point, 2, 2), complex, 'C')
        for i in range(point):
            m = self.Mat2Port(nwType, w[i])
            marray[i] = m
        return marray
