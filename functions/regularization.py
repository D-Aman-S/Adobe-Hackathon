# regularization.py
import numpy as np

def fit_line(points):
    x = points[:, 0]
    y = points[:, 1]
    A = np.vstack([x, np.ones(len(x))]).T
    m, c = np.linalg.lstsq(A, y, rcond=None)[0]
    return m, c

def fit_circle(points):
    x = points[:, 0]
    y = points[:, 1]
    x_m = np.mean(x)
    y_m = np.mean(y)
    u = x - x_m
    v = y - y_m
    Suu = np.dot(u, u)
    Suv = np.dot(u, v)
    Svv = np.dot(v, v)
    Suuu = np.dot(u, u**2)
    Suvv = np.dot(u, v**2)
    Svvv = np.dot(v, v**2)
    Svvu = np.dot(v, u**2)
    A = np.array([[Suu, Suv], [Suv, Svv]])
    B = np.array([Suuu + Suvv, Svvv + Svvu]) / 2.0
    uc, vc = np.linalg.solve(A, B)
    xc = x_m + uc
    yc = y_m + vc
    R = np.sqrt(uc**2 + vc**2 + (Suu + Svv) / len(x))
    return xc, yc, R
