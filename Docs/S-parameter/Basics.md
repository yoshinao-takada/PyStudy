# S-/Z-/Y-/T-parameter conversion
## S to Z, Z to S
An N-port network is assumed. Its terminal voltages and terminal sink currents
are defined as $i_i$ and $i_i$. The impedance matrix $\text{Z}$ is given and
relates $v_i$ and $i_i$ as
$$\begin{equation}\begin{bmatrix}
    v_0 \\ v_1 \\ \vdots \\ v_{N-1}
\end{bmatrix} = \text{Z}\begin{bmatrix}
    i_0 \\ i_1 \\ \vdots \\ i_{N-1}
\end{bmatrix}.\end{equation}$$

Considering S-parameter, the voltages are normalized by
the square-roots of port impedances as
$$\begin{equation}\begin{matrix}
    v_{0} & = & \sqrt{z_{\text{P}0}}u_{0}, \\
    v_{1} & = & \sqrt{z_{\text{P}1}}u_{1}, \\
    & \cdots & \\
    v_{N-1} & = & \sqrt{z_{\text{P}(N-1)}}u_{N-1}. \\
\end{matrix}\end{equation}$$
Representing in matrix-vector notation,
$$\begin{equation}
    \textbf{V} = \begin{bmatrix}
        \sqrt{z_{\text{P}0}} & 0 & \cdots & 0 \\
        0 & \sqrt{z_{\text{P}1}} & \cdots & 0 \\
        \vdots & \vdots & \ddots & 0 \\
        0 & 0 & \cdots & \sqrt{z_{\text{P}(N-1)}}
    \end{bmatrix}\textbf{U} = \text{S}_\text{ZP}\textbf{U}.
\end{equation}$$
and the currents are normalized by the square roots of port admittances as
$$\begin{equation}\begin{matrix}
    i_{0} & = & \sqrt{y_{\text{P}0}}h_{0}, \\
    i_{1} & = & \sqrt{y_{\text{P}1}}h_{1}, \\
    & \cdots & \\
    i_{N-1} & = & \sqrt{y_{\text{P}(N-1)}}h_{N-1}. \\
\end{matrix}\end{equation}$$
Representing in matrix-vector notation,
$$\begin{equation}
    \textbf{I} = \begin{bmatrix}
        \sqrt{y_{\text{P}0}} & 0 & \cdots & 0 \\
        0 & \sqrt{y_{\text{P}1}} & \cdots & 0 \\
        \vdots & \vdots & \ddots & 0 \\
        0 & 0 & \cdots & \sqrt{y_{\text{P}(N-1)}}
    \end{bmatrix}\textbf{H} = \text{S}_\text{YP}\textbf{H}.
\end{equation}$$
Including (3) and (5) into (1), it is modified as
$$\begin{equation}
    \text{S}_\text{ZP}\textbf{U} = \text{Z}\text{S}_\text{YP}\textbf{H}
\end{equation}$$

$$\begin{equation}
    \textbf{U} = \text{S}_\text{ZP}^{-1}\text{Z}\text{S}_\text{YP}\textbf{H}
        = \text{S}_\text{YP}\text{Z}\text{S}_\text{YP}\textbf{H}
\end{equation}$$

<!--(8),(9)-->
Decomposing the normalized voltages and the normalized currents into their incident and reflected components,
$$\begin{equation}
    \textbf{U} = \textbf{U}_\text{I} + \textbf{U}_\text{R}
        = (\text{I} + \text{S})\textbf{U}_\text{I},
\end{equation}$$
$$\begin{equation}
    \textbf{H} = \textbf{H}_\text{I} - \textbf{H}_\text{R}
        = \textbf{U}_\text{I} - \textbf{U}_\text{R}
        = (\text{I} - \text{S})\textbf{U}_\text{I}.
\end{equation}$$

<!--(10),(11)-->
Including (8),(9) into (7),
$$\begin{equation}
(\text{I} + \text{S})\textbf{U}_\text{I} =
    \text{S}_\text{YP}\text{Z}\text{S}_\text{YP}
        (\text{I} - \text{S})\textbf{U}_\text{I}
\end{equation}$$
$$\begin{equation}
    (\text{I}+\text{S})(\text{I}-\text{S})^{-1}=
        \text{S}_\text{YP}\text{Z}\text{S}_\text{YP}
\end{equation}$$

