"""
This is a boilerplate pipeline 'feature_processing'
generated using Kedro 0.18.3
"""

import pathlib
import uuid

import numpy
import pandas
import soundfile
from scipy import stats


def _execute_normality_test(signal: numpy.ndarray) -> int:
    _, p_value = stats.normaltest(signal)
    return int(p_value < 1e-3)


def _get_kurtosis(signal: numpy.ndarray) -> float:
    return stats.kurtosis(signal)


def _parse_signal_type(file_name: str) -> int:
    if "gaussian" in file_name:
        signal_type = 0
    else:
        signal_type = 1

    return signal_type


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


def compute_features(data_set: dict) -> pandas.DataFrame:
    features = pandas.DataFrame()

    for file_name, load_function in data_set.items():
        file_class = _parse_signal_type(file_name)
        audio_signal, sample_rate = load_function()

        for channel_id, channel_signal in enumerate(audio_signal.T):
            hypothesis = _execute_normality_test(channel_signal)
            kurtosis = _get_kurtosis(channel_signal)

            new_data = {
                "Hypothesis": hypothesis,
                "Kurtosis": kurtosis,
                "Channel": channel_id + 1,
                "Label": file_class,
            }

            this_features = pandas.DataFrame(new_data, index=[0])

            features = pandas.concat((features, this_features), ignore_index=True)

    return features
