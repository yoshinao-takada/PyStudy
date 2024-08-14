import matplotlib.pyplot as plt
import numpy as np
import numpy.polynomial.polynomial as poly

"""1st kind chebyshev polynomial returns an even function when n is
    even and returns an odd function when n is odd."""
def Cheby1(n: int):
    x2 = poly.Polynomial([0,2])
    if (n == 0):
        return poly.Polynomial([1])
    elif (n == 1):
        return poly.Polynomial([0,1])
    else:
        return poly.polysub( \
            poly.polymul(x2,Cheby1(n-1)), \
            Cheby1(n-2))

def Cheby1HDenom(n: int, eps: float):
    c = Cheby1(n)
    c2 = poly.polymul(c, c)
    eps_c2 = poly.polymul([eps], c2)
    return poly.polyadd([1], eps_c2)
    
    
def main() :
    w = np.logspace(-2,2)
    hbw = np.zeros([len(w)])
    for i in range(len(w)):
        hbw[i] = 1 + w[i]**2
    plt.grid(True)
    plt.loglog(w,hbw)
    c1 = Cheby1HDenom(3, 0.1) # 3rd order chebyshev filter with eps = 0.1
    hbw2 = poly.polyval(w, c1[0].coef) # calc the chebyshev response.
    plt.loglog(w, hbw2)
    plt.show()

if (__name__ == "__main__"):
    main()