<!--(12)-->
$$\begin{equation}
\text{Z} = 
    \text{S}_\text{ZP}
        (\text{I}+\text{S})(\text{I}-\text{S})^{-1}
    \text{S}_\text{ZP}
\end{equation}$$

<!--(13)~(15)-->
$$\begin{equation}
(\text{I}+\text{S})=
    \text{S}_\text{YP}\text{Z}\text{S}_\text{YP}
        (\text{I}-\text{S})
\end{equation}$$
$$\begin{equation}
    (\text{I}+\text{S}_\text{YP}\text{Z}\text{S}_\text{YP})\text{S}
    = (\text{S}_\text{YP}\text{Z}\text{S}_\text{YP}-\text{I})
\end{equation}$$
$$\begin{equation}
    \text{S}
    = (\text{S}_\text{YP}\text{Z}\text{S}_\text{YP}+\text{I})^{-1}
        (\text{S}_\text{YP}\text{Z}\text{S}_\text{YP}-\text{I})
\end{equation}$$
## S to Y, Y to S
<!--(16),(17)-->
$$\begin{equation}
\text{Y} = \text{Z}^{-1} =
    (
        \text{S}_\text{ZP}
            (\text{I}+\text{S})(\text{I}-\text{S})^{-1}
        \text{S}_\text{ZP}
    )^{-1}
\end{equation}$$
$$\begin{equation}
    \text{Y} =
        \text{S}_\text{YP}(\text{I}-\text{S})(\text{I}+\text{S})^{-1}\text{S}_\text{YP}
\end{equation}$$

<!--(18),(19),(20),(21)-->
$$\begin{equation}
(\text{I}-\text{S})(\text{I}+\text{S})^{-1} =
    \text{S}_\text{ZP}\text{Y}\text{S}_\text{ZP}
\end{equation}$$

$$\begin{equation}
(\text{I}-\text{S}) = 
    \text{S}_\text{ZP}\text{Y}\text{S}_\text{ZP}
    (\text{I}+\text{S})
\end{equation}$$

$$\begin{equation}
(\text{I}-\text{S}_\text{ZP}\text{Y}\text{S}_\text{ZP}) = 
    (\text{S}_\text{ZP}\text{Y}\text{S}_\text{ZP} + \text{I})\text{S}
\end{equation}$$

$$\begin{equation}
\text{S} =
    (\text{I} + \text{S}_\text{ZP}\text{Y}\text{S}_\text{ZP})^{-1}
(\text{I}-\text{S}_\text{ZP}\text{Y}\text{S}_\text{ZP})
\end{equation}$$

## S to T, T to S
A transport matrix can be applied only to an 2N-port network.
port[0] to port[N-1] are on the left side of the network.
port[N] to port[2N-1] are on the right side of the network.
$$\begin{equation}\begin{bmatrix}
    \textbf{B}_\text{U} \\ \textbf{B}_\text{L}
\end{bmatrix}=\begin{bmatrix}
    \text{T}_\text{UL} & \text{T}_\text{UR} \\
    \text{T}_\text{LL} & \text{T}_\text{LR} \\
\end{bmatrix}\begin{bmatrix}
    \textbf{A}_\text{U} \\ \textbf{A}_\text{L}
\end{bmatrix}\end{equation}$$

Scattering matrix is applied to the 2N-port network,
$$\begin{equation}\begin{bmatrix}
    \textbf{B}_\text{U} \\ \textbf{A}_\text{L}
\end{bmatrix}=\begin{bmatrix}
    \text{S}_\text{UL} &\text{S}_\text{UR} \\
    \text{S}_\text{LL} &\text{S}_\text{LR} \\
\end{bmatrix}\begin{bmatrix}
    \textbf{B}_\text{L} \\ \textbf{A}_\text{U}
\end{bmatrix}\end{equation}$$

Decomposing (22),
$$\begin{equation}
    \textbf{B}_\text{U} = 
        \text{T}_\text{UL}\textbf{A}_\text{U} + \text{T}_\text{UR}\textbf{A}_\text{L},
\end{equation}$$
$$\begin{equation}
    \textbf{B}_\text{L} = 
        \text{T}_\text{LL}\textbf{A}_\text{U} + \text{T}_\text{LR}\textbf{A}_\text{L}.
\end{equation}$$

Decomposing (23),
$$\begin{equation}
    \textbf{B}_\text{U} =
        \text{S}_\text{UL}\textbf{B}_\text{L} + \text{S}_\text{UR}\textbf{A}_\text{U},
