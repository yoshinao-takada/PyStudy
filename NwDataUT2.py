import Filter1
import numpy as np
from TsReaderWriter import NwData as tsio
from _pyio import FileIO as file
import matplotlib.pyplot as plt
import NwConv
import math

def main():
    w:np.ndarray = Filter1.CreateW()
    s:np.ndarray = Filter1.CreateFilter()
    io:tsio = tsio()
    io2:tsio = tsio()
    io.setNwData(w, s)
    io.setHeaderComments([ \
        "3rd order Butterworth filter", \
        "fc = 1 GHz"])
    io.fmtVer1()
    ostream:file = open("s.ts", "w")
    io.write(ostream)
    ostream.close()
    istream:file = open("s.ts", "r")
    io2.read(istream)
    istream.close()
    print(f"io2.nPorts = {io2.nPorts}")
    print(f"io2.nFreqPoints = {io2.nFreqPoints}")
    print(f"io2.opt = {io2.opt.format()}")
    w2 = np.zeros(io2.nFreqPoints, float)
    s2 = np.zeros((io2.nFreqPoints, io2.nPorts, io2.nPorts), complex)    
    io2.extractNNwDataVer1(w2, s2)
    absS11 = NwConv.NwConv.magSeries(s2, 0, 0)
    absS21 = NwConv.NwConv.magSeries(s2, 1, 0)
    rcpPi2:float = 0.5 / math.pi
    plt.plot(w2 * rcpPi2, absS11, w2 * rcpPi2, absS21)
    plt.show()
    return

if __name__ == "__main__":
    main()