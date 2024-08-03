"""
File: NwConv.py
Network parameter conversion among S, T, Y, and Z.
"""
import numpy as np
import math
import Submat as sm

class NwConv(object):
    """Constructor accepts zp as a scalar number or 1-D vector of
        float or complex. The number or numbers represent ports'
        characteristic impedances."""
    def __init__(self, zp, ports:int = 2):
        self.szp = object   # sqrt of port impedances
        self.syp = object   # sqrt of port admittances
        self.i = np.identity(ports, complex)     # identity matrix
        if (type(zp)==complex) or (type(zp)==float) or (type(zp) == int) :
            # if zp is a scalar characteristic impedance common to all the ports.
            self.szp = np.asmatrix(self.i * math.sqrt(zp))
            self.syp = np.asmatrix(self.i / math.sqrt(zp))
        elif (type(zp)==np.ndarray) and (len(zp.shape) == 1):
            # if zp is a vector of port characteristic impedances.
            self.i = np.identity(len(zp), complex)
            self.szp = np.identity(len(zp), complex)
            self.syp = np.identity(len(zp), complex)
            for i in range(len(zp)):
                self.szp[i,i] = math.sqrt(zp[i])
                self.syp[i,i] = math.sqrt(1.0/zp[i])
    
    """It converts a scattering matrix to an admittance matrix."""
    def s2y(self, s: np.ndarray):
        if (len(s.shape) != 2) or (s.shape[0] != s.shape[1]):
            raise("s is not a square matrix.")
        sm = np.asmatrix(s)
        return self.syp * (self.i - sm) * np.linalg.inv(self.i + sm) * self.syp

    """It converts an admittance matrix to a scattering matrix."""
    def y2s(self, y: np.ndarray):
        if (len(y.shape) != 2) or (y.shape[0] != y.shape[1]):
            raise("y is not a square matrix.")
        ym = np.asmatrix(y)
        sys = self.szp * ym * self.szp
        return np.linalg.inv(self.i + sys) * (self.i - sys)
    
    """It converts a scattering matrix to an impedance matrix."""
    def s2z(self, s: np.ndarray):
        if (len(s.shape) != 2) or (s.shape[0] != s.shape[1]):
            raise("s is not a square matrix.")
        sm = np.asmatrix(s)
        return self.szp * (self.i + sm) * np.linalg.inv(self.i - sm) * self.szp
    
    """It converts an impedance matrix to a scattering matrix."""
    def z2s(self, z: np.ndarray):
        if (len(z.shape) != 2) or (z.shape[0] != z.shape[1]):
            raise("z is not a square matrix.")
        szs = self.syp * np.asmatrix(z) * self.syp
        return np.linalg.inv(szs + self.i) * (szs - self.i)
    
    """It converts a scatternig matrix to a transport matrix."""
    def s2t(self, s: np.ndarray):
        if (len(s.shape) != 2) or (s.shape[0] != s.shape[1]):
            raise("s is not a square matrix.")
        if (s.shape[0] % 2):
            raise("s is not a 2N-port matrix.")
        s2 = sm.Submat(s)
        sll = s2.getLL()
        slr = s2.getLR()
        sul = s2.getUL()
        sur = s2.getUR()
        t = np.zeros(s.shape, complex)
        t2 = sm.Submat(t)
        tlr = np.linalg.inv(sll)
        tll = -tlr * slr
        tur = sul * tlr
        tul = sur + sul * tll
        t2.setLL(tll)
        t2.setLR(tlr)
        t2.setUL(tul)
        t2.setUR(tur)
        return np.asmatrix(t)
    
    """It converts a transport matrix to a scattering matrix."""
    def t2s(self, t: np.ndarray):
        if (len(t.shape) != 2) or (t.shape[0] != t.shape[1]):
            raise("t is not a square matrix.")
        if (t.shape[0] % 2):
            raise("t is not a 2N-port matrix.")
        t2 = sm.Submat(t)
        tll = t2.getLL()
        tlr = t2.getLR()
        tul = t2.getUL()
        tur = t2.getUR()
        sll = np.linalg.inv(tlr)
        slr = -sll * tll
        sul = tur * sll
        sur = tul + tur * slr
        s = np.zeros(t.shape, complex)
        s2 = sm.Submat(s)
        s2.setLL(sll)
        s2.setLR(slr)
        s2.setUL(sul)
        s2.setUR(sur)
        return np.asmatrix(s)

    """It converts an array of scattering matrices
        to an array of admittance matrices."""
    def sa2ya(self, sa: np.ndarray):
        ya = np.zeros(sa.shape, complex)
        for index in range(sa.shape[0]):
            ya[index] = self.s2y(sa[index])
        return ya
    
    """It convers an array of admittance matrices
        to an array of scattering matrices."""
    def ya2sa(self, ya: np.ndarray):
        sa = np.zeros(ya.shape, complex)
        for index in range(ya.shape[0]):
            sa[index] = self.y2s(ya[index])
        return sa
    
    """It converts an array of scattering matrices
        to an array of impedance matrices."""
    def sa2za(self, sa: np.ndarray):
        za = np.zeros(sa.shape, complex)
        for index in range(sa.shape[0]):
            za[index] = self.s2z(sa[index])
        return sa
    
    """It converts an array of impedacne matrices
        to an array of scattering matrices."""
    def za2sa(self, za: np.ndarray):
        sa = np.zeros(za.shape, complex)
        for index in range(za.shape[0]):
            sa[index] = self.z2s(za[index])
        return sa
    
    """It converts an array of scattering matrices
        to an array of impedance matrices."""
    def sa2za(self, sa: np.ndarray):
        za = np.zeros(sa.shape, complex)
        for index in range(sa.shape[0]):
            za[index] = self.s2z(sa[index])
        return za
