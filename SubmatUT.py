import Submat as sm
import numpy as np

def main():
    a = np.array([[-8, -7, -6, -5], [-4, -3, -2, -1], [0, 1, 2, 3], [4, 5, 6, 7]], \
                 float)
    sm_a = sm.Submat(a)
    print("a UL")
    print(sm_a.getUL())
    print("a UR")
    print(sm_a.getUR())
    print("a LL")
    print(sm_a.getLL())
    print("a LR")
    print(sm_a.getLR())

if __name__ == "__main__":
    main()
