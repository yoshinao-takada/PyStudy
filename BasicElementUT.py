import BasicElement as be
import numpy as np
import NwConv as nwc
import matplotlib.pyplot as plt

def main():
    beC1 = be.BasicElement(be.ElementType.Capacitance, 0, 0, 1, 1e-9)
    beL2 = be.BasicElement(be.ElementType.Inductance, 1e-9, 2, 0, 0)
    w = np.linspace(0, np.pi)
    aZ1 = beC1.MatArray2Port(be.NetworkType.ShuntZ, w)
    aY2 = beL2.MatArray2Port(be.NetworkType.SeriesY, w)
    conv = nwc.NwConv([1,1])
    aS1 = conv.za2sa(aZ1)
    aS2 = conv.ya2sa(aY2)
    aT1 = conv.sa2ta(aS1)
    aT2 = conv.sa2ta(aS2)
    aTall = np.zeros(aT1.shape, complex)
    for i in range(aT2.shape[0]):
        aTall[i] = np.asmatrix(aT1[i]) * np.asmatrix(aT2[i]) * np.asmatrix(aT1[i])
    aSall = conv.ta2sa(aTall)
    s11all = np.zeros([aSall.shape[0]], complex)
    s21all = np.zeros([aSall.shape[0]], complex)
    for i in range(aSall.shape[0]):
        s11all[i] = aSall[i,0,0]
        s21all[i] = aSall[i,1,0]
    plt.plot(w, np.abs(s11all), w, np.abs(s21all))
    plt.show()
    
if __name__ == "__main__":
    main()
    
