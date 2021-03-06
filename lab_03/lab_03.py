import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from math import exp
from numpy import fft

PERIOD = 2.0
A = 1.0
SIGMA = 1
POINT_NUMBER = 250


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

def convolution(seq1, seq2, step):
    result = fft.ifft(
        [
            v1 * v2
            for v1, v2 in zip(fft.fft(seq1), fft.fft(seq2))
        ]
    ) * step

    N = len(seq1)
    half = int(N / 2)
    if N % 2 != 0:
        half += 1

    return list(result[half:]) + list(result[:half])


def main():
    border_c = 2.0
    border = PERIOD * border_c

    step = 2 * PERIOD / POINT_NUMBER

    s_gauss = GaussSignal(A, SIGMA)
    s_rect = RectSignal(PERIOD)

    s_gauss2 = GaussSignal(A / 2, SIGMA / 2)
    s_rect2 = RectSignal(PERIOD / 2)

    t_values = [- border + i * step for i in range(int(2 * border / step) + 1)]
    gauss_values = [s_gauss.func(t) for t in t_values]
    rect_values = [s_rect.func(t) for t in t_values]

    gauss_values2 = [s_gauss2.func(t) for t in t_values]
    rect_values2 = [s_rect2.func(t) for t in t_values]

    convolution1 = convolution(rect_values, gauss_values, step)
    convolution2 = convolution(rect_values, rect_values2, step)
    convolution3 = convolution(gauss_values, gauss_values2, step)

    plt.plot(t_values, rect_values, 'r', t_values, gauss_values, 'g', t_values,  convolution1, 'b')
    plt.grid()
    plt.show()

    plt.plot(t_values, rect_values, 'r', t_values, rect_values2, 'g', t_values,  convolution2, 'b')
    plt.grid()
    plt.show()

    plt.plot(t_values, gauss_values, 'r', t_values, gauss_values2, 'g', t_values,  convolution3, 'b')
    plt.grid()
    plt.show()


if __name__ == '__main__':
    main()