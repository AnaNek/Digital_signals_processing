import numpy as np
import matplotlib.pyplot as plt
from math import exp, sin, pi, cos

T = 2.0
A = 1.0
SIGMA = 0.5

class Signal:
    def func(self, x):
        pass

class GaussSignal(Signal):
    def __init__(self, amplitude, sigma):
        self.amplitude = amplitude
        self.sigma = sigma

    def func(self, x):
        return self.amplitude * exp(- (x ** 2) / (self.sigma ** 2))

class RectSignal(Signal):
    def __init__(self, period):
        self.period = period

    def func(self, x):
        dif = abs(x) - abs(self.period)
        if dif == 0:
            return 0.5
        elif dif > 0:
            return 0
        else:
            return 1

def dft(seq):
    N = len(seq)
    result = []
    for k in range(N):
        accumutation = 0
        for n in range(N):
            coefficient = 2 * pi * k * n / N
            cosx, sinx = cos(coefficient), sin(coefficient)
            accumutation += seq[n] * (cosx - 1j * sinx)
        result.append(accumutation)

    return result

def main():
    delta = 5
    step = 0.05
    t = np.arange(-delta, delta, step)
    signal_gauss = GaussSignal(A, SIGMA)
    signal_rect = RectSignal(T)

    gauss_values = [signal_gauss.func(x) for x in t]
    rect_values = [signal_rect.func(x) for x in t]
    xs = np.arange(0, len(t), 1)

    # fft с эффектом близнецов
    y_rec = np.fft.fft(rect_values)
    y_gauss = np.fft.fft(gauss_values)

    # fft без эффекта близнецов
    y_rec_without_twin = np.fft.fftshift(y_rec)
    y_rec_without_twin = [(abs(y)/len(xs)) for y in y_rec_without_twin]
    y_gauss_without_twin = np.fft.fftshift(y_gauss)
    y_gauss_without_twin = [(abs(y)/len(xs)) for y in y_gauss_without_twin]

    # dft с эффектом близнецов
    z_rec = dft(rect_values)
    z_gauss = dft(gauss_values)

    # dft без эффекта близнецов
    z_rec_without_twin = np.fft.fftshift(z_rec)
    z_rec_without_twin = [(abs(z)/len(xs)) for z in z_rec_without_twin]
    z_gauss_without_twin = np.fft.fftshift(z_gauss)
    z_gauss_without_twin = [(abs(z)/len(xs)) for z in z_gauss_without_twin]

    # взять значения по модулю
    y_gauss = [(abs(y)/len(xs)) for y in y_gauss]
    y_rec = [(abs(y)/len(xs)) for y in y_rec]
    z_gauss = [(abs(z)/len(xs)) for z in z_gauss]
    z_rec = [(abs(z)/len(xs)) for z in z_rec]

    plt.figure(figsize=(12, 7))
    ax = plt.subplot2grid((3, 2), (0, 0))
    plt.plot(xs, y_rec, 'r', xs, y_rec_without_twin, 'b')
    ax.grid()
    ax.title.set_text("FFT Rect")
    plt.xlabel('time(s)')

    bx = plt.subplot2grid((3, 2), (0, 1))
    plt.plot(xs, y_gauss, 'r', xs, y_gauss_without_twin, 'b')
    bx.grid()
    bx.title.set_text("FFT Gauss")
    plt.xlabel('time(s)')

    cx = plt.subplot2grid((3, 2), (2, 0))
    plt.plot(xs, z_rec, 'r', xs, z_rec_without_twin, 'b')
    cx.grid()
    cx.title.set_text("DFT Rect")
    plt.xlabel('time(s)')

    dx = plt.subplot2grid((3, 2), (2, 1))
    plt.plot(xs, z_gauss, 'r', xs, z_gauss_without_twin, 'b')
    dx.grid()
    dx.title.set_text("DFT Gauss")
    plt.xlabel('time(s)')

    plt.show()

if __name__ == '__main__':
    main()