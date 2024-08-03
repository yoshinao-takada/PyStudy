# Elementary passive devices
## Termination
### Typical resistance with parasitics
It is composed of a main resistance, a series parasitic inductance,
and a shunt parasitic capacitance.
The admittance is
$$\begin{equation}
y = sC + {1\over{R + sL}}.
\end{equation}$$
### Typical inductance with parasitics
It is composed of a main inductance, a series parasitic resistance, and
a shunt parasitic capacitance.
The admittance formula is identical to (1).

### Typical capacitance with parasitics
It is composed of a main capacitance, a series parasitic resistance, 
a series parasitic inductance, and a shunt parasitic conductance, $G$.
The admittance formula is
$$\begin{equation}
y = G + {1\over{R + sL + 1/sC}}
\end{equation}$$

## Seriese two-terminal
A two-port network composed of a series two-terminal element can be
formulated in an admmittance matrix.
$$\begin{equation}
\text{Y}=\begin{bmatrix}
y_e & -y_e \\
-y_e & y_e
\end{bmatrix}
\end{equation}$$

## Shunt one-terminal
A two-port network composed of a shunt two-terminal element can be
formulated in an impedance matrix.
$$\begin{equation}
\text{Z} = \begin{bmatrix}
    z_e & z_e \\
    z_e & z_e
\end{bmatrix}
\end{equation}$$

## Python classes
```
"""Basic two-terminal element definition and admittance evaluation"""
class BasicElement(object):
    """Constructor defines a two terminal element with parasitic
    elements"""
    __init__(etype, r, l, c, g=0):
        ...

    """Get the element admittance"""
    def y():
        return xx

    """Get the admittance mat
    def YmSeries():
        return mY
```