\end{equation}$$
$$\begin{equation}
    \textbf{A}_\text{L} =
        \text{S}_\text{LL}\textbf{B}_\text{L} + \text{S}_\text{LR}\textbf{A}_\text{U}.
\end{equation}$$

### S to T conversion
<!--(28)-->
Moving $\textbf{B}_\text{L}$ to LHS and moving
$\textbf{A}_\text{L}$ to RHS in (27),
$$\begin{equation}
    \textbf{B}_\text{L} = \text{S}_\text{LL}^{-1}
        (\textbf{A}_\text{L}-\text{S}_\text{LR}\textbf{A}_\text{U})
\end{equation}$$
<!--(29)-->
Comparing (28) and (25),
$$\begin{equation}
    \text{T}_\text{LL} = -\text{S}_\text{LL}^{-1}\text{S}_\text{LR},
\end{equation}$$
$$\begin{equation}
    \text{T}_\text{LR} = \text{S}_\text{LL}^{-1}.
\end{equation}$$
Replaceing $\textbf{B}_\text{L}$ in (26) with LSH in (28),
<!--(31)-->
$$\begin{equation}\textbf{B}_\text{U} =
    \text{S}_\text{UL}\text{S}_\text{LL}^{-1}
        (\textbf{A}_\text{L}-\text{S}_\text{LR}\textbf{A}_\text{U}) +
    \text{S}_\text{UR}\textbf{A}_\text{U}
\end{equation}$$
<!--(32)-->
$$\begin{equation}\textbf{B}_\text{U} =
    (\text{S}_\text{UR}-\text{S}_\text{UL}\text{S}_\text{LL}^{-1}\text{S}_\text{LR})\textbf{A}_\text{U} +
    \text{S}_\text{UL}\text{S}_\text{LL}^{-1}\textbf{A}_\text{L}
\end{equation}$$
Comparing (32) and (24),
<!--(33)-->
$$\begin{equation}\text{T}_\text{UL} =
    \text{S}_\text{UR}-\text{S}_\text{UL}\text{S}_\text{LL}^{-1}\text{S}_\text{LR} = \text{S}_\text{UR} + \text{S}_\text{UL}\text{T}_\text{LL},
\end{equation}$$
<!--(34)-->
$$\begin{equation}\text{T}_\text{UR} =
    \text{S}_\text{UL}\text{S}_\text{LL}^{-1} =
    \text{S}_\text{UL}\text{T}_\text{LR}
\end{equation}$$

### T to S conversion
<!--(35)-->
Moving $\textbf{B}_\text{L}$ in (25) to RHS and moving $\textbf{A}_\text{L}$ in (25) to LHS,
$$\begin{equation}\textbf{A}_\text{L} =
    \text{T}_\text{LR}^{-1}(\textbf{B}_\text{L}-\text{T}_\text{LL}\textbf{A}_\text{U}).
\end{equation}$$
Comparing (35) and (27),
$$\begin{equation}
    \text{S}_\text{LL}=\text{T}_\text{LR}^{-1},
\end{equation}$$
$$\begin{equation}
    \text{S}_\text{LR}=-\text{T}_\text{LR}^{-1}\text{T}_\text{LL}.
\end{equation}$$
Replacing $\textbf{A}_\text{L}$ in (24) with (35),
$$\begin{equation}\textbf{B}_\text{U} = 
    \text{T}_\text{UL}\textbf{A}_\text{U} + \text{T}_\text{UR}
    \text{T}_\text{LR}^{-1}(\textbf{B}_\text{L}-\text{T}_\text{LL}\textbf{A}_\text{U}),
\end{equation}$$
$$\begin{equation}\textbf{B}_\text{U} = 
    \text{T}_\text{UR}
    \text{T}_\text{LR}^{-1}\textbf{B}_\text{L} + (
        \text{T}_\text{UL}-\text{T}_\text{UR}\text{T}_\text{LR}^{-1}\text{T}_\text{LL}
    ) \textbf{A}_\text{U}
\end{equation}$$
Comparing (39) and (26),
$$\begin{equation}\text{S}_\text{UL} =
    \text{T}_\text{UR}\text{T}_\text{LR}^{-1},
\end{equation}$$
$$\begin{equation}\text{S}_\text{UR} =
    \text{T}_\text{UL}-
    \text{T}_\text{UR}\text{T}_\text{LR}^{-1}\text{T}_\text{LL}
\end{equation}$$