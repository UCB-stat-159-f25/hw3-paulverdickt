from pathlib import Path
import numpy as np
import pytest
from ligotools import readligo as rl

# Paths
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
H1 = next(DATA.glob("H-H1_LOSC_4_V2-*.hdf5"))
L1 = next(DATA.glob("L-L1_LOSC_4_V2-*.hdf5"))

def _call_reader(path):
    """Call your reader, whichever name it uses."""
    if hasattr(rl, "read_hdf5"):
        return rl.read_hdf5(str(path))
    if hasattr(rl, "loaddata"):
        return rl.loaddata(str(path))
    pytest.skip("No reader found (read_hdf5/loaddata)")

def _long_series(arrays, min_len=4096):
    """Return 1-D numpy arrays that look like real time-series (long)."""
    return [a for a in arrays if isinstance(a, np.ndarray) and a.ndim == 1 and len(a) >= min_len]

def _get_fs(result, fallback=4096):
    """Try to pull a positive sampling rate; else fallback."""
    nums = [x for x in result if isinstance(x, (int, float)) and x > 0]
    return int(nums[0]) if nums else int(fallback)

def test_reader_returns_long_series_with_consistent_lengths():
    result = _call_reader(H1)
    arrays = [x for x in result if isinstance(x, np.ndarray)]
    assert arrays, "Reader returned no numpy arrays"
    long = _long_series(arrays)
    assert long, "No long time-series arrays found (len >= 4096)"
    n = len(long[0])
    for a in long:
        assert len(a) == n, f"Long arrays must all share same length (got {len(a)} vs {n})"

def test_write_wavfile_creates_nonempty_file(tmp_path):
    result = _call_reader(L1)
    arrays = [x for x in result if isinstance(x, np.ndarray)]
    long = _long_series(arrays)
    assert long, "Need at least one long array to write wav"
    y = long[0].astype(np.float32)
    fs = _get_fs(result, fallback=4096)

    if not hasattr(rl, "write_wavfile"):
        pytest.skip("write_wavfile not found in readligo.py")
    out = tmp_path / "test.wav"
    rl.write_wavfile(str(out), int(fs), y)
    assert out.exists(), "WAV file was not created"
    assert out.stat().st_size > 0, "WAV file is empty"
