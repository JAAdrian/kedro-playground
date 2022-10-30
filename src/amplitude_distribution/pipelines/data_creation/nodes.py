"""
This is a boilerplate pipeline 'data_creation'
generated using Kedro 0.18.3
"""

import pathlib
import uuid

import numpy
import soundfile
from scipy import stats


def _get_gaussian_noise(len_samples: int, num_channels: int, gain: float):
    return gain * numpy.random.randn(len_samples, num_channels)


def _get_laplace_noise(len_samples: int, num_channels: int, gain: float):
    return stats.laplace.rvs(loc=0, scale=gain, size=(len_samples, num_channels))


def _get_filename(target_directory: pathlib.Path, type: str, suffix=".flac"):
    filename = (target_directory / (type + "_" + str(uuid.uuid4()))).with_suffix(suffix)
    return filename.as_posix()


def clean_data(parameters):
    if parameters["clean_existing_data"]:
        target_directory = pathlib.Path(parameters["target_directory"])

        audio_files = target_directory.glob("*{}".format(parameters["file_suffix"]))
        if audio_files:
            [file.unlink() for file in audio_files]


def create_audio_files(parameters: dict):
    target_directory = pathlib.Path(parameters["target_directory"])

    if not target_directory.is_dir():
        target_directory.mkdir()

    len_samples = round(parameters["sample_rate"] * parameters["len_signal_sec"])

    for _ in range(parameters["num_files_to_create"]):
        filename = _get_filename(
            target_directory, type="gaussian", suffix=parameters["file_suffix"]
        )

        signal = _get_gaussian_noise(
            len_samples, parameters["num_channels"], parameters["gaussian_gain"]
        )
        soundfile.write(filename, signal, parameters["sample_rate"])

    for _ in range(parameters["num_files_to_create"]):
        filename = _get_filename(
            target_directory, type="laplace", suffix=parameters["file_suffix"]
        )

        signal = _get_laplace_noise(
            len_samples, parameters["num_channels"], parameters["laplace_gain"]
        )
        soundfile.write(filename, signal, parameters["sample_rate"])
