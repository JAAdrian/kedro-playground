"""
This is a boilerplate pipeline 'feature_processing'
generated using Kedro 0.18.3
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import compute_features


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=compute_features,
                inputs=["raw_audio", "params:feature_parameters"],
                outputs="features",
                name="feature_processing",
            ),
        ]
    )
