"""
File: CFmtUT.py
Unit test for CFmt and FmtConf
"""
from CFmt import FmtConf as fmtcnf
import CFmt
import math
import numpy as np

pi2:float = 2.0 * math.pi

def main():
    cnf0 = fmtcnf( \
        CFmt.FreqUnit.kHz, \
        CFmt.ComplexFormat.RI, \
        CFmt.MatrixFormat.Upper, \
        CFmt.TwoPortDataOrder.Modern)
    cnf1 = fmtcnf( \
        CFmt.FreqUnit.kHz, \
        CFmt.ComplexFormat.MA, \
        CFmt.MatrixFormat.Upper, \
        CFmt.TwoPortDataOrder.Modern)
    cnf2 = fmtcnf( \
        CFmt.FreqUnit.kHz, \
        CFmt.ComplexFormat.dB, \
        CFmt.MatrixFormat.Upper, \
        CFmt.TwoPortDataOrder.Modern)
    m = np.array([[1+1j, 0-0.49j], [0-0.51j, 1+1j]])
    mt = cnf0.mat2Text(m)
    m2 = cnf0.text2Mat(mt, 2)
    print(m2-m)
    mt = cnf1.mat2Text(m)
    m2 = cnf1.text2Mat(mt, 2)
    print(m2-m)
    mt = cnf2.mat2Text(m)
    m2 = cnf2.text2Mat(mt, 2)
    print(m2-m)
    return

if __name__ == "__main__":
    main()
