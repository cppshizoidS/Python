import numpy as np


def aizawa(XYZ, t, a=0.95, b=0.7, c=0.6, d=3.5, e=0.25, dz=0.1):
    """
    The Aizawa Attractor.
    x0 = (0.1,0,0)
    """
    x, y, z = XYZ
    x_dt = (z - b) * x - d * y
    y_dt = d * x + (z - b) * y
    z_dt = c + a * z - (z**3) / 3 - (x**2 + y**2) * (1 + e * z) + dz * z * x**3
    return x_dt, y_dt, z_dt


def anish_astakh(XYZ, t, u=1.2, n=0.5):
    """
    The Anishenko-Astakhov Attractor.
    x0 = (0.1,0,0)
    """
    x, y, z = XYZ
    i = 1 if x >= 0 else 0
    x_dt = u * x + y - x * z
    y_dt = -x
    z_dt = -n * z + n * i * x**2
    return x_dt, y_dt, z_dt


def arneodo(XYZ, t, a=-5.5, b=3.5, c=-1):
    """
    The Arneodo Attractor.
    x0 = (0.1,0,0)
    """
    x, y, z = XYZ
    x_dt = y
    y_dt = z
    z_dt = -a * x - b * y - z + c * x**3
    return x_dt, y_dt, z_dt


def bouali2(XYZ, t, a=0.3, c=1):
    """
    The 2nd Bouali Attractor.
    x0 = (0.1,0.1,0.1)
    """
    x, y, z = XYZ
    x_dt = x * (4 - y) + a * z
    y_dt = -y * (1 - x**2)
    z_dt = -x * (1.5 - c * z) - 0.05 * z
    return x_dt, y_dt, z_dt


def burke_shaw(XYZ, t, s=10, v=4.272):
    """
    The Burke-Shaw Attractor.
    x0 = (0.1,0.1,0.1)
    """
    x, y, z = XYZ
    x_dt = -s * (x + y)
    y_dt = -y - s * x * z
    z_dt = s * x * y + v
    return x_dt, y_dt, z_dt


def chen_celikovsky(XYZ, t, a=36, b=3, d=20):
    """
    The Chen-Celikovsky Attractor.
    x0 = (0.1,0.1,0.1)
    """
    x, y, z = XYZ
    x_dt = a * (y - x)
    y_dt = -x * z + d * y
    z_dt = x * y - b * z
    return x_dt, y_dt, z_dt


def chen_lee(XYZ, t, a=5, b=-10, d=-0.38):
    """
    The Chen-Lee Attractor.
    x0 = (1,1,1)
    """
    x, y, z = XYZ
    x_dt = a * x - y * z
    y_dt = b * y + x * z
    z_dt = d * z + x * y / 3
    return x_dt, y_dt, z_dt


def chua(XYZ, t, a=15.6, b=1, c=25.58, d=-1, e=0):
    """
    The Chua Attractor.
    x0 = (1.8,-0.7,-2.85)
    """
    x, y, z = XYZ
    G = e * x + 0.5 * (d + e) * (np.abs(x + 1) - np.abs(x - 1))
    x_dt = a * (y - x - G)
    y_dt = b * (x - y + z)
    z_dt = -c * y
    return x_dt, y_dt, z_dt


def coullet(XYZ, t, a=0.8, b=-1.1, c=-0.45, d=-1):
    """
    The Coullet Attractor.
    x0 = (0.1,0,0)
    """
    x, y, z = XYZ
    x_dt = y
    y_dt = z
    z_dt = a * x + b * y + c * z + d * x**3
    return x_dt, y_dt, z_dt


def dadras(XYZ, t, p=3, s=2.7, r=1.7, c=2, e=9):
    """
    The Dadras Attractor.
    x0 = (0.1,0.03,0)
    """
    x, y, z = XYZ
    x_dt = y - p * x + s * y * z
    y_dt = r * y - x * z + z
    z_dt = c * x * y - e * z
    return x_dt, y_dt, z_dt


def dequan(XYZ, t, a=40, b=1.833, d=0.16, e=0.65, p=55, dz=20):
    """
    The Dequan Li Attractor.
    x0 = (0.1,0,0)
    """
    x, y, z = XYZ
    x_dt = a * (y - x) + d * x * z
    y_dt = p * x + dz * y - x * z
    z_dt = b * z + x * y - e * x**2
    return x_dt, y_dt, z_dt


def finance(XYZ, t, a=0.001, b=0.2, c=1.1):
    """
    The Finance Attractor.
    x0 = (0.1,0,0)
    """
    x, y, z = XYZ
    x_dt = (1 / b - a) * x + z + x * y
    y_dt = -b * y - x**2
    z_dt = -x - c * z
    return x_dt, y_dt, z_dt


