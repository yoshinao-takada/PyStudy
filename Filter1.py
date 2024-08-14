import matplotlib.pyplot as plt
import numpy as np
from BasicElement import BasicElement as be
from BasicElement import ElementType as et
from BasicElement import NetworkType as nt
from NwConv import NwConv as nc
import math

PI2:float = math.pi * 2.0
Z0:float = 50.0
ZP:list = [Z0, Z0]
L0:float = 1
C1:float = 2
L2:float = 1

def CreateW() -> np.ndarray:
    fmin:float = 0
    fmax:float = 2e9
    w = np.linspace(PI2 * fmin, PI2 * fmax, 21)
    return w

def CreateFilter() -> np.ndarray:
    fc:float = 1e9 # cutoff frequency
    wc = fc * PI2
    w = CreateW()
    lx0 = L0 * Z0 / wc
    cx1 = C1 / (Z0 * wc)
    lx2 = L2 * Z0 / wc
    beL0:be = be(et.Inductance, 1e-6, lx0, cx1 * 1e-2, 1e-9)
    beC1:be = be(et.Capacitance, 1e-6, lx0 * 1e-2, cx1, 1e-9)
    beL2:be = be(et.Inductance, 1e-6, lx2, cx1 * 1e-2, 1e-9)
    seriesY_L0:np.ndarray = beL0.MatArray2Port(nt.SeriesY, w)
    shuntZ_C1:np.ndarray = beC1.MatArray2Port(nt.ShuntZ, w)
    SeriesY_L2:np.ndarray = beL2.MatArray2Port(nt.SeriesY, w)
    nc0 = nc(ZP)
    s_L0:np.ndarray = nc0.y2sSeries(seriesY_L0)
    s_C1:np.ndarray = nc0.z2sSeries(shuntZ_C1)
    s_L2:np.ndarray = nc0.y2sSeries(SeriesY_L2)
    t_L0:np.ndarray = nc0.s2tSeries(s_L0)
    t_C1:np.ndarray = nc0.s2tSeries(s_C1)
    t_L2:np.ndarray = nc0.s2tSeries(s_L2)
    t_All:np.ndarray = np.zeros(t_L0.shape, complex)
    for i in range(len(w)):
        t_All[i] = np.asmatrix(t_L0[i]) * np.asmatrix(t_C1[i]) * np.asmatrix(t_L2[i])
    s_All:np.ndarray = nc0.t2sSeries(t_All)
    return s_All
