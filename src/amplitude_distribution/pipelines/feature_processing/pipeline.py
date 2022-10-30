"""
This is a boilerplate pipeline 'feature_processing'
generated using Kedro 0.18.3
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import compute_features, create_audio_files


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=create_audio_files,
                inputs="params:data_creation",
                outputs=None,
                name="data_creation",
            ),
            node(
                func=compute_features,
                inputs="raw_audio",
                outputs="features",
                name="feature_computation",
            ),
        ]
    )