def four_wing(XYZ, t, a=5, b=16, c=2):
    """
    The Four-Wing Attractor.
    x0 = (1,-1,1)
    """
    x, y, z = XYZ
    x_dt = a * x + y + y * z
    y_dt = y * z - x * z
    z_dt = -z - c * x * y + b
    return x_dt, y_dt, z_dt


def genesio(XYZ, t, a=0.44, b=1.1, d=1):
    """
    The Genesio-Tesi Attractor.
    x0 = (0.1,0,0)
    """
    x, y, z = XYZ
    x_dt = y
    y_dt = z
    z_dt = -d * x - b * y - a * z + x**2
    return x_dt, y_dt, z_dt


def hadley(XYZ, t, a=0.2, b=4, dz=8, d=1):
    """
    The Hadley Attractor.
    x0 = (0.39,-1,0)
    """
    x, y, z = XYZ
    x_dt = -(y**2) - z**2 - a * x + a * dz
    y_dt = x * y - b * x * z - y + d
    z_dt = b * x * y + x * z - z
    return x_dt, y_dt, z_dt


def halvorsen(XYZ, t, a=1.4):
    """
    The Halvorsen Attractor.
    x0 = (-5,0,0)
    """
    x, y, z = XYZ
    x_dt = -a * x - 4 * y - 4 * z - y**2
    y_dt = -a * y - 4 * z - 4 * x - z**2
    z_dt = -a * z - 4 * x - 4 * y - x**2
    return x_dt, y_dt, z_dt


def liu_chen(XYZ, t, a=2.4, b=-3.78, c=14, d=-11, e=4, dz=5.58):
    """
    The Lui-Chen Attractor.
    x0 = (0.1,0.1,0.1)
    """
    x, y, z = XYZ
    x_dt = a * y + b * x + c * y * z
    y_dt = d * y - z + e * x * z
    z_dt = dz * z - x * y
    return x_dt, y_dt, z_dt


def lorenz(XYZ, t, the=10, r=28, b=8 / 3):
    """
    The Lorenz Attractor.
    x0 = (0,1,0)
    """
    x, y, z = XYZ
    x_dt = the * (y - x)
    y_dt = x * (r - z) - y
    z_dt = x * y - b * z
    return x_dt, y_dt, z_dt


def lorenzmod1(XYZ, t, a=0.1, b=4, dz=14, d=0.08):
    """
    The Lorenz Mod 1 Attractor.
    x0 = (0,1,0)
    """
    x, y, z = XYZ
    x_dt = -a * x + y**2 - z**2 + a * dz
    y_dt = x * (y - b * z) + d
    z_dt = -z + x * (b * y + z)
    return x_dt, y_dt, z_dt


def lorenzmod2(XYZ, t, a=0.9, b=5, dz=9.9, d=1):
    """
    The Lorenz Mod 2 Attractor.
    x0 = (1,1,1)
    """
    x, y, z = XYZ
    x_dt = -a * x + y**2 - z**2 + a * dz
    y_dt = x * (y - b * z) + d
    z_dt = -z + x * (b * y + z)
    return x_dt, y_dt, z_dt


def lu_chen(XYZ, t, a=-10, b=-4, c=18.1):
    """
    The Lu-Chen Attractor.
    x0 = (0.1,0.1,0.1)
    """
    x, y, z = XYZ
    x_dt = -a * b / (a + b) * x - y * z + c
    y_dt = a * y + x * z
    z_dt = b * z + x * y
    return x_dt, y_dt, z_dt


def newton_leipnik(XYZ, t, a=0.4, b=0.175):
    """
    The Newton-Leipnik Attractor.
    x0 = (0.349,0,-0.16)
    """
    x, y, z = XYZ
    x_dt = -a * x + y + 10 * y * z
    y_dt = -x - 0.4 * y + 5 * x * z
    z_dt = b * z - 5 * x * y
    return x_dt, y_dt, z_dt


def nose_hoover(XYZ, t, a=1.5):
    """
    The Nose-Hoover Attractor.
    x0 = (1,0,0)
    """
    x, y, z = XYZ
    x_dt = y
    y_dt = -x + y * z
    z_dt = a - y**2
    return x_dt, y_dt, z_dt


def qi_chen(XYZ, t, a=38, b=8 / 3, c=80):
    """
    The Qi-Chen Attractor.
    x0 = (1,1,1)
    """
    x, y, z = XYZ
    x_dt = a * (y - x) + y * z
    y_dt = c * x + y - x * z
    z_dt = x * y - b * z
    return x_dt, y_dt, z_dt


