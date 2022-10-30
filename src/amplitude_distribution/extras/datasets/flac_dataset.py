import fsspec
import numpy
import pathlib
import soundfile
from kedro.io import AbstractDataSet
from kedro.io.core import get_protocol_and_path, get_filepath_str


class FlacDataSet(AbstractDataSet[numpy.ndarray, int]):
    def __init__(self, filepath: str):
         # parse the path and protocol (e.g. file, http, s3, etc.)
        protocol, path = get_protocol_and_path(filepath)
        self._protocol = protocol
        self._filepath = pathlib.PurePosixPath(path)
        self._fs = fsspec.filesystem(self._protocol)

    def _load(self):
        load_path = get_filepath_str(self._filepath, self._protocol)
        signal, sample_rate = soundfile.read(load_path)

        return signal, sample_rate

    def _save(self):
        raise RuntimeError("Not yet implemented")

    def _describe(self):
        return dict(filepath=self._filepath, protocol=self._protocol)
