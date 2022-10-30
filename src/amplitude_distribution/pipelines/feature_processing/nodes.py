"""
This is a boilerplate pipeline 'feature_processing'
generated using Kedro 0.18.3
"""

import numpy
import pandas
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

            features = pandas.concat(
                (features, this_features), ignore_index=True
            )

    return features
