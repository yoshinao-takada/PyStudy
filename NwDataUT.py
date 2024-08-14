import Filter1
import numpy as np
from NwData import NwDataAttributes as nwattrib
from NwData import NwData as nwdata
import CFmt

def main():
    w:np.ndarray = Filter1.CreateW()
    s:np.ndarray = Filter1.CreateFilter()
    data:nwdata = nwdata(w, s)
    attrib:nwattrib = nwattrib()
    attrib.ver = "2.1"
    attrib.numPorts = 2
    attrib.tpdo = CFmt.TwoPortDataOrder.Modern
    attrib.numfrqs = len(w)
    attrib.numnoisefrqs = 0
    attrib.matfmt = CFmt.MatrixFormat.Full
    tsstream = open("s.ts", "w")
    attrib.writePreamble(tsstream)
    conf:CFmt.FmtConf = CFmt.FmtConf( \
        CFmt.FreqUnit.GHz, CFmt.ComplexFormat.MA, attrib.matfmt, \
        attrib.tpdo)
    data.write(conf, tsstream)
    tsstream.write(nwattrib.END_KEY + "\n")
    tsstream.close()
    return

if __name__ == "__main__":
    main()
