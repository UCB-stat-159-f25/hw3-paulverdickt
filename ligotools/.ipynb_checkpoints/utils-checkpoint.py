from __future__ import annotations
import numpy as np
from scipy.signal import welch
from scipy.interpolate import interp1d
from scipy.io import wavfile as _wav
import matplotlib.pyplot as plt

# -------- required by the assignment --------
def whiten(strain: np.ndarray, fs: float, seglen: float = 4.0) -> np.ndarray:
    """
    Whiten a strain time series:
      1) estimate PSD with Welch
      2) FFT -> divide by sqrt(PSD/(fs/2))
      3) iFFT back to time domain
    """
    strain = np.asarray(strain, dtype=float)
    nperseg = int(seglen * fs)
    f_psd, psd = welch(strain, fs=fs, nperseg=nperseg)

    # interpolate PSD onto positive rFFT freqs
    freqs_fft = np.fft.rfftfreq(len(strain), d=1.0/fs)
    psd_i = interp1d(f_psd, psd, bounds_error=False, fill_value="extrapolate")(freqs_fft)

    hf = np.fft.rfft(strain)
    white_hf = hf / np.sqrt(psd_i / (fs / 2.0))
    w = np.fft.irfft(white_hf, n=len(strain))
    return w

def write_wavfile(path: str, fs: int, data: np.ndarray) -> None:
    """
    Save a waveform as 16-bit PCM WAV after normalizing to [-1,1].
    """
    y = np.asarray(data, dtype=float)
    if np.max(np.abs(y)) > 0:
        y = y / np.max(np.abs(y))
    y_int16 = (y * np.iinfo(np.int16).max).astype(np.int16)
    _wav.write(path, int(fs), y_int16)

def reqshift(x: np.ndarray, fshift: float, fs: float) -> np.ndarray:
    """
    Real 'frequency shift' by multiplying with a cosine at fshift.
    (Good enough for the narrowband LIGO tutorial demo.)
    """
    x = np.asarray(x, dtype=float)
    t = np.arange(len(x)) / float(fs)
    return x * np.cos(2.0 * np.pi * fshift * t)

# -------- move the PSD plotting cell here --------
def plot_psd(strain: np.ndarray, fs: float, seglen: float = 4.0,
             ax: plt.Axes | None = None, outpath: str | None = None):
    """
    Compute and plot ASD (=sqrt(PSD)) like in the notebook's PSD cell.
    """
    nperseg = int(seglen * fs)
    f, pxx = welch(np.asarray(strain, dtype=float), fs=fs, nperseg=nperseg)
    asd = np.sqrt(pxx)

    if ax is None:
        _, ax = plt.subplots(figsize=(6, 4))
    ax.loglog(f, asd)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("ASD [strain/√Hz]")
    ax.grid(True, which="both", ls=":")

    if outpath:
        plt.savefig(outpath, dpi=150, bbox_inches="tight")
    return f, asd, ax
