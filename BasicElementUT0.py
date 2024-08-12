import BasicElement as be
import numpy as np
import NwConv as nwc

def main():
    beC1 = be.BasicElement(be.ElementType.Capacitance, 0, 0, 1, 1e-5)
    beL2 = be.BasicElement(be.ElementType.Inductance, 1e-5, 2, 0, 0)
    w = 0
    z1 = beC1.Mat2Port(be.NetworkType.ShuntZ, w)
    y2 = beL2.Mat2Port(be.NetworkType.SeriesY, w)
    conv = nwc.NwConv(np.array([1,1]))
    s1 = conv.z2s(z1)
    s2 = conv.y2s(y2)
    z1r = conv.s2z(s1)
    y2r = conv.s2y(s2)
    """
    print("--- z1, z1r ---")
    print(z1)
    print(z1r)
    print("--- y2, y2r ---")
    print(y2)
    print(y2r)
    """
    t1 = conv.s2t(s1)
    t2 = conv.s2t(s2)
    s1r = conv.t2s(t1)
    s2r = conv.t2s(t2)
    print("--- s1, s1r ---")
    print(s1)
    print(s1r)
    print("--- s2, s2r ---")
    print(s2)
    print(s2r)

if __name__ == "__main__":
    main()