def rayleight_benard(XYZ, t, a=9, r=12, b=5):
    """
    The Rayleight-Benard Attractor.
    x0 = (0.1,0,0)
    """
    x, y, z = XYZ
    x_dt = a * (y - x)
    y_dt = x * (r - z) - y
    z_dt = x * y - b * z
    return x_dt, y_dt, z_dt


def roessler(XYZ, t, a=0.2, b=0.2, c=5.7):
    """
    The Roessler Attractor.
    x0 = (1,1,1)
    """
    x, y, z = XYZ
    x_dt = -(y + z)
    y_dt = x + a * y
    z_dt = b + z * (x - c)
    return x_dt, y_dt, z_dt


def rucklidge(XYZ, t, k=2, a=6.7):
    """
    The Rucklidge Attractor.
    x0 = (0.1,0,0)
    """
    x, y, z = XYZ
    x_dt = -k * x + y * (a - z)
    y_dt = x
    z_dt = -z + y**2
    return x_dt, y_dt, z_dt


def sakarya(XYZ, t, a=0.4, b=0.3):
    """
    The Sakarya Attractor.
    x0 = (1,-1,1)
    """
    x, y, z = XYZ
    x_dt = -x + y + y * z
    y_dt = -x - y + a * x * z
    z_dt = z - b * x * y
    return x_dt, y_dt, z_dt


def shimizu_mirioka(XYZ, t, a=0.75, b=0.45):
    """
    The Shinizu-Mirioka Attractor.
    x0 = (0.1,0,0)
    """
    x, y, z = XYZ
    x_dt = y
    y_dt = (1 - z) * x - a * y
    z_dt = x**2 - b * z
    return x_dt, y_dt, z_dt


def thomas(XYZ, t, b=0.19):
    """
    The Thomas Attractor.
    x0 = (0.1,0,0)
    """
    x, y, z = XYZ
    x_dt = -b * x + np.sin(y)
    y_dt = -b * y + np.sin(z)
    z_dt = -b * z + np.sin(x)
    return x_dt, y_dt, z_dt


def tsucs1(XYZ, t, a=40, b=0.833, d=0.5, e=0.65, dz=20):
    """
    The Three-Scroll Unified Chaotic System (TSUCS1) Attractor.
    x0 = (0.01,0,0)
    """
    x, y, z = XYZ
    x_dt = a * (y - x) + d * x * z
    y_dt = dz * y - x * z
    z_dt = b * z + x * y - e * x**2
    return x_dt, y_dt, z_dt


def tsucs2(XYZ, t, a=40, b=1.833, c=55, d=0.16, e=0.65, dz=20):
    """
    The Three-Scroll Unified Chaotic System (TSUCS2) Attractor.
    x0 = (0.01,0,0)
    """
    x, y, z = XYZ
    x_dt = a * (y - x) + d * x * z
    y_dt = dz * y - x * z + c * x
    z_dt = b * z + x * y - e * x**2
    return x_dt, y_dt, z_dt


def wang_sun(XYZ, t, a=0.2, b=-0.01, c=1, d=-0.4, e=-1, dz=-1):
    """
    The Wang-Sun Attractor.
    x0 = (0.1,0.1,0.1)
    """
    x, y, z = XYZ
    x_dt = a * x + c * y * z
    y_dt = b * x + d * y - x * z
    z_dt = e * z + dz * x * y
    return x_dt, y_dt, z_dt


def wimol_banlue(XYZ, t, a=2):
    """
    The Wimol-Banlue Attractor.
    x0 = (0.1,0,0)
    """
    x, y, z = XYZ
    x_dt = y - x
    y_dt = -z * np.tanh(x)
    z_dt = -a + x * y + np.abs(y)
    return x_dt, y_dt, z_dt


def yu_wang(XYZ, t, a=10, b=40, c=2, d=2.5):
    """
    The Yu-Wang Attractor.
    x0 = (0.1,0,0)
    """
    x, y, z = XYZ
    x_dt = a * (y - x)
    y_dt = b * x - c * x * z
    z_dt = np.exp(x * y) - d * z
    return x_dt, y_dt, z_dt


