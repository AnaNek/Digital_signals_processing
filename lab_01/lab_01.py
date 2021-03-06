import numpy as np
import matplotlib.pyplot as plt
from math import exp, sin, pi

SIGMA = 2.0
A = 1.0
PERIOD = 4.0
POINTS_COUNT = 20
STEP = 0.01

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
        return int(abs(x) <= abs(self.period))

class KotelnikovMethod:
    def __init__(self, period, points_count):
        self.period = period
        self.points_count = points_count
        self.delta = period / (points_count - 1)
        self.max_k = int(self.period / self.delta)
        self.min_k = - self.max_k

    def sinc(self, x):
        if x == 0.0:
            return 0
        return sin(x) / (x)

    def recover(self, signal, x):
        aggregation = 0
        for k in range(self.min_k, self.max_k + 1):
            new_value = signal.func(k * self.delta) * self.sinc(pi * (x / self.delta - k))

            aggregation += new_value
        return aggregation

def main():
    POINTS_COUNT = int(input("Points count:"))
    sampler = KotelnikovMethod(PERIOD, POINTS_COUNT)
    signal_gauss = GaussSignal(A, SIGMA)
    signal_rect = RectSignal(PERIOD)

    t = np.arange(-(PERIOD + 1), PERIOD + 1, STEP)
    gauss_values = [signal_gauss.func(x) for x in t]
    rect_values = [signal_rect.func(x) for x in t]

    recovered_gauss = [sampler.recover(signal_gauss, x) for x in t]
    recovered_rect = [sampler.recover(signal_rect, x) for x in t]

    plt.figure(figsize=(9, 5))
    ax = plt.subplot(1, 2, 1)
    plt.plot(t, recovered_gauss, 'r', label='recovered')
    plt.plot(t, gauss_values, 'b:', label='discrete')
    ax.grid()
    plt.xlabel('time(s)')
    ax.legend(loc='upper right', shadow=False)
    bx = plt.subplot(1, 2, 2)
    plt.plot(t, recovered_rect, 'r', label='recovered')
    plt.plot(t, rect_values, 'b:', label='discrete')
    bx.grid()
    plt.xlabel('time(s)')
    bx.legend(loc='upper right', shadow=False)
    plt.show()

if __name__ == '__main__':
    main()