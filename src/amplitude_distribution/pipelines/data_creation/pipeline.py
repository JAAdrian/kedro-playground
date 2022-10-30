"""
This is a boilerplate pipeline 'data_creation'
generated using Kedro 0.18.3
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import clean_data, create_audio_files

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=clean_data,
                inputs="params:data_cleaning_and_creation",
                outputs=None,
                name="data_cleaning",
            ),
            node(
                func=create_audio_files,
                inputs="params:data_cleaning_and_creation",
                outputs=None,
                name="data_creation",
            ),
        ]
    )
