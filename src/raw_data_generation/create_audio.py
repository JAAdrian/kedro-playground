import numpy
import pathlib
import soundfile
import uuid
from scipy import stats


_NUM_FILES_TO_CREATE = 10
_TARGET_DIRECTORY = r"data/01_raw"

_LEN_SIGNAL_SEC = 5
_NUM_CHANNELS = 2
_SAMPLE_RATE = 16_000

_GAUSSIAN_GAIN = 0.2
_LAPLACE_GAIN = (0.01 / 2)**0.5


def _get_gaussian_noise(len_samples: int, num_channels: int, gain: float):
    return gain * numpy.random.randn(len_samples, num_channels)


def _get_laplace_noise(len_samples: int, num_channels: int, gain: float):
    return stats.laplace.rvs(loc=0, scale=gain, size=(len_samples, num_channels))


def _get_filename(target_directory: pathlib.Path, type: str):
    filename = (target_directory / (type + "_" + str(uuid.uuid4()))).with_suffix(
        ".flac"
    )
    return filename.as_posix()


if __name__ == "__main__":
    target_directory = pathlib.Path(_TARGET_DIRECTORY)
    if not target_directory.is_dir():
        target_directory.mkdir()

    len_samples = round(_SAMPLE_RATE * _LEN_SIGNAL_SEC)

    for _ in range(_NUM_FILES_TO_CREATE):
        filename = _get_filename(target_directory, type="gaussian")

        signal = _get_gaussian_noise(len_samples, _NUM_CHANNELS, _GAUSSIAN_GAIN)
        soundfile.write(filename, signal, _SAMPLE_RATE)

    for _ in range(_NUM_FILES_TO_CREATE):
        filename = _get_filename(target_directory, type="laplace")

        signal = _get_laplace_noise(len_samples, _NUM_CHANNELS, _LAPLACE_GAIN)
        soundfile.write(filename, signal, _SAMPLE_RATE)
