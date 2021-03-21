import matplotlib  
matplotlib.use('TkAgg')   
import matplotlib.pyplot as plt
from math import exp, floor
from numpy import fft, random
from scipy import linspace


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


def noise_impulse(signal_point_number, noise_point_number, mult):
    step = floor(signal_point_number / noise_point_number)
    result = [0] * signal_point_number
    middle = round(signal_point_number / 2)
    for i in range(floor(noise_point_number / 2)):
        result[middle + i * step] = mult * (0.5 + random.rand())
        result[middle - i * step] = mult * (0.5 + random.rand())
    return result


def wiener(signal, noise):
    return [1 - (n / s) ** 2 for s, n in zip(signal, noise)]


def main():
    border_c = 2.0
    border = PERIOD * border_c

    step = 2 * PERIOD / POINT_NUMBER
    amplitude = 1.0

    s_gauss = GaussSignal(A, SIGMA)
    t_values = [- border + i * step for i in range(int(2 * border / step) + 1)]

    gauss_values = [s_gauss.func(t) for t in t_values]
    gauss_noise_values = random.normal(0, 0.05, len(t_values))
    impulse_noise_values = noise_impulse(len(gauss_values), 7, 0.4)

    values_w_gauss = [val1 + val2 for val1, val2 in zip(gauss_values, gauss_noise_values)]
    values_w_impulse = [val1 + val2 for val1, val2 in zip(gauss_values, impulse_noise_values)]

    wiener_f1 = wiener(fft.fft(values_w_gauss), fft.fft(gauss_noise_values))
    wiener_f2 = wiener(fft.fft(values_w_impulse), fft.fft(impulse_noise_values))

    plt.figure(figsize=(20, 7))


    bx = plt.subplot2grid((1, 2), (0, 1))
    plt.plot(
        t_values, values_w_gauss, 'r',
        t_values, fft.ifft([v_g * w for v_g, w in zip(fft.fft(values_w_gauss), wiener_f1)]), 'g'
    )
    bx.grid()
    bx.title.set_text("Фильтация сигнала Гаусса фильтром Винера")
    plt.xlabel('time(s)')

    cx = plt.subplot2grid((1, 2), (0, 0))
    plt.plot(
        t_values, values_w_impulse, 'r',
        t_values, fft.ifft([v_i * w for v_i, w in zip(fft.fft(values_w_impulse), wiener_f2)]), 'g'
    )
    cx.grid()
    cx.title.set_text("Фильтация импульсного сигнала фильтром Винера")
    plt.xlabel('time(s)')
    plt.show()
    

if __name__ == '__main__':
    main()
