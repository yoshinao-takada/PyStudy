import BasicElement as be
import numpy as np
import NwConv as nwc

def main():
    be0 = be.BasicElement(be.ElementType.Capacitance, 0, 0, 1, 1e-9)
    w = 2 * np.pi
    zC = be0.Mat2Port(be.NetworkType.ShuntZ, w)
    print(zC)
    conv = nwc.NwConv(1)
    s = conv.z2s(zC)
    print("--- s ---")
    print(s)
    t = conv.s2t(s)
    print("--- t ---")
    print(t)
    s2 = conv.t2s(t)
    print("--- s2 ---")
    print(s2)

if __name__ == "__main__":
    main()
    
