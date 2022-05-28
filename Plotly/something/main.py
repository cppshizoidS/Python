import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import numpy as np

from scipy.integrate import ode


XLIM = (-4, 4)  # region for drawing
YLIM = (-4, 4)  # integral curves


def f(x, y):
    return y**2 + x  # change function in this line


class InitAxes:
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(xlim=XLIM, ylim=YLIM)
        self.tune_axes()

    def tune_axes(self):
        self.ax.set_aspect('equal')
        self.ax.grid()

    def set_events(self, callback):
        self.fig.canvas.mpl_connect('button_press_event', callback)
        self.fig.canvas.mpl_connect('motion_notify_event', callback)

    def get_ax(self):
        return self.ax


class Plots:
    """ Make all plots """
    def __init__(self, ax):
        self.ax = ax
        self.ax.hlines(0, *XLIM, lw=0.5)
        self.ax.vlines(0, *YLIM, lw=0.5)
        self.dot, = ax.plot([], [], '.g')
        self.curve, = ax.plot([], [], 'm', lw=2)
        self.added = []

    def reset(self):
        self.dot.set_data([], [])
        self.curve.set_data([], [])
        self.ax.set_title("")

    def draw_idle(self):
        self.ax.figure.canvas.draw_idle()

    def draw_dot(self, x0, y0):
        self.dot.set_data([x0], [y0])

    def draw_curve(self, soln):
        self.curve.set_data(soln[0], soln[1])

    def add_new(self, soln):
        new, = self.ax.plot(soln[0], soln[1], 'r', lw=2)
        self.added.append(new)

    def set_title(self, title):
        self.ax.set_title(title)

    def clear(self):
        for item in self.added:
            item.set_data([], [])
        self.added.clear()



def dsolve(func, y0, x0):
    """ Numerical solution with "ode" class """

    de = ode(func)
    de.set_integrator('dop853')
    # de.set_integrator('zvode', method='bdf')

    dt = 0.05
    soln = [[x0], [y0]]

    # integration to the right from start point
    de.set_initial_value(y0, x0)
    while de.successful() and de.t <= XLIM[1]:
        de.integrate(de.t + dt)
        soln[0].append(de.t)
        soln[1].append(de.y[0])

    # integration to the left from start point
    de.set_initial_value(y0, x0)
    while de.successful() and de.t >= XLIM[0]:
        de.integrate(de.t - dt)
        soln[0].insert(0, de.t)
        soln[1].insert(0, de.y[0])

    return soln


def on_move(event, plots, ax):
    """ Event handler (mouse move, mouse click) """
    x0 = event.xdata
    y0 = event.ydata

    if x0 is None or y0 is None:  # mouse is out of region XLIM, YLIM
        plots.reset()
        plots.draw_idle()
        return

    if event.button == 2:
        plots.clear()

    plots.reset()
    plots.draw_dot(x0, y0)
    title = f"y({x0:.2f})={y0:.2f}"

    soln = dsolve(func=f, y0=y0, x0=x0)
    plots.draw_curve(soln)

    if event.button == 1:
        plots.add_new(soln)  # freeze plot
        print(title)

    plots.set_title(title)
    plots.draw_idle()  # make all drawings in axes


def main():
    axes = InitAxes()
    ax = axes.get_ax()

    plots = Plots(ax)

    callback = lambda event: on_move(event, plots, ax)
    axes.set_events(callback)

    plt.show()


if __name__ == "__main__":
    main()
