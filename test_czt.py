"""Test CZT package.

To run:

    pytest test_czt.py -v

"""

import numpy as np

import czt


def test_compare_czt_methods():
    """Compare different CZT calculation methods."""
    
    # Time data
    t = np.arange(0, 20e-3, 1e-4)
    dt = t[1] - t[0]
    Fs = 1 / dt
    N = len(t)

    # Signal data
    def model(t):
        output = (1.0 * np.sin(2 * np.pi * 1e3 * t) + 
                  0.3 * np.sin(2 * np.pi * 2e3 * t) + 
                  0.1 * np.sin(2 * np.pi * 3e3 * t)) * np.exp(-1e3 * t)
        return output
    x = model(t)

    # Calculate CZT using different methods
    X_czt1 = czt.czt_simple(x)
    X_czt2 = czt.czt(x, t_method='ce')
    X_czt3 = czt.czt(x, t_method='pd')
    X_czt4 = czt.czt(x, t_method='mm')
    X_czt5 = czt.czt(x, t_method='ce', f_method='fast')
    X_czt6 = czt.czt(x, t_method='pd', f_method='fast')
    X_czt7 = czt.czt(x, t_method='mm', f_method='fast')

    # # Debug
    # import matplotlib.pyplot as plt 
    # plt.figure()
    # plt.plot(np.abs(X_czt1))
    # plt.plot(np.abs(X_czt2))
    # plt.plot(np.abs(X_czt3))
    # plt.plot(np.abs(X_czt4))
    # plt.plot(np.abs(X_czt5))
    # plt.plot(np.abs(X_czt6))
    # plt.plot(np.abs(X_czt7))
    # plt.figure()
    # plt.plot(X_czt1.real)
    # plt.plot(X_czt2.real)
    # plt.plot(X_czt3.real)
    # plt.plot(X_czt4.real)
    # plt.plot(X_czt5.real)
    # plt.plot(X_czt6.real)
    # plt.plot(X_czt7.real)
    # plt.figure()
    # plt.plot(X_czt1.imag)
    # plt.plot(X_czt2.imag)
    # plt.plot(X_czt3.imag)
    # plt.plot(X_czt4.imag)
    # plt.plot(X_czt5.imag)
    # plt.plot(X_czt6.imag)
    # plt.plot(X_czt7.imag)
    # plt.show()

    # Compare Toeplitz matrix multiplication methods
    np.testing.assert_almost_equal(X_czt1, X_czt2, decimal=12)
    np.testing.assert_almost_equal(X_czt1, X_czt3, decimal=12)
    np.testing.assert_almost_equal(X_czt1, X_czt4, decimal=12)

    # Compare FFT methods
    np.testing.assert_almost_equal(X_czt1, X_czt5, decimal=1)
    np.testing.assert_almost_equal(X_czt1, X_czt6, decimal=1)
    np.testing.assert_almost_equal(X_czt1, X_czt7, decimal=1)


def test_compare_czt_to_fft():
    """Compare CZT to FFT."""
    
    # Time data
    t = np.arange(0, 20e-3, 1e-4)
    dt = t[1] - t[0]
    Fs = 1 / dt
    N = len(t)

    # Signal data
    def model(t):
        output = (1.0 * np.sin(2 * np.pi * 1e3 * t) + 
                  0.3 * np.sin(2 * np.pi * 2e3 * t) + 
                  0.1 * np.sin(2 * np.pi * 3e3 * t)) * np.exp(-1e3 * t)
        return output
    x = model(t)

    # CZT (defaults to FFT)
    X_czt = czt.czt(x)

    # FFT
    X_fft = np.fft.fft(x)

    # # Debug
    # import matplotlib.pyplot as plt 
    # plt.figure()
    # plt.plot(np.abs(X_czt), 'k')
    # plt.plot(np.abs(X_fft), 'r--')
    # plt.figure()
    # plt.plot(X_czt.real, 'k')
    # plt.plot(X_fft.real, 'r--')
    # plt.figure()
    # plt.plot(X_czt.imag, 'k')
    # plt.plot(X_fft.imag, 'r--')
    # plt.show()

    # Compare
    np.testing.assert_almost_equal(X_czt, X_fft, decimal=12)


if __name__ == "__main__":
    test_compare_czt_methods()
    test_compare_czt_to_fft()
