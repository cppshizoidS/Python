import numpy as np
import plotly.graph_objects as go
from scipy.integrate import odeint

import attractors as attr


def dfunc_plotly(func, x0=(1, 0, 0), tmax=150, n=40000, args=()):
    t = np.linspace(0, tmax, n)
    f = odeint(func, x0, t, args=args)
    X, Y, Z = f.T

    c = np.linspace(0, 1, n)

    DATA = go.Scatter3d(
        x=X, y=Y, z=Z, line=dict(color=c, width=3, colorscale="Viridis"), mode="lines"
    )

    fig = go.Figure(data=DATA)
    fig.update_layout(
        margin=dict(r=10, l=10, b=10, t=10),
        paper_bgcolor="rgb(0,0,0)",
        scene=dict(
            camera=dict(up=dict(x=0, y=0, z=1), eye=dict(x=0, y=1, z=1)),
            aspectratio=dict(x=1, y=1, z=1),
            aspectmode="manual",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
        ),
    )

    return fig


if __name__ == "__main__":
    equ = attr.EQUATIONS["lorenz"]
    dfunc_plotly(**equ).show()