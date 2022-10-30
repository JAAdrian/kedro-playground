"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 0.18.3
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import plot_decision_boundary, split_data, test_model, train_model


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=split_data,
                inputs=["features", "params:model_options"],
                outputs=["X_train", "X_test", "y_train", "y_test"],
                name="feature_splitting",
            ),
            node(
                func=train_model,
                inputs=["X_train", "y_train"],
                outputs="classifier",
                name="model_training",
            ),
            node(
                func=test_model,
                inputs=["classifier", "X_test", "y_test"],
                outputs=None,
                name="model_testing",
            ),
            node(
                func=plot_decision_boundary,
                inputs=["classifier", "X_train", "y_train", "params:plot_options"],
                outputs=None,
                name="model_plotting",
            ),
        ]
    )
