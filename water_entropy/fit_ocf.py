import sys
import numpy as np
from scipy.optimize import curve_fit

def exponential_func(x, A, B):
    return (A * np.exp(-(x - 1) /B)) 


data1 = np.loadtxt(sys.argv[1])

x_data = data1[:, 0]
y_data = data1[:, 1]

bounds = ([0, 0], [1, np.inf])
params, cov_matrix = curve_fit(exponential_func, x_data, y_data, bounds = bounds, maxfev=2000)
A_fit, B_fit = params
A_err, B_err = np.sqrt(np.diag(cov_matrix))

x_fit = np.linspace(min(x_data), max(x_data), 100) 
y_fit = exponential_func(x_fit, A_fit, B_fit)

print(B_fit)


