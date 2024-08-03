import numpy as np

"""Operations of submatrices of 2N x 2N matrix"""
class Submat(object):
    """Constructor sets a whole matrix as self.m."""
    def __init__(self, m: np.ndarray):
        if (len(m.shape) != 2) or (m.shape[0] != m.shape[1]):
            raise("m is not a square matrix.")
        if (m.shape[0] % 2):
            raise("row nor column of m is even.")
        self.m = m

    """Get an upper-left part of self.m."""
    def getUL(self):
        n: int = self.m.shape[0] >> 1
        return np.matrix(self.m[0:n, 0:n])
    
    """Get an upper-right part of self.m."""
    def getUR(self):
        n2: int = self.m.shape[0]
        n: int = n2 >> 1
        return np.matrix(self.m[0:n, n:n2])
    
    """Get an lower-left part of self.m."""
    def getLL(self):
        n2: int = self.m.shape[0]
        n: int = n2 >> 1
        return np.matrix(self.m[n:n2, 0:n])
    
    """Get an lower-right part of self.m."""
    def getLR(self):
        n2: int = self.m.shape[0]
        n: int = n2 >> 1
        return np.matrix(self.m[n:n2, n:n2])
    
    """set sm in upper-left of self.m"""
    def setUL(self, sm: np.ndarray):
        n: int = self.m.shape[0] >> 1
        if (n != sm.shape[0]) or (n != sm.shape[1]):
            raise("matrix size mismatch.")
        self.m[0:n, 0:n] = sm
    
    """set sm in upper-right of self.m"""
    def setUR(self, sm: np.ndarray):
        n2: int = self.m.shape[0]
        n: int = n2 >> 1
        if (sm.shape[0] != n) or (sm.shape[1] != n):
            raise("matrix size mismatch.")
        self.m[0:n, n:n2] = sm
    
    """set sm in lower-left part of self.m."""
    def setLL(self, sm: np.ndarray):
        n2: int = self.m.shape[0]
        n: int = n2 >> 1
        if (sm.shape[0] != n) or (sm.shape[1] != n):
            raise("matrix size mismatch.")
        self.m[n:n2, 0:n] = sm

    """set sm in lower-right part of self.m."""
    def setLR(self, sm: np.ndarray):
        n2: int = self.m.shape[0]
        n: int = n2 >> 1
        if (sm.shape[0] != n) or (sm.shape[1] != n):
            raise("matrix size mismatch.")
        self.m[n:n2, n:n2] = sm