EQUATIONS = {
    "aizawa": {
        "func": aizawa,
        "x0": (0.1, 0, 0),
        "tmax": 150,
        "n": 40000,
    },
    "anish_astakh": {
        "func": anish_astakh,
        "x0": (0.1, 0, 0),
        "tmax": 1000,
        "n": 40000,
    },
    "arneodo": {
        "func": arneodo,
        "x0": (0.1, 0, 0),
        "tmax": 500,
        "n": 40000,
    },
    "bouali2": {
        "func": bouali2,
        "x0": (0.1, 0.1, 0.1),
        "tmax": 200,
        "n": 40000,
    },
    "burke_shaw": {
        "func": burke_shaw,
        "x0": (0.1, 0.1, 0.1),
        "tmax": 150,
        "n": 40000,
    },
    "chen_celikovsky": {
        "func": chen_celikovsky,
        "x0": (0.1, 0.1, 0.1),
        "tmax": 150,
        "n": 40000,
    },
    "chen_lee": {
        "func": chen_lee,
        "x0": (1, 1, 1),
        "tmax": 200,
        "n": 30000,
    },
    "chua": {
        "func": chua,
        "x0": (1.8, -0.7, -2.85),
        "tmax": 200,
        "n": 20000,
    },
    "coullet": {
        "func": coullet,
        "x0": (0.1, 0, 0),
        "tmax": 500,
        "n": 40000,
    },
    "dadras": {
        "func": dadras,
        "x0": (0.1, 0.03, 0),
        "tmax": 250,
        "n": 40000,
    },
    "dequan": {
        "func": dequan,
        "x0": (0.1, 0, 0),
        "tmax": 50,
        "n": 40000,
    },
    "finance": {
        "func": finance,
        "x0": (0.1, 0, 0),
        "tmax": 350,
        "n": 40000,
    },
    "four_wing": {
        "func": four_wing,
        "x0": (1, -1, 1),
        "tmax": 100,
        "n": 50000,
    },
    "genesio": {
        "func": genesio,
        "x0": (0.1, 0, 0),
        "tmax": 500,
        "n": 40000,
    },
    "hadley": {
        "func": hadley,
        "x0": (0.39, -1, 0),
        "tmax": 150,
        "n": 20000,
    },
    "halvorsen": {
        "func": halvorsen,
        "x0": (-5, 0, 0),
        "tmax": 150,
        "n": 20000,
    },
    "liu_chen": {
        "func": liu_chen,
        "x0": (0.1, 0.1, 0.1),
        "tmax": 150,
        "n": 40000,
    },
    "lorenz": {
        "func": lorenz,
        "x0": (0, 1, 0),
        "tmax": 150,
        "n": 50000,
    },
    "lorenzmod1": {
        "func": lorenzmod1,
        "x0": (0, 1, 0),
        "tmax": 150,
        "n": 40000,
    },
    "lorenzmod2": {
        "func": lorenzmod2,
        "x0": (1, 1, 1),
        "tmax": 80,
        "n": 40000,
    },
    "lu_chen": {
        "func": lu_chen,
        "x0": (0.1, 0.1, 0.1),
        "tmax": 100,
        "n": 20000,
    },
    "newton_leipnik": {
        "func": newton_leipnik,
        "x0": (0.349, 0, -0.16),
        "tmax": 350,
        "n": 40000,
    },
    "nose_hoover": {
        "func": nose_hoover,
        "x0": (1, 0, 0),
        "tmax": 150,
        "n": 20000,
    },
    "qi_chen": {
        "func": qi_chen,
        "x0": (1, 1, 1),
        "tmax": 80,
        "n": 40000,
    },
    "rayleight_benard": {
        "func": rayleight_benard,
        "x0": (0.1, 0, 0),
        "tmax": 150,
        "n": 20000,
    },
    "roessler": {
        "func": roessler,
        "x0": (1, 1, 1),
        "tmax": 300,
        "n": 40000,
    },
    "rucklidge": {
        "func": rucklidge,
        "x0": (0.1, 0, 0),
        "tmax": 300,
        "n": 40000,
    },
    "sakarya": {
        "func": sakarya,
        "x0": (1, -1, 1),
        "tmax": 400,
        "n": 40000,
    },
    "shimizu_mirioka": {
        "func": shimizu_mirioka,
        "x0": (0.1, 0, 0),
        "tmax": 400,
        "n": 40000,
    },
    "thomas": {
        "func": thomas,
        "x0": (0.1, 0, 0),
        "tmax": 200,
        "n": 40000,
    },
    "tsucs1": {
        "func": tsucs1,
        "x0": (0.01, 0, 0),
        "tmax": 80,
        "n": 40000,
    },
    "tsucs2": {
        "func": tsucs2,
        "x0": (0.01, 0, 0),
        "tmax": 50,
        "n": 40000,
    },
    "wang_sun": {
        "func": wang_sun,
        "x0": (0.1, 0.1, 0.1),
        "tmax": 1000,
        "n": 40000,
    },
    "wimol_banlue": {
        "func": wimol_banlue,
        "x0": (0.1, 0, 0),
        "tmax": 300,
        "n": 40000,
    },
    "yu_wang": {
        "func": yu_wang,
        "x0": (0.1, 0, 0),
        "tmax": 100,
        "n": 40000,
    },